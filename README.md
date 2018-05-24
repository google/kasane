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

## Examples

* [Simple Layers](https://github.com/google/kasane/tree/master/examples/01-simple-layers) is an introduction to kasane features.
* [Jsonnet Transformations](https://github.com/google/kasane/tree/master/examples/02-jsonnet-transformations) shows how to use Jsonnet to transform objects.
* [Environment](https://github.com/google/kasane/tree/master/examples/03-environment) explains how to use the external environment for customized pipelines.
* [Complex Service](https://github.com/google/kasane/tree/master/examples/04-complex-service) shows all the features together by using the upstream configuration for kubernetes dashboard, adding an ingress, and optionally enabling istio sidecar.
