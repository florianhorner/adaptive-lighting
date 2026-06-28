# Upstream Patch Ledger

This fork intentionally does not merge upstream wholesale. Use this ledger to
track upstream fixes that were ported, adapted, skipped, or deferred.

| Upstream commit/PR | Local files changed | Intentionally skipped files | Reason | Validation | Last checked | Owner |
|---|---|---|---|---|---|---|
| `c4b8e28` / upstream CI restore | `.github/workflows/pytest.yaml`, `scripts/setup-dependencies`, `test_dependencies.py`, `tests/test_test_dependencies.py`, `tests/test_switch.py`, `custom_components/adaptive_lighting/translations/*.json` | `custom_components/adaptive_lighting/config_flow.py`, `scripts/update-test-matrix.py`, description placeholder plumbing | Port only HA Core dependency/test compatibility while preserving fork config-flow UX and right-sized CI. Non-English translations only drop the stale raw upstream simulator URL sentence already absent from canonical English strings. `tests/test_switch.py` changes are HA 2026.6 test-harness compatibility only. | `./scripts/test`; `pre-commit run --all-files`; `./scripts/update-generated-content` | 2026-06-28 | Florian |
| `17e43e0` / setup-uv v8 | None | `.github/workflows/install_dependencies/action.yml`, `.github/workflows/docs.yml`, `.github/workflows/markdown-code-runner.yml` | Deferred because `astral-sh/setup-uv@v8` was not resolvable by GitHub Actions on 2026-06-28. Keep the fork on the existing resolvable `v7` action until upstream or the Marketplace exposes `v8`. | GitHub Actions initially failed to resolve `astral-sh/setup-uv@v8`; recheck after reverting to `v7` | 2026-06-28 | Florian |
| `c8c31be` / upload Pages artifact v5 | `.github/workflows/docs.yml` | None | Update existing docs workflow action version while preserving PR artifact guard | GitHub Actions after PR push | 2026-06-28 | Florian |
| `cb4eb7e` / deploy Pages v5 | `.github/workflows/docs.yml` | None | Update existing docs deploy action version while preserving main-only deploy guard | GitHub Actions after PR push | 2026-06-28 | Florian |
| Upstream PR #1460 | None in this branch | Runtime adaptation files | Keep this fork compatibility branch free of timing, transition, and adaptation behavior changes | Maintainer nudge only; separate upstream PR remains open | 2026-06-28 | Florian |
