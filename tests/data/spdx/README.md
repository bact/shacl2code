# SPDX 3 model fixtures

Vendored, pinned snapshots of the SPDX 3 ontology, used by `tests/test_spdx.py`
to exercise code generation against a real, large model. They are committed
rather than downloaded at test time, so the tests are deterministic and
offline.

## Contents

| Directory  | Version                | File                                  | SHA-256                                                            |
|------------|------------------------|---------------------------------------|--------------------------------------------------------------------|
| `3.0.1/`   | SPDX 3.0.1             | `spdx-model.ttl`                      | `30ebb4af2d70a9809044ef46f44cc3dc5125226d70f818a50ed2e1d5f404c593` |
|            |                        | `spdx-json-serialize-annotations.ttl` | `c6a54b51230eb2bf3b31302546af201f303e0b7931c1db404d7f5b72b6f863e6` |
|            |                        | `spdx-context.jsonld`                 | `c72b0928f094c83e5c127784edb1ebca2af74a104fcacc007c332b23cbc788bd` |
| `3.1-dev/` | SPDX 3.1-RC1 snapshot  | `spdx-model.ttl`                      | `711b44efb7bcefc05ec752cd096b8fbd3d2d487e5143aaed12025615ee840949` |
|            |                        | `spdx-json-serialize-annotations.ttl` | `006ddcb8a5c04bfc4dc771df11af5508df8536ada44eebcf69a36c0b18173331` |
|            |                        | `spdx-context.jsonld`                 | `e57db84c9418d9ff88ff0d1901a893a4377653ea69155ad94ce6e41441f3f178` |

Sources, fetched 2026-08-28:

- 3.0.1:
  - <https://spdx.org/rdf/3.0.1/spdx-model.ttl>
  - <https://spdx.org/rdf/3.0.1/spdx-json-serialize-annotations.ttl>
  - <https://spdx.org/rdf/3.0.1/spdx-context.jsonld>
- 3.1-RC1 (the `3.1` URLs are not version-pinned, so the SHA-256s above are
  authoritative for what is vendored):
  - <https://spdx.org/rdf/3.1/spdx-model.ttl>
  - <https://spdx.org/rdf/3.1/spdx-json-serialize-annotations.ttl>
  - <https://spdx.org/rdf/3.1/spdx-context.jsonld>

The 3.1 snapshot may differ from other files called "3.1" elsewhere (e.g. the
`spdx-python-model` project bundles a different one).

Check a file with `shasum -a 256 -c`, e.g. from this directory:

```shell
echo "30ebb4af2d70a9809044ef46f44cc3dc5125226d70f818a50ed2e1d5f404c593  3.0.1/spdx-model.ttl" | shasum -a 256 -c
```

## Distribution

These files are test data kept in the git repository only; nothing under
`tests/data/spdx/` is included in the sdist or wheel (see
`[tool.hatch.build.targets.sdist]` in `pyproject.toml`).

## License

The SPDX model is developed in the
[spdx/spdx-3-model](https://github.com/spdx/spdx-3-model) project and
published by the SPDX Working Group under the
[Community Specification License 1.0](https://github.com/spdx/spdx-3-model/blob/develop/License.md).
