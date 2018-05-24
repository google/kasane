# Simple Layers

In the simplest mode of operation Kasane walks through the layers in order and concatenates them. This can be useful in a case when you need to source an external file and then add several local objects.

Remote files must be vendored prior to use. Kasane verifies the remote hash to keep track of the changing upstream and `kasane update` will sync the state to the latest one.

```bash
$ cat Kasanefile
layers:
- first.yaml
- https://raw.githubusercontent.com/google/kasane/master/examples/01-simple-layers/second.yaml

$ kasane update

$ kasane show
kind: FakeObject
metadata:
  name: fake
---
kind: FakeObject
metadata:
  name: fake2
---
kind: FakeObject
metadata:
  name: fake3
```

The current verison supports only the simple http[s] upstreams.

Notice how `kasane update` creates `Kasanefile.lock` with the hash of the remote file.
