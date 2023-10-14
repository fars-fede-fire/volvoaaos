"""Support for Volvo AAOS climate."""
"""No endpoint exposed to show if climate is on or off"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.climate import(
    ClimateEntity,
    ClimateEntityDescription,
    ClimateEntityFeature)

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, LOGGER

from .coordinator import VolvoData, VolvoUpdateCoordinator

from .entity import VolvoEntity


