# Complex Service

This example demonstrates the use of kasane helpers library and `istio` loader to load kubernetes dashboard and optionally add istio sidecar.

```bash
$ kasane show
kasane show -k Ingress
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: dashboard-ingress
  namespace: kube-system
  annotations:
    nginx.ingress.kubernetes.io/auth-tls-secret: ingress-nginx/ingress-client-cert
spec:
  rules:
  - host: dashboard.example.com
    http:
      paths:
      - backend:
          serviceName: kubernetes-dashboard
          servicePort: 80
  tls:
  - secretName: wildcard-example-com
    hosts:
    - dashboard.example.com
```

Notice how you can use `-k $KIND` to quickly filter the output by kubernetes kind field.
