# Changelog

All notable changes to **florianhorner/adaptive-lighting** (a community fork of [basnijholt/adaptive-lighting](https://github.com/basnijholt/adaptive-lighting)) are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

This is a human-authored fork narrative. Per-release auto-drafted notes live in GitHub Releases.

## [Unreleased]

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
- Built on [basnijholt/adaptive-lighting](https://github.com/basnijholt/adaptive-lighting). The per-axis engine (`LightControlAttributes` IntFlag in `adaptation_utils.py`) and per-axis manual-control state machine already lived upstream — this release surfaces that capability via UI and entity attributes.
- Thanks to the upstream PR authors whose work on the manual-control mechanism made this surface change small.

### Switching back to upstream
If this fork misbehaves, switch back to `basnijholt/adaptive-lighting` via HACS — your existing automations work without changes. The fork stays additive; nothing in your config needs to flip.

---

[Unreleased]: https://github.com/florianhorner/adaptive-lighting/compare/v1.31.0...HEAD
