# Copyright 2018 Google LLC
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     https://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import shutil
import subprocess
from io import StringIO

from ruamel.yaml import YAML
yaml = YAML()

from . import common, jsonnet

def show(path: str, rc: common.RuntimeConfig, highlight: bool, filter_kind: str) -> None:
  cfg = common.get_config(path, rc)
  try:
    data = cfg.run()
  except common.RemoteNotVendoredError as e:
    print("layer {name} isn't vendored yet. Run kasane update.".format(name=e.layer.name))
    exit(1)
  s = StringIO()
  if filter_kind:
    filter_kind = filter_kind.lower()
    data = list(filter(lambda o: o['kind'].lower() == filter_kind, data))
  yaml.dump_all(data, s)
  val = s.getvalue()
  if highlight and shutil.which('highlight') != None:
    subprocess.run(['highlight', '-l', 'yaml'], input=val.encode('utf-8'))
  else:
    print(val, end='')
