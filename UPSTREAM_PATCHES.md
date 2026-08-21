# Upstream Patch Ledger

This fork selectively adopts upstream maintenance changes. This ledger records
only the changes carried by this branch.

| Adopted change | Local files | Reason | Validation |
| --- | --- | --- | --- |
| [`astral-sh/setup-uv` v10.0.1](https://github.com/astral-sh/setup-uv/releases/tag/v10.0.1), as tested by [upstream PR #1501](https://github.com/basnijholt/adaptive-lighting/pull/1501) | `.github/workflows/docs.yml`, `.github/workflows/markdown-code-runner.yml`, `.github/workflows/install_dependencies/action.yml` | Pin the action to immutable commit `20cfd1bf945f4377ade1205e4dbc17946fc9a30d`; enable cache pruning explicitly to preserve v7 cleanup behavior. | `actionlint` on workflow files; `check-jsonschema` on the composite action; `./scripts/lint`; all fork PR checks before merge. |
| Pages actions v5 | `.github/workflows/docs.yml` | Adopt `actions/upload-pages-artifact@v5` and `actions/deploy-pages@v5` while preserving the PR upload guard and main-only deploy guard. | `actionlint`; `./scripts/lint`; Documentation check before merge; Pages deployment after merge. |
