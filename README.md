# Kasane

![](https://raw.githubusercontent.com/google/kasane/master/logo.png)

[![Build Status](https://travis-ci.org/google/kasane.svg?branch=master)](https://travis-ci.org/google/kasane) [![Coverage Status](https://coveralls.io/repos/github/google/kasane/badge.svg?branch=master)](https://coveralls.io/github/google/kasane?branch=master)

kasane [ 重ね ] (n.) pile; heap; layers

**This is not an official Google product**

Kasane is a layering tool for kubernetes. It allows you to use the officially published YAML documents and extend them further with your local configuration.

Kasane can utilise Jsonnet for deep object modification and patching.

## Installation

Kasane requires Python 3+. Install via pip:

```shell
pip install kasane
```

Installation via Homebrew:

```shell
brew tap google/kasane https://github.com/google/kasane.git
brew install google/kasane/kasane
```

## Running from a Docker container

You can run kasane from a docker container, the official image is `gcr.io/kasaneapp/kasane`. The image is based on alpine and comes pre-packaged with bash, curl, git and kubectl in addition to kasane itself. The workdir is set to `/app` and the default command is `kasane show` so you can quickly examine your local Kasanefiles like this:

```bash
$ docker run --rm -ti -v $PWD/examples/03-environment:/app gcr.io/kasaneapp/kasane
config:
  defaultFlag: UNRESOLVED_ENV_VAR__DEFAULT_VALUE
  defaultFromKasanefile: value
  jsonnetEnv: UNRESOLVED_ENV_VAR__OTHER_VALUE
kind: VendoredObject
metadata:
  name: PreconfiguredObject
```

Tagged builds for versions starting with 0.1.4 are also available as e.g. `gcr.io/kasaneapp/kasane:0.1.4`.

## Examples

* [Simple Layers](examples/01-simple-layers) is an introduction to kasane features.
* [Jsonnet Transformations](examples/02-jsonnet-transformations) shows how to use Jsonnet to transform objects.
* [Environment](examples/03-environment) explains how to use the external environment for customized pipelines.
* [Complex Service](examples/04-complex-service) shows all the features together by using the upstream configuration for kubernetes dashboard, adding an ingress, and optionally enabling istio sidecar.

## Similar tools

### Helm

Helm is fully-featured package management solution for kubernetes. Compared to it, kasane is a swiss army knife. It's simple, lightweight, doesn't install helper code into your production. Kasane allows you to use original YAML files written by application authors, modifying them to your local needs. If you see a `kubectl apply -f http://` example you can turn it into a Kasane deployment with a single line of code and then extend it to your needs.

Kasane doesn't do any templating, relying on Jsonnet for data manipulation. You won't ever need to count number of spaces to make sure your yaml go template is rendered correctly.

### Ksonnet

Kasane is similar to Ksonnet but is much simpler to use. Kasane allows to re-use original YAML files and minimizes amount of custom Jsonnet code you need to write. Most of the time your Kasane project would consist of a Kasanefile and single yaml or jsonnet file. Still, Kasane allows runtime flexibility with conditional layers and custom environment.

## License

Kasane is distributed under Apache-2 [license](LICENSE). See the [contributing guidelines](CONTRIBUTING.md) on how you can contribute to the project.
