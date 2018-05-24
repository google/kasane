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


import os
import json
from typing import List

import click

from kasane import ops

@click.group()
@click.option('-p', '--path')
@click.option('-l', '--lib')
@click.option('-c', '--config')
@click.option('-e', '--env', multiple=True)
@click.pass_context
def cli(ctx, path: str, lib: str, config: str, env: List[str]):
  if not path:
    path = os.path.curdir
  if not lib:
    lib = ''
  ctx.obj['path'] = path
  ctx.obj['config'] = config
  collectedenv = os.getenv('KASANE_JSONNET_ENV', '{ }')
  collectedenv = json.loads(collectedenv)
  for kv in env:
    k, v = kv.split('=', 1)
    collectedenv[k] = v
  ctx.obj['env'] = collectedenv
  ctx.obj['j'] = ops.Jsonnet([path] + [lib], collectedenv)
  ctx.obj['rc'] = ops.RuntimeConfig(check_hashes=True, jsonnet=ctx.obj['j'], kubeconfig=ctx.obj['config'])

@cli.add_command
@click.command()
@click.pass_context
@click.option('-r', '--raw/--highlight', default=False)
@click.option('--validate-signatures/--no-validate-signatures', default=True)
@click.option('-k')
@click.option('--ignore-env/--no-ignore-env', default=True)
def show(ctx, raw: bool, validate_signatures: bool, k: str, ignore_env: bool) -> None:
  '''prints the compiled bundle'''

  if ignore_env:
    ctx.obj['j'].ignore_env = True
  
  ctx.obj['rc'] = ops.common.RuntimeConfig(
    check_hashes=validate_signatures,
    jsonnet=ctx.obj['rc'].jsonnet,
    kubeconfig=ctx.obj['rc'].kubeconfig)
  ops.show(ctx.obj['path'], ctx.obj['rc'], not raw, k)

@cli.add_command
@click.command()
@click.pass_context
def apply(ctx) -> None:
  '''applies the compiled bundle'''
  
  try:
    ops.apply(ctx.obj['path'], ctx.obj['rc'])
  except ops.jsonnet.UndefinedEnvError as e:
    print(e)
    print('known env:', ', '.join(ctx.obj['env'].keys()))
    exit(1)

@cli.add_command
@click.command()
@click.option('--lock-all/--lock-remote-only', default=False)
@click.pass_context
def update(ctx, lock_all: bool) -> None:
  '''updates the bundle'''
  
  ops.update(ctx.obj['path'], ctx.obj['rc'], lock_all)

def main():
  cli(obj={})
