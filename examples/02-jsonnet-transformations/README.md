# Jsonnet Transformations

Kasane uses [Jsonnet](http://jsonnet.org/) to transform objects in its pipeline. You can use jsonnet to define new objects, but more commonly you'd use it to make paches to vendored dependencies. This example shows how to modify a vendored dependency.

```bash
$ cat kasanefile
layers:
- https://raw.githubusercontent.com/google/kasane/master/examples/02-jsonnet-transformations/object.yaml
- patch.jsonnet

$ kasane update

$ kasane show
kind: VendoredObject
config:
  defaultFlag: 42
  otherFlag: don't change
metadata:
  name: PreconfiguredObject
```

Jsonnet files receive the **array** with all the previous layers concatenated as a function input named `layers` and **must** return an array with the results. It might be a completely different set of objects but it still must be an array.
