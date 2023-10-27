"""Support for Volvo AAOS binary sensors."""

from __future__ import annotations

from collections.abc import Callable, Awaitable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.button import (
    ButtonDeviceClass,
    ButtonEntity,
    ButtonEntityDescription,
)

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, LOGGER

from .coordinator import VolvoData, VolvoUpdateCoordinator

from .entity import VolvoEntity
from .volvo import ConnectedVehicle

@dataclass
class VolvoButtonEntityMixin:
    """Mixin values for Volvo binary sensor entities."""

    button_fn: Callable[[ConnectedVehicle], Awaitable[Any]]

@dataclass
class VolvoButtonEntityDescription(ButtonEntityDescription, VolvoButtonEntityMixin):
    """Class describing Volvo AAOS binary sensor entities"""

BUTTONS = [
    VolvoButtonEntityDescription(
        key="start_cliamte",
        name="Start climate",
        button_fn=lambda client: client.set_climate_start(),
    ),
    VolvoButtonEntityDescription(
        key="stop_cliamte",
        name="Stop climate",
        button_fn=lambda client: client.set_climate_stop(),
    ),

]

async def async_setup_entry(
        hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Setup Volvo binary sensors from config entry."""

    volvo_coordinator: VolvoUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        VolvoButtonEntity(
            coordinator=volvo_coordinator,
            description=description
        )
        for description in BUTTONS
    )

class VolvoButtonEntity(VolvoEntity,ButtonEntity):
    """Representation of a Volvo binary sensor."""

    entity_description: VolvoButtonEntityDescription

    def __init__(self, coordinator: VolvoUpdateCoordinator, description: VolvoButtonEntityDescription) -> None:
        """Initiate Volvo binary sensor."""
        super().__init__(coordinator)

        self.entity_description = description
        self._attr_unique_id = f"{description.key}"

    async def async_press(self) -> None:
        self.coordinator.set_tokens()
        await self.entity_description.button_fn(self.coordinator.connected_vehicle)