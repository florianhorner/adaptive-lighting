# Changelog

All notable changes to **florianhorner/adaptive-lighting-fork** (a community fork of [basnijholt/adaptive-lighting](https://github.com/basnijholt/adaptive-lighting)) are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

This is a human-authored fork narrative. Per-release auto-drafted notes live in GitHub Releases.

## [Unreleased]

## [1.32.0-beta.2] - 2026-07-24

### Fixed

- Replaced Home Assistant's deprecated `get_astral_location` path with Astral `Observer` calculations. Home Assistant 2026.7+ uses `get_astral_observer`; the fork retains an equivalent fallback for its 2024.12 minimum.
- Recognize direct and Home Assistant Light Group member `light.turn_on` calls that legitimately reuse an earlier turn-off context. The check is bounded between the recorded off and on state changes, so stale service events and polling artifacts remain blocked.

### Changed

- Updated the required latest-stable CI leg to Home Assistant `2026.7.4` on Python `3.14.2`; `2024.12.5` remains the required minimum and `dev` remains advisory.
- Updated the Home Assistant test harness for modern template lights, `requirements_all.txt`, `aiohasupervisor`, and service-translation validation.
- Added regression coverage for Astral calculations, observer compatibility across the minimum/current HA legs, direct/member group turn-ons, stale events, polling artifacts, and the event-bus group path.
- Preserved the fork surfaces unchanged: the four-option manual-control selector, per-axis attributes and legacy union, warn-once diagnostics, progressive configuration, diagnostic sensors, group expansion, and Lightener handling.

### Upstream v1.31 provenance

- **Inherited:** upstream [`6cebe14`](https://github.com/basnijholt/adaptive-lighting/commit/6cebe14a69bf0ea19efeaf3ed5c20e5396087216) / [#1426](https://github.com/basnijholt/adaptive-lighting/pull/1426), which merges `last_service_data` across split adaptation calls, is the exact shared ancestor of beta.1 and upstream v1.31.0.
- **Already equivalent:** the fork already carried the macOS dependency setup fix from [#1463](https://github.com/basnijholt/adaptive-lighting/pull/1463) and the reduced warning payload from [#1434](https://github.com/basnijholt/adaptive-lighting/pull/1434).
- **Newly ported:** the runtime and test behavior from [#1482](https://github.com/basnijholt/adaptive-lighting/pull/1482) and [#1483](https://github.com/basnijholt/adaptive-lighting/pull/1483).
- **Intentionally excluded:** upstream's `v1.31.0` manifest bump and unrelated action/deployment churn. Releases in this fork are tag-driven, and the release workflow stamps the fork version into the ZIP without merging upstream wholesale.

## [1.32.0-beta.1] - 2026-04-26

### Added
- `extra_state_attributes.manual_control_brightness` and `manual_control_color` — per-axis sibling lists exposing which lights have brightness vs color manually controlled. The legacy `manual_control` flat list is preserved as union semantics ("any axis locked") for full backwards compatibility with existing user automations.
- 4-option `adaptive_lighting.set_manual_control` service selector. The HA service-picker UI now shows human-labeled options (Pause both / Resume adaptation / Pause brightness only / Pause color only) instead of a boolean toggle. The schema already accepted axis strings (`"brightness"`, `"color"`); this release surfaces them in the UI.
- Warn-once log signal when adaptation is silently bypassed because no light feature intersects the currently-adapting axes (typical case: brightness locked on a color-only bulb). The first occurrence per light fires at WARNING level with the affected entity, features, and adapt flags. Subsequent skips for the same light stay at debug level. The warning re-arms when the switch toggles off-and-on so a configuration change between off and on produces a fresh signal.

### Changed
- `services.set_manual_control.fields.manual_control` description rewritten from boolean-only ("add/remove") to axis-aware ("pause both / brightness / color / resume"). The `update-services.py` and `update-strings.py` regeneration cascade auto-updates `README.md`, `docs/configuration.md`, and `docs/services.md`.

### Notes for upgrade from 1.31.x
- Existing automations reading `state_attributes.manual_control` continue to work — the flat list is preserved with union semantics.
- New automations can read `manual_control_brightness` and `manual_control_color` for axis-aware behavior.
- Existing `set_manual_control` calls with `manual_control: true` or `false` continue to work unchanged. The schema is unchanged; only the picker is now richer.
- Non-English service description and selector option labels ship English-only this cycle. Weblate translation sync will catch up locales asynchronously. HA falls back to English option labels for missing locale keys.

### Attribution
- Branched from upstream commit [`6cebe14`](https://github.com/basnijholt/adaptive-lighting/commit/6cebe14a69bf0ea19efeaf3ed5c20e5396087216), before the final upstream `v1.31.0` tag. The original beta.1 tag annotation's “Built on v1.31.0” wording was inaccurate.
- The per-axis engine (`LightControlAttributes` IntFlag in `adaptation_utils.py`) and per-axis manual-control state machine already lived upstream — this release surfaces that capability via UI and entity attributes.
- Thanks to the upstream PR authors whose work on the manual-control mechanism made this surface change small.

### Switching back to upstream

If this fork misbehaves, switch back to `basnijholt/adaptive-lighting` via HACS — your existing automations work without changes. The fork stays additive; nothing in your config needs to flip.

---

[Unreleased]: https://github.com/florianhorner/adaptive-lighting-fork/compare/v1.32.0-beta.2...HEAD
[1.32.0-beta.2]: https://github.com/florianhorner/adaptive-lighting-fork/compare/v1.32.0-beta.1...v1.32.0-beta.2
[1.32.0-beta.1]: https://github.com/florianhorner/adaptive-lighting-fork/releases/tag/v1.32.0-beta.1
