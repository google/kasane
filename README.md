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

* [Simple Layers](examples/01-simple-layers) is an introduction to kasane features.
* [Jsonnet Transformations](examples/02-jsonnet-transformations) shows how to use Jsonnet to transform objects.
* [Environment](examples/03-environment) explains how to use the external environment for customized pipelines.
* [Complex Service](examples/04-complex-service) shows all the features together by using the upstream configuration for kubernetes dashboard, adding an ingress, and optionally enabling istio sidecar.

## Similar tools

### Helm

Helm is fully-featured package management solution for kubrnetes. Compared to it, kasane is a swiss army knife. It's simple, lightweight, doesn't install helper code into your production. Kasane allows you to use original YAML files written by application authors, modifying them to your local needs. If you see a `kubectl apply -f http://` example you can turn it into a Kasane deployment with a single line of code and then extend it to your needs.

Kasane doesn't do any templating, relying on Jsonnet for data manipulation. You won't ever need to count number of spaces to make sure your yaml go template is rendered correctly.

### Ksonnet

Kasane is similar to Ksonnet but is much simpler to use. Kasane allows to re-use original YAML files and minimizes amount of custom Jsonnet code you need to write. Most of the time your Kasane project would consist of a Kasanefile and single yaml or jsonnet file. Still, Kasane allows runtime flexibility with conditional layers and custom environment.

## License

Kasane is distributed under Apache-2 [license](LICENSE). See the [contributing guidelines](CONTRIBUTING.md) on how you can contribute to the project.
