# Environment

Kasane supports references to the external environment in yaml, jsonnet and Kasanefiles.

A layer description in Kasanefile can be provided with a simple name that's actually a shorthand for

```yaml
- name: layername
```

Two more options supported by layers are `loader` and `when`.

Loaders allow to transform the loaded data. YAML suppors the loader `yamlenv` that handles a common syntax `${VAR}` found in numerous vendored YAML files.

Jsonnet supports the environment natively via an exported function `std.native("env")('VAR')`.

Kasanefiles can skip or include additional layers based on the environment, specified by `when` condition -- if you ever worked with ansible you'll immediately know how it operates. The string in the `when` condition is a jinja2 expression with all the environment options exposed.

```bash
$ cat kasanefile
layers:
- name: object.yaml
  loader: yamlenv
- name: patch.jsonnet
  when: not ignore_jsonnet

$ kasane show
Kind: VendoredObject
config:
  defaultFlag: UNRESOLVED_ENV_VAR__DEFAULT_VALUE
  jsonnetEnv: UNRESOLVED_ENV_VAR__OTHER_VALUE
metadata:
  name: PreconfiguredObject
```

Notice how by default kasane doesn't fail if the environment is undefined. `kasane show` allows to preview your code quickly but `kasane apply` will fail if environment variables are missing. You can run `kasane show --no-ignore-env` to replicate the same behavior with the show command.

```bash
$ kasane -e DEFAULT_VALUE=10 -e OTHER_VALUE=11 show --no-ignore-env
Kind: VendoredObject
config:
  defaultFlag: 10
  jsonnetEnv: '11'
metadata:
  name: PreconfiguredObject
```

Notice how the environment resolves to whatever is contextually sensible in YAML but always to a string in Jsonnet. You must use the appropriate type casting in jsonnet files.

```bash
kasane -e DEFAULT_VALUE=10 -e ignore_jsonnet=true show --no-ignore-env
Kind: VendoredObject
metadata:
  name: PreconfiguredObject
config:
  defaultFlag: 10
```

If the layer is skipped its environment isn't evaluated and it's fine to skip unused environment fields.

You can also pass the environment via the os environment `KASANE_JSONNET_ENV` variable. It must be a json dictionary:

```bash
KASANE_JSONNET_ENV='{"DEFAULT_VALUE":"20"}' kasane show
Kind: VendoredObject
config:
  defaultFlag: 20
  jsonnetEnv: UNRESOLVED_ENV_VAR__OTHER_VALUE
metadata:
  name: PreconfiguredObject
```
