# coding=utf-8
"""cli feature tests."""

from pytest_bdd import (parsers, scenario, given, when, then)

from kasane import cmd


@scenario('cli.feature', "Showing a simple Kasanefile")
def test_showing_a_simple_kasanefile():
  pass

@scenario('cli.feature', "Showing a remote layer fails when the layer isn't vendored")
def test_fetiching_remote_layer_fails_when_not_vendored():
  pass

@scenario('cli.feature', "Showing a remote layer works")
def test_showing_remote_layer_works():
  pass

@scenario('layers.feature', "Combining two layers together")
def test_combining_two_layers_together():
  pass

@scenario('layers.feature', "Using yamlenv loader substitutes ${ENV} with env values")
def test_yamlenv_loader():
  pass

###

@given(parsers.parse("Kasanefile:\n{text}"))
def kasanefile(tmpdir, text):
  tmpdir.join('Kasanefile').write(text)
  return {'output': None}

###

@when(parsers.parse("a layer named '{name}' contains:\n{text}"))
def named_layer(tmpdir, name, text):
  tmpdir.join(name).write(text)

@when(parsers.parse("user runs kasane {action}"))
def run_kasane_action(kasanefile, cli_runner, tmpdir, action):
  try:
    old_dir = tmpdir.chdir()

    # TODO(farcaller): fix the highlight breakage
    if action == 'show':
      args = ['-r']
    else:
      args = []

    kasanefile['output'] = cli_runner.invoke(cmd.cli, [action, *args])
  except:
    raise
  finally:
    old_dir.chdir()

###

@then(parsers.parse("kasane outputs:\n{text}"))
def kasane_outputs(kasanefile, text):
  assert kasanefile['output'].output == text + '\n'

@then(parsers.parse("kasane fails with a message '{message}'"))
def kasane_fails_with_message(kasanefile, message):
  assert kasanefile['output'].exit_code == 1
  assert kasanefile['output'].output == message + '\n'
