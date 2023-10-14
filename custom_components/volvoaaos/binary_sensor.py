"""Support for Volvo AAOS binary sensors."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, LOGGER

from .coordinator import VolvoData, VolvoUpdateCoordinator

from .entity import VolvoEntity

@dataclass
class VolvoBinarySensorEntityMixin:
    """Mixin values for Volvo binary sensor entities."""

    value_fn: Callable[[VolvoData], float]
    attr_name: str | None
    attr_fn: Callable[[VolvoData], float | None]

@dataclass
class VolvoBinarySensorEntityDescription(BinarySensorEntityDescription, VolvoBinarySensorEntityMixin):
    """Class describing Volvo AAOS binary sensor entities"""

BINARY_SENSORS = [
    VolvoBinarySensorEntityDescription(
        key="locked_state",
        name="Lock state",
        device_class=BinarySensorDeviceClass.LOCK,
        value_fn=lambda x: False if x.connected_vehicle_door_status.data.car_locked.value == 'LOCKED' else True,
        attr_name=None,
        attr_fn=None
    )
]

async def async_setup_entry(
        hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Setup Volvo binary sensors from config entry."""

    volvo_coordinator: VolvoUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        VolvoBinarySensorEntity(
            coordinator=volvo_coordinator,
            description=description
        )
        for description in BINARY_SENSORS
    )

class VolvoBinarySensorEntity(VolvoEntity,BinarySensorEntity):
    """Representation of a Volvo binary sensor."""

    entity_description: VolvoBinarySensorEntityDescription

    def __init__(self, coordinator: VolvoUpdateCoordinator, description: VolvoBinarySensorEntityDescription) -> None:
        """Initiate Volvo binary sensor."""
        super().__init__(coordinator)

        self.entity_description = description
        self._attr_unique_id = f"{description.key}"

    @property
    def is_on(self) -> bool:
        """Return binary sensor value."""
        return self.entity_description.value_fn(self.coordinator.data)