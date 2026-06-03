# Contributing

This is a personal, actively-maintained fork of
[basnijholt/adaptive-lighting](https://github.com/basnijholt/adaptive-lighting),
distributed as a **HACS custom repository**. This file captures the bits of the
workflow that aren't obvious from the code.

## Home Assistant versions

- **Minimum supported:** `2024.12.0` (declared in `hacs.json`; this is what HACS
  shows users).
- **CI tests** against three Home Assistant cores: the minimum (`2024.12.5`), the
  latest stable, and `dev`. The `dev` leg is **advisory** (`continue-on-error`) —
  it tracks an unstable upstream and is an early-warning signal, not a gate.
- Mid-range HA versions are intentionally not tested (acceptable trade for a solo
  fork). Bump the "latest stable" leg in `.github/workflows/pytest.yaml` by hand at
  release time.

## Running things locally

```bash
# Lint + format (mirrors the pre-commit CI check exactly)
./scripts/lint

# Tests — requires the Home Assistant core test harness once:
git clone --depth 1 https://github.com/home-assistant/core.git core
./scripts/setup-dependencies
./scripts/setup-symlinks
# then:
./scripts/test                       # full adaptive_lighting suite
./scripts/test -k test_manual_control -x   # extra pytest args pass through
```

- Formatting/linting is **ruff** (`ruff format` + `ruff check`); `.ruff.toml` is the
  single source of truth. There is no black.
- `Dockerfile` is optional local-dev tooling (runs the same suite in a container);
  it is not part of CI.

## Generated content

`services.yaml`, `strings.json`, and the English translation are generated from
`custom_components/adaptive_lighting/const.py`. After changing options/docstrings:

```bash
./scripts/update-generated-content
```

The `markdown-code-runner` PR check fails if these are out of date.

## Cutting a release

Releases are **tag-driven** — pushing a tag is the whole release:

```bash
git tag v1.2.3      # use -alpha / -beta / -rc / -dev suffixes for prereleases
git push origin v1.2.3
```

`release.yml` then stamps `manifest.json`'s `version` from the tag, zips
`custom_components/adaptive_lighting/`, and creates a GitHub Release with that zip
attached (HACS installs from this). Prerelease suffixes are auto-flagged so HACS
doesn't promote them to stable users. **Do not** hand-bump the version in normal
commits — the tag is the source of truth at release time.

`pyproject.toml`'s `version` is **not** stamped and is **not** published (no PyPI; it
isn't in the release zip) — it's a cosmetic dev-tooling marker that may lag the latest
tag (it isn't bumped per-release). Leave it alone; the tag-stamped `manifest.json` is the only version that
ships.

## CI gate

`main` requires these checks to be green before merge: `pre-commit`,
`verify / Verify PR proof block`, `validate_hacs`, `validate_hassfest`, and the two
stable `pytest` legs. PRs also need a `## Proof` block in the description (enforced
by `verify-claims`).
