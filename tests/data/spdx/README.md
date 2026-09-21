# SPDX 3 model fixtures

Vendored, pinned snapshots of the SPDX 3 ontology, used by the cross-version
Protocol test harness to exercise codegen against a real, large-scale model
that embeds its version number in every class IRI. Fetched once and
committed rather than downloaded at test time, so the tests are
deterministic and offline.

## Contents

| Directory  | Version                | File                                | SHA-256                                                           |
|------------|-------------------------|--------------------------------------|--------------------------------------------------------------------|
| `3.0.1/`   | SPDX 3.0.1 (stable)     | `spdx-model.ttl`                     | `30ebb4af2d70a9809044ef46f44cc3dc5125226d70f818a50ed2e1d5f404c593` |
|            |                          | `spdx-json-serialize-annotations.ttl`| `c6a54b51230eb2bf3b31302546af201f303e0b7931c1db404d7f5b72b6f863e6` |
|            |                          | `spdx-context.jsonld`                | `c72b0928f094c83e5c127784edb1ebca2af74a104fcacc007c332b23cbc788bd` |
| `3.1-dev/` | SPDX 3.1-RC1 (created 2026-01-23) | `spdx-model.ttl`           | `711b44efb7bcefc05ec752cd096b8fbd3d2d487e5143aaed12025615ee840949` |
|            |                          | `spdx-json-serialize-annotations.ttl`| `006ddcb8a5c04bfc4dc771df11af5508df8536ada44eebcf69a36c0b18173331` |
|            |                          | `spdx-context.jsonld`                | `e57db84c9418d9ff88ff0d1901a893a4377653ea69155ad94ce6e41441f3f178` |

Source URLs (these point at whatever SPDX considers "3.0"/"3.1" *right now*
-- moving targets, not pinned snapshots -- so the SHA-256s above, not the
URLs, are authoritative for what's actually vendored here):

- <https://spdx.org/rdf/3.0/spdx-model.ttl>
- <https://spdx.org/rdf/3.0/spdx-json-serialize-annotations.ttl>
- <https://spdx.org/rdf/3.0/spdx-context.jsonld>
- <https://spdx.org/rdf/3.1/spdx-model.ttl>
- <https://spdx.org/rdf/3.1/spdx-json-serialize-annotations.ttl>
- <https://spdx.org/rdf/3.1/spdx-context.jsonld>

Fetched: 2026-08-28.

The 3.1 snapshot is specifically RC1 as published on the date above, and may
differ from other files also called "3.1" circulating elsewhere (e.g. the
`spdx-python-model` project bundles a different 3.1 snapshot) -- acceptance
results measured against this fixture apply to this snapshot, not to "SPDX
3.1" as a whole.

Verify a file hasn't drifted with `shasum -a 256 -c`, e.g. from this
directory:

```shell
echo "30ebb4af2d70a9809044ef46f44cc3dc5125226d70f818a50ed2e1d5f404c593  3.0.1/spdx-model.ttl" | shasum -a 256 -c
```

## Distribution

These files are vendored test data: they are kept in the git repository
only and are **not** redistributed in the project's sdist or wheel (see
`[tool.hatch.build.targets.sdist]` in `pyproject.toml`).

## License

These files are from the [spdx/spdx-3-model](https://github.com/spdx/spdx-3-model)
repository, published by the SPDX Working Group under the
[Community Specification License 1.0](https://github.com/spdx/spdx-3-model/blob/develop/License.md).
