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
