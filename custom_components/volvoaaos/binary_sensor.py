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
        key="front_left_door",
        name="Front left door",
        device_class=BinarySensorDeviceClass.DOOR,
        value_fn=lambda x: False if x.connected_vehicle_door_status.data.front_left_door_open.value == 'CLOSED' else True,
        attr_name=None,
        attr_fn=None
    ),
        VolvoBinarySensorEntityDescription(
        key="front_right_door",
        name="Front right door",
        device_class=BinarySensorDeviceClass.DOOR,
        value_fn=lambda x: False if x.connected_vehicle_door_status.data.front_right_door_open.value == 'CLOSED' else True,
        attr_name=None,
        attr_fn=None
    ),
        VolvoBinarySensorEntityDescription(
        key="rear_left_door",
        name="Rear left door",
        device_class=BinarySensorDeviceClass.DOOR,
        value_fn=lambda x: False if x.connected_vehicle_door_status.data.rear_left_door_open.value == 'CLOSED' else True,
        attr_name=None,
        attr_fn=None
    ),
        VolvoBinarySensorEntityDescription(
        key="rear_right_door",
        name="Rear right door",
        device_class=BinarySensorDeviceClass.DOOR,
        value_fn=lambda x: False if x.connected_vehicle_door_status.data.rear_right_door_open.value == 'CLOSED' else True,
        attr_name=None,
        attr_fn=None
    ),
    VolvoBinarySensorEntityDescription(
        key="hood",
        name="Hood",
        device_class=BinarySensorDeviceClass.DOOR,
        value_fn=lambda x: False if x.connected_vehicle_door_status.data.hood_open.value == 'CLOSED' else True,
        attr_name=None,
        attr_fn=None
    ),
    VolvoBinarySensorEntityDescription(
        key="tail_gate",
        name="Tail gate",
        device_class=BinarySensorDeviceClass.DOOR,
        value_fn=lambda x: False if x.connected_vehicle_door_status.data.tail_gate_open.value == 'CLOSED' else True,
        attr_name=None,
        attr_fn=None
    ),
    VolvoBinarySensorEntityDescription(
        key="tank_lid",
        name="Tank lid",
        device_class=BinarySensorDeviceClass.DOOR,
        value_fn=lambda x: False if x.connected_vehicle_door_status.data.tank_lid_open.value == 'CLOSED' else True,
        attr_name=None,
        attr_fn=None
    ),
    VolvoBinarySensorEntityDescription(
        key="front_left_window",
        name="Front left window",
        device_class=BinarySensorDeviceClass.WINDOW,
        value_fn=lambda x: False if x.connected_vehicle_window_status.data.front_left_window_open.value == 'CLOSED' else True,
        attr_name=None,
        attr_fn=None
    ),
    VolvoBinarySensorEntityDescription(
        key="front_right_window",
        name="Front right window",
        device_class=BinarySensorDeviceClass.WINDOW,
        value_fn=lambda x: False if x.connected_vehicle_window_status.data.front_right_window_open.value == 'CLOSED' else True,
        attr_name=None,
        attr_fn=None
    ),
    VolvoBinarySensorEntityDescription(
        key="rear_left_window",
        name="Rear left window",
        device_class=BinarySensorDeviceClass.WINDOW,
        value_fn=lambda x: False if x.connected_vehicle_window_status.data.rear_left_window_open.value == 'CLOSED' else True,
        attr_name=None,
        attr_fn=None
    ),
    VolvoBinarySensorEntityDescription(
        key="rear_right_window",
        name="Rear right window",
        device_class=BinarySensorDeviceClass.WINDOW,
        value_fn=lambda x: False if x.connected_vehicle_window_status.data.rear_right_window_open.value == 'CLOSED' else True,
        attr_name=None,
        attr_fn=None
    ),
    VolvoBinarySensorEntityDescription(
        key="sunroof",
        name="Sunroof",
        device_class=BinarySensorDeviceClass.WINDOW,
        value_fn=lambda x: False if x.connected_vehicle_window_status.data.sun_roof_open.value == 'CLOSED' else True,
        attr_name=None,
        attr_fn=None
    ),
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