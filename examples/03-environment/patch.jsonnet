local env(name) = std.native("env")(name);

function (layers)

[
  layers[0] {
    config+: {
      jsonnetEnv: env('OTHER_VALUE'),
    },
  }
]
