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
  
  objectName(obj)::
    obj.kind + '/' +
       (if std.objectHas(obj.metadata, 'namespace') then obj.metadata.namespace + '/' else '') +
       obj.metadata.name,
  
  named(objectlist)::
    {
      [$.objectName(k)]: k,
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
