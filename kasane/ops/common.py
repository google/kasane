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

import re
from typing import Optional, List, Any, Dict
import os
from collections import namedtuple
import hashlib
from io import StringIO
import subprocess
import pathlib

from ruamel.yaml import YAML, comments
import json
import requests
from jinja2 import Template

yaml = YAML()
yaml.allow_duplicate_keys = True  # https://github.com/istio/istio/issues/2330

from .jsonnet import Jsonnet

CONFIG_NAME = 'Kasanefile'
LOCKFILE_NAME = 'Kasanefile.lock'

RuntimeConfig = namedtuple('RuntimeConfig', ['check_hashes', 'jsonnet', 'kubeconfig'])

class RemoteNotVendoredError(RuntimeError):
  def __init__(self, layer):
    super().__init__()
    self.layer = layer

class Config(object):
  def __init__(self, path: str, configdata: dict, lockdata: dict, rc: RuntimeConfig) -> None:
    self._configdata = configdata
    self._lockdata = lockdata
    self.path = path
    self.vendor_dir = os.path.join(path, 'vendor')

    self.namespace = configdata.get('namespace')
    self.default_loader = configdata.get('default_loader')
    self.localenv = configdata.get('environment', {})
    self.layers: List[Layer] = []
    self.rc = rc

    merged_env = dict()
    merged_env.update(self.localenv)
    merged_env.update(self.rc.jsonnet.env)
    self.rc.jsonnet.env = merged_env
    
    for l in configdata['layers']:
      if isinstance(l, str):
        l = {'name': l}
      d: Dict[str, Any] = l
      d.update(next((lk for lk in lockdata['layers'] if l['name'] == lk.get('name')), {}))
      self.layers.append(Layer.build(d, self))
  
  def run(self) -> Any:
    data: List[Any] = []
    for l in self.layers:
      if not l.should_run():
        continue
      data = l.run(data)
    return data
  
  def write_lockfile(self, newlockfile):
    lockpath = os.path.join(self.path, LOCKFILE_NAME)
    s = StringIO()
    yaml.dump(newlockfile, s)
    val = s.getvalue()
    with open(lockpath, 'w') as f:
      f.write(val)

class Layer(object):
  def __init__(self, data: dict, cfg: Config) -> None:
    self.name: str = data['name']
    self.hash: Optional[str] = data.get('hash')
    self.loader: Optional[str] = cfg.default_loader
    if data.get('loader'):
      self.loader = data.get('loader')
    self.when: Optional[str] = data.get('when')
    self.ignore_namespace: Optional[str] = data.get('ignore_namespace', False)
    self.check_hash: str = data.get('check_hash', False)
    self.__content: Optional[str] = None
    self.__content_digest: Optional[str] = None
    self._cfg = cfg
  
  @staticmethod
  def build(data: dict, cfg: Config) -> Any:
    name = data['name']
    if data.get('loader') == 'inject':
      return InjectLayer(data, cfg)
    if name.endswith('.yaml') or name.endswith('.yml'):
      return DataLayer(data, cfg)
    elif name.endswith('.jsonnet'):
      return JsonnetLayer(data, cfg)
    else:
      return None
  
  @property
  def is_remote(self) -> bool:
    if isinstance(self.name, comments.TaggedScalar):
      return False
    return self.name.startswith('http://') or self.name.startswith('https://')

  @property
  def vendored_path(self) -> str:
    if not self.is_remote:
      raise RuntimeError('only remote layers can be vendored')
    if self.name.startswith('http://'):
      return os.path.join(self._cfg.vendor_dir, self.name[7:])
    elif self.name.startswith('https://'):
      return os.path.join(self._cfg.vendor_dir, self.name[8:])
    else:
      raise RuntimeError('don\'t know how to vendor {}'.format(self.name))
  
  @property
  def content(self) -> str:
    if not self.__content:
      self.__content = self._load_content()
    return self.__content

  @property
  def content_digest(self) -> str:
    if not self.__content_digest:
      m = hashlib.sha256()
      m.update(self.content.encode('utf-8'))
      self.__content_digest = m.hexdigest()
    return self.__content_digest
  
  def _load_content(self) -> str:
    if self.is_remote:
      path = self.vendored_path
    else:
      path = os.path.join(self._cfg.path, self.name)
    
    try:
      return open(path).read()
    except FileNotFoundError:
      if self.is_remote:
        raise RemoteNotVendoredError(self)
      raise
  
  def vendor_content(self):
    if not self.is_remote:
      return
    r = requests.get(self.name)
    data = r.text
    pathlib.Path(os.path.dirname(self.vendored_path)).mkdir(parents=True, exist_ok=True)
    open(self.vendored_path, 'w').write(data)
  
  def run(self, previous: List[Any]) -> Any:
    raise RuntimeError('not implemented')
  
  def should_run(self) -> bool:
    if not self.when:
      return True
    conditional = '{%% if %s %%}True{%% else %%}False{%% endif %%}' % self.when
    return Template(conditional).render(**self._cfg.rc.jsonnet.env) == 'True'
  
  def _verify_digest(self):
    if self._cfg.rc.check_hashes and (self.hash or self.check_hash) and self.hash != self.content_digest:
      raise RuntimeError("digest mismatch, got {}, expected {}. Need to run kasane update?".format(self.content_digest, self.hash))

class InjectLayer(Layer):
  @property
  def is_remote(self) -> bool:
    return False

  def run(self, previous: List[Any]) -> Any:
    if self.name == 'istio':
      env = dict(**os.environ)
      if self._cfg.rc.kubeconfig:
        env['KUBECONFIG'] = self._cfg.rc.kubeconfig
      data = subprocess.check_output(['istioctl', 'kube-inject', '-f', '-', '--includeIPRanges=10.200.0.0/16'], universal_newlines=True, input=dump_yaml(previous), env=env)
      data = list(yaml.load_all(data))
      data = list(filter(None.__ne__, data))
    else:
      raise RuntimeError("don't know how to run {} tag".format(self.name))
    
    return data

RX_ENV = re.compile(r'\$\{([^}]+)\}')

class DataLayer(Layer):
  def run(self, previous: List[Any]) -> Any:
    self._verify_digest()
    
    content = self.content

    if self.loader == 'yamlenv':
      def replace(m):
        key = m.group(1)
        val = self._cfg.rc.jsonnet.get_env(key)
        if val.find('\n') != -1:
          # if it contains newlines must force a string
          val = json.dumps(val)
        return val
      content = RX_ENV.sub(replace, content)

    data: List[Any] = list(yaml.load_all(content))
    data = list(filter(None.__ne__, data))
    data = previous + data
    return data

class JsonnetLayer(Layer):
  def run(self, previous: List[Any]) -> Any:
    self._verify_digest()

    return self._cfg.rc.jsonnet.evaluate_snippet(self.name, self.content, tla_codes=dict(layers=json.dumps(previous)))

def get_config(path: str, rc: RuntimeConfig) -> Config:
  cfgpath = os.path.join(path, CONFIG_NAME)
  lockpath = os.path.join(path, LOCKFILE_NAME)
  if not os.path.isfile(cfgpath):
    raise RuntimeError("config {} isn't found at {} or is not a file".format(CONFIG_NAME, cfgpath))  

  cfg = yaml.load(open(cfgpath))
  lock = None

  if os.path.isfile(lockpath):
    lock = yaml.load(open(lockpath))
  
  if not lock:
    lock = {}

  if not 'layers' in lock:
    lock['layers'] = []
  
  return Config(path, cfg, lock, rc)

def dump_yaml(data):
  s = StringIO()
  yaml.dump_all(data, s)
  return s.getvalue()
