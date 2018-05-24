# Kasane

kasane [ 重ね ] (n.) pile; heap; layers

**This is not an official Google product**

**This is also a PoC. It works, though (for some extent of "works")**

Kasane is a layering tool for kubernetes. It allows you to use the officially published YAML documents and extend them further with your local configuration.

Kasane can utilise Jsonnet for deep object modification and patching.

## Installation

Kasane requires Python 3+. Install via pip:

```shell
pip install kasane
```

## Sample

Kasanefile:
```yaml
layers:
- https://raw.githubusercontent.com/kubernetes/dashboard/master/src/deploy/recommended/kubernetes-dashboard.yaml
- name: service.override.jsonnet
  when: expose_http
- name: istio
  loader: inject
  when: istio
```

service.override.jsonnet:

```jsonnet
local h = import 'helpers.libsonnet';

function (layers)

h.list(h.named(layers) {
  'Service/kube-system/kubernetes-dashboard'+: {
    spec+: {
      ports: [{
        name: 'http',
        port: 80,
        targetPort: 9090,
      }],
    },
  },
  'Deployment/kube-system/kubernetes-dashboard'+: h.patchContainer({
    args: [
      '--insecure-bind-address=0.0.0.0',
      '--insecure-port=9090',
      '--enable-insecure-login',
      '--heapster-host=http://heapster.kube-system.svc:80',
    ],
    livenessProbe:: null,
  }),
})
```

helpers.libsonnet:
```jsonnet
{
  patchPodSpec(dep, patch)::
      dep { spec+: { template+: { spec+: patch } } },

  patchContainer(container)::
    {
      spec+: { template+: { spec+: {
        local checkContainerCount = std.assertEqual(std.length(super.continers), 1),

        containers: [super.containers[0] + container],
    } } } },
  
  patchPort(portNumber, portSpec)::
    {
      spec+: {
        ports: std.map(
            function(oldPort)
                if oldPort.port == portNumber then oldPort + portSpec else oldPort,
            super.ports),
      },
    },
  
  named(objectlist)::
    {
      [k.kind + '/' +
       (if std.objectHas(k.metadata, 'namespace') then k.metadata.namespace + '/' else '') +
       k.metadata.name]: k,
      for k in
      std.makeArray(
          std.length(objectlist),
          function(i)
              objectlist[i] + {_named_object_index:: i})
    },

  list(objecthash)::
    local objs = [objecthash[f] for f in std.objectFields(objecthash)];
    local objsKeyed = {[std.toString(o._named_object_index)]: o for o in objs};
    [o
      for o in std.makeArray(
        std.length(objs),
        function(i)
            local k = std.toString(i);
            if std.objectHas(objsKeyed, k) then objsKeyed[k] else null)
      if o != null],
  
  env(name)::
    std.native("env")(name),
}
```

This is a sample deployment for kubernetes dashboard.

Kasane will calculate the hash of the remote layers and store them in a local vendored dir. This way you can version control everything required to deploy your app but also can do updates easily when upstream changes.

Layers are joined in order. Every layer must render into an array of k8s objects.

Joining several YAML layers concatenates them together. A Jsonnet layer is provided with a named argument `layers` which is a list of all the concatendated objects before it. It's expected that the layer will return the list of objects as well. For simplicity of naming the helpers library provides two functions: `named`, which turns the input into a map keyed by object kind, namespace and name; and `list` that renders the named map back preserving the original object order.

Kasane has support for custom loaders of which there's one: `istio` pipes the objects through the istio injector.

Kasane supports conditions using jinja2 with `when:` syntax. Those are equivalent to Ansible's conditions.
