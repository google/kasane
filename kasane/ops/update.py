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

import subprocess
from io import StringIO

from ruamel.yaml import YAML
yaml = YAML()

from . import common, jsonnet

def update(path: str, rc: common.RuntimeConfig, lock_all: bool) -> None:
  cfg = common.get_config(path, rc)
  lockedlayers = []
  for l in cfg.layers:
    if not lock_all and not (l.is_remote or l.check_hash):
      continue
    l.vendor_content()
    lockedlayers.append(dict(
      name=l.name,
      hash=l.content_digest,
    ))

  lockfile = dict(layers=lockedlayers)
  
  cfg.write_lockfile(lockfile)
