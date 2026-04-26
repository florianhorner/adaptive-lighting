"""Tests for PR-specific changes in const.py and helpers.py.

Covers:
- Removal of STEP_OPTIONS, ROOM_PRESETS, CONF_ENABLE_DIAGNOSTIC_SENSORS,
  LightStatus, LightStatusInfo, STATUS_PRIORITY, SIGNAL_STATUS_UPDATED
- sleep_brightness validation changed from int_between(0, 100) to int_between(1, 100)
- expand_light_groups removed from helpers.py
"""

import pytest
import voluptuous as vol


# ---------------------------------------------------------------------------
# Removed constants / symbols from const.py
# ---------------------------------------------------------------------------


def test_step_options_removed_from_const():
    """Test that STEP_OPTIONS is no longer defined in const.py.

    It was used by the 5-step options wizard which was removed in this PR.
    """
    from homeassistant.components.adaptive_lighting import const  # noqa: PLC0415

    assert not hasattr(const, "STEP_OPTIONS"), (
        "STEP_OPTIONS should have been removed when the multi-step flow was dropped"
    )


def test_room_presets_removed_from_const():
    """Test that ROOM_PRESETS is no longer defined in const.py."""
    from homeassistant.components.adaptive_lighting import const  # noqa: PLC0415

    assert not hasattr(const, "ROOM_PRESETS"), (
        "ROOM_PRESETS should have been removed along with the multi-step flow"
    )


def test_conf_room_preset_removed_from_const():
    """Test that CONF_ROOM_PRESET is no longer defined in const.py."""
    from homeassistant.components.adaptive_lighting import const  # noqa: PLC0415

    assert not hasattr(const, "CONF_ROOM_PRESET"), (
        "CONF_ROOM_PRESET should have been removed"
    )


def test_conf_enable_diagnostic_sensors_removed_from_const():
    """Test that CONF_ENABLE_DIAGNOSTIC_SENSORS is no longer in const.py.

    Diagnostic status sensors were removed in this PR.
    """
    from homeassistant.components.adaptive_lighting import const  # noqa: PLC0415

    assert not hasattr(const, "CONF_ENABLE_DIAGNOSTIC_SENSORS"), (
        "CONF_ENABLE_DIAGNOSTIC_SENSORS should have been removed with sensor platform removal"
    )


def test_default_enable_diagnostic_sensors_removed_from_const():
    """Test that DEFAULT_ENABLE_DIAGNOSTIC_SENSORS is no longer in const.py."""
    from homeassistant.components.adaptive_lighting import const  # noqa: PLC0415

    assert not hasattr(const, "DEFAULT_ENABLE_DIAGNOSTIC_SENSORS"), (
        "DEFAULT_ENABLE_DIAGNOSTIC_SENSORS should have been removed"
    )


def test_light_status_removed_from_const():
    """Test that LightStatus enum is no longer defined in const.py."""
    from homeassistant.components.adaptive_lighting import const  # noqa: PLC0415

    assert not hasattr(const, "LightStatus"), (
        "LightStatus should have been removed with the sensor platform"
    )


def test_light_status_info_removed_from_const():
    """Test that LightStatusInfo dataclass is no longer defined in const.py."""
    from homeassistant.components.adaptive_lighting import const  # noqa: PLC0415

    assert not hasattr(const, "LightStatusInfo"), (
        "LightStatusInfo should have been removed with the sensor platform"
    )


def test_status_priority_removed_from_const():
    """Test that STATUS_PRIORITY dict is no longer defined in const.py."""
    from homeassistant.components.adaptive_lighting import const  # noqa: PLC0415

    assert not hasattr(const, "STATUS_PRIORITY"), (
        "STATUS_PRIORITY should have been removed with the sensor platform"
    )


def test_signal_status_updated_removed_from_const():
    """Test that SIGNAL_STATUS_UPDATED is no longer defined in const.py."""
    from homeassistant.components.adaptive_lighting import const  # noqa: PLC0415

    assert not hasattr(const, "SIGNAL_STATUS_UPDATED"), (
        "SIGNAL_STATUS_UPDATED should have been removed with the sensor platform"
    )


# ---------------------------------------------------------------------------
# sleep_brightness validation: now int_between(1, 100), was int_between(0, 100)
# ---------------------------------------------------------------------------


def test_sleep_brightness_not_in_validation_tuples_with_zero_minimum():
    """Test that sleep_brightness minimum is now 1, not 0.

    Find CONF_SLEEP_BRIGHTNESS in VALIDATION_TUPLES and verify the validator
    rejects 0 and accepts 1.
    """
    from homeassistant.components.adaptive_lighting.const import (  # noqa: PLC0415
        CONF_SLEEP_BRIGHTNESS,
        VALIDATION_TUPLES,
    )

    # Find the validator for sleep_brightness
    validator = None
    for name, _default, valid in VALIDATION_TUPLES:
        if name == CONF_SLEEP_BRIGHTNESS:
            validator = valid
            break

    assert validator is not None, "CONF_SLEEP_BRIGHTNESS not found in VALIDATION_TUPLES"

    # 0 must now be invalid (changed from int_between(0,100) to int_between(1,100))
    with pytest.raises((vol.Invalid, vol.MultipleInvalid)):
        validator(0)

    # 1 must be valid (minimum)
    assert validator(1) == 1

    # 100 must be valid (maximum)
    assert validator(100) == 100

    # 101 must be invalid (over maximum)
    with pytest.raises((vol.Invalid, vol.MultipleInvalid)):
        validator(101)


def test_sleep_brightness_default_is_one():
    """Test that the default for sleep_brightness is 1 (minimum valid value)."""
    from homeassistant.components.adaptive_lighting.const import (  # noqa: PLC0415
        CONF_SLEEP_BRIGHTNESS,
        DEFAULT_SLEEP_BRIGHTNESS,
        VALIDATION_TUPLES,
    )

    assert DEFAULT_SLEEP_BRIGHTNESS == 1

    # Also verify that the default appears in VALIDATION_TUPLES
    defaults = {name: default for name, default, _ in VALIDATION_TUPLES}
    assert defaults[CONF_SLEEP_BRIGHTNESS] == 1


def test_enable_diagnostic_sensors_not_in_validation_tuples():
    """Test that enable_diagnostic_sensors is not in VALIDATION_TUPLES.

    The option was removed in this PR along with the sensor platform.
    """
    from homeassistant.components.adaptive_lighting.const import (  # noqa: PLC0415
        VALIDATION_TUPLES,
    )

    names = {name for name, _, _ in VALIDATION_TUPLES}
    assert "enable_diagnostic_sensors" not in names, (
        "enable_diagnostic_sensors should have been removed from VALIDATION_TUPLES"
    )


# ---------------------------------------------------------------------------
# helpers.py: expand_light_groups removed
# ---------------------------------------------------------------------------


def test_expand_light_groups_removed_from_helpers():
    """Test that expand_light_groups is no longer importable from helpers.

    The function was removed from helpers.py in this PR because its logic was
    inlined into switch.py's _expand_light_groups function.
    """
    from homeassistant.components.adaptive_lighting import helpers  # noqa: PLC0415

    assert not hasattr(helpers, "expand_light_groups"), (
        "expand_light_groups should have been removed from helpers.py"
    )


def test_expand_light_groups_import_raises():
    """Test that importing expand_light_groups from helpers raises ImportError."""
    with pytest.raises((ImportError, AttributeError)):
        from homeassistant.components.adaptive_lighting.helpers import (  # noqa: PLC0415
            expand_light_groups,
        )

        # If the import somehow succeeded (e.g. future re-export), fail explicitly
        raise AssertionError(
            "expand_light_groups should not be importable from helpers"
        )


# ---------------------------------------------------------------------------
# switch.py: _expand_light_groups behavior (unit-tested without HA fixtures)
# ---------------------------------------------------------------------------


def test_is_light_group_detects_group_by_entity_id():
    """Test that _is_light_group identifies groups via entity_id attribute."""
    from unittest.mock import Mock  # noqa: PLC0415

    from homeassistant.components.adaptive_lighting.switch import (  # noqa: PLC0415
        _is_light_group,
    )
    from homeassistant.core import State  # noqa: PLC0415

    # A state with entity_id attribute and no is_hue_group flag → group
    group_state = State("light.group", "on", {"entity_id": ["light.a", "light.b"]})
    assert _is_light_group(group_state) is True

    # A state with entity_id attribute but is_hue_group=True → not a plain group
    hue_group_state = State(
        "light.hue_group",
        "on",
        {"entity_id": ["light.a"], "is_hue_group": True},
    )
    assert _is_light_group(hue_group_state) is False

    # A regular light (no entity_id attribute) → not a group
    regular_state = State("light.single", "on", {"brightness": 200})
    assert _is_light_group(regular_state) is False


# ---------------------------------------------------------------------------
# sensor.py: module should not exist (was deleted in this PR)
# ---------------------------------------------------------------------------


def test_sensor_module_deleted():
    """Test that sensor.py no longer exists as a module.

    The entire sensor.py file was deleted in this PR.
    """
    with pytest.raises((ImportError, ModuleNotFoundError)):
        import homeassistant.components.adaptive_lighting.sensor  # noqa: PLC0415, F401