Feature: layers

Scenario: Combining two layers together
    Given Kasanefile:
        layers:
        - test.yaml
        - test2.yaml
    When a layer named 'test.yaml' contains:
        ---
        kind: FakeObject
        metadata:
          name: fake
    And a layer named 'test2.yaml' contains:
        ---
        kind: FakeObject
        metadata:
          name: fake2
    And user runs kasane show
    Then kasane outputs:
        kind: FakeObject
        metadata:
          name: fake
        ---
        kind: FakeObject
        metadata:
          name: fake2

Scenario: Using yamlenv loader substitutes ${ENV} with env values
    Given Kasanefile:
        layers:
        - name: test.yaml
          loader: yamlenv
        environment:
          TEST: case
    When a layer named 'test.yaml' contains:
        ---
        kind: FakeObject
        metadata:
          name: ${TEST}
    And user runs kasane show
    Then kasane outputs:
        kind: FakeObject
        metadata:
          name: case
