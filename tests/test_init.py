"""Tests for Adaptive Lighting integration."""

from homeassistant.components import adaptive_lighting
from homeassistant.components.adaptive_lighting.const import (
    DEFAULT_NAME,
    UNDO_UPDATE_LISTENER,
)
from homeassistant.config_entries import ConfigEntryState
from homeassistant.const import CONF_NAME
from homeassistant.setup import async_setup_component

from tests.common import MockConfigEntry


async def test_setup_with_config(hass):
    """Test that we import the config and setup the integration."""
    config = {
        adaptive_lighting.DOMAIN: {
            adaptive_lighting.CONF_NAME: DEFAULT_NAME,
        },
    }
    assert await async_setup_component(hass, adaptive_lighting.DOMAIN, config)
    assert adaptive_lighting.DOMAIN in hass.data


async def test_successful_config_entry(hass):
    """Test that Adaptive Lighting is configured successfully."""
    entry = MockConfigEntry(
        domain=adaptive_lighting.DOMAIN,
        data={CONF_NAME: DEFAULT_NAME},
    )
    entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(entry.entry_id)

    assert entry.state == ConfigEntryState.LOADED

    assert UNDO_UPDATE_LISTENER in hass.data[adaptive_lighting.DOMAIN][entry.entry_id]


async def test_unload_entry(hass):
    """Test removing Adaptive Lighting."""
    entry = MockConfigEntry(
        domain=adaptive_lighting.DOMAIN,
        data={CONF_NAME: DEFAULT_NAME},
    )
    entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(entry.entry_id)

    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()

    assert entry.state == ConfigEntryState.NOT_LOADED
    assert adaptive_lighting.DOMAIN not in hass.data


# ---------------------------------------------------------------------------
# Tests for PR changes: PLATFORMS, removed sensor platform, removed constants
# ---------------------------------------------------------------------------


def test_platforms_switch_only():
    """Test that PLATFORMS contains only 'switch' after sensor platform removal.

    The PR removed the sensor platform (diagnostic status sensors) from PLATFORMS.
    """
    assert adaptive_lighting.PLATFORMS == ["switch"]
    assert "sensor" not in adaptive_lighting.PLATFORMS


async def test_sensor_platform_not_loaded(hass):
    """Test that the sensor platform is NOT set up after PR removes it.

    Before this PR, PLATFORMS included 'sensor'. After the PR, only 'switch'
    is in PLATFORMS. Verify that no sensor entities are created on setup.
    """
    entry = MockConfigEntry(
        domain=adaptive_lighting.DOMAIN,
        data={CONF_NAME: DEFAULT_NAME},
    )
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    sensor_entities = hass.states.async_entity_ids("sensor")
    al_sensors = [e for e in sensor_entities if "adaptive_lighting" in e]
    assert (
        al_sensors == []
    ), f"No adaptive_lighting sensor entities should exist, found: {al_sensors}"


async def test_no_attr_adaptive_lighting_manager_in_domain_data_on_entry_setup(hass):
    """Test that AdaptiveLightingManager is no longer set up in async_setup_entry.

    The PR moved manager initialization out of async_setup_entry and into the
    switch platform. Verify domain data structure after entry setup.
    """
    entry = MockConfigEntry(
        domain=adaptive_lighting.DOMAIN,
        data={CONF_NAME: DEFAULT_NAME},
    )
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    domain_data = hass.data.get(adaptive_lighting.DOMAIN, {})
    # entry_id sub-dict should exist and contain UNDO_UPDATE_LISTENER
    assert entry.entry_id in domain_data
    assert UNDO_UPDATE_LISTENER in domain_data[entry.entry_id]
