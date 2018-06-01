Feature: cli
    Command-line interface to kasane

Scenario: Showing a simple Kasanefile
    Given Kasanefile:
        layers:
        - test.yaml
    When a layer named 'test.yaml' contains:
        ---
        kind: FakeObject
        metadata:
          name: fake
    And user runs kasane show
    Then kasane outputs:
        kind: FakeObject
        metadata:
          name: fake

Scenario: Showing a remote layer fails when the layer isn't vendored
    Given Kasanefile:
        layers:
        - https://raw.githubusercontent.com/google/kasane/master/examples/01-simple-layers/second.yaml
    When user runs kasane show
    Then kasane fails with a message 'layer https://raw.githubusercontent.com/google/kasane/master/examples/01-simple-layers/second.yaml isn't vendored yet. Run kasane update.'

Scenario: Showing a remote layer works
    Given Kasanefile:
        layers:
        - https://raw.githubusercontent.com/google/kasane/master/examples/01-simple-layers/second.yaml
    When user runs kasane update
    And user runs kasane show
    Then kasane outputs:
        kind: FakeObject
        metadata:
          name: fake3
