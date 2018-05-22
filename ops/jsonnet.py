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

import json
import os

import _jsonnet

class UndefinedEnvError(RuntimeError):
  def __init__(self, var):
    super().__init__('unresolved environment variable ' + var)
    self.var = var

class Jsonnet(object):
  def __init__(self, search_dirs, env):
    self.ignore_env = False
    self.env = env
    self._search_dirs = search_dirs
    self._native_callbacks = {
      'env': (('name', ), self.get_env),
    }
  
  def get_env(self, name):
    e = self.env.get(name)
    if e is not None:
      return e
    if self.ignore_env:
      return 'UNRESOLVED_ENV_VAR__' + name
    raise UndefinedEnvError(name)

  def evaluate(self, *args, **kwargs):
    kwargs['import_callback'] = self._import_callback
    kwargs['native_callbacks'] = self._native_callbacks
    return json.loads(_jsonnet.evaluate_file(*args, **kwargs))

  def evaluate_snippet(self, *args, **kwargs):
    kwargs['import_callback'] = self._import_callback
    kwargs['native_callbacks'] = self._native_callbacks
    return json.loads(_jsonnet.evaluate_snippet(*args, **kwargs))

  def _import_callback(self, localdir, rel):
    if not rel:
      raise RuntimeError('Got invalid filename (empty string).')

    if rel[-1] == '/':
      raise RuntimeError('Attempted to import a directory')

    if rel[0] == '.':
      full_path, content = self._try_path(os.path.join(localdir, rel))
      if content:
        return full_path, content

    if rel[0] == '/':
      full_path, content = self._try_path(rel)
      if content:
        return full_path, content

    full_path, content = self._try_path(os.path.join(localdir, rel))
    if content:
      return full_path, content

    for d in self._search_dirs:
      d = os.path.abspath(d)
      full_path, content = self._try_path(os.path.join(d, rel))
      if content:
        return full_path, content

    raise RuntimeError('File not found')

  def _try_path(self, full_path):
    if not os.path.isfile(full_path):
      return full_path, None
    with open(full_path) as f:
      return full_path, f.read()

