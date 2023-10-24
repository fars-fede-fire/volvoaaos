"""Support for Volvo AAOS device tracker"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.device_tracker import(
    SourceType, TrackerEntity
)

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, LOGGER

from .coordinator import VolvoData, VolvoUpdateCoordinator

from .entity import VolvoEntity

@dataclass
class VolvoDeviceTrackerEntityMixin:
    """Mixin values for Volvo device tracker entities."""
    key="location"
    name=None
    longtitude_fn: Callable[[VolvoData], float]
    latitude_fn: Callable[[VolvoData], float]

@dataclass
class VolvoDeviceTrackerEntityDescription(VolvoDeviceTrackerEntityMixin, TrackerEntity):
    """Class describing Volvo AAOS device tracker entities"""


DEVICE_TRACKER = [
    VolvoDeviceTrackerEntityDescription(
        longtitude_fn=lambda x: x.location.data.geometry.coordinates[0],
        latitude_fn=lambda x: x.location.data.geometry.coordinates[1]
    )
]

async def async_setup_entry(
        hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Setup Volvo device tracker from config entry."""

    volvo_coordinator: VolvoUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        VolvoDeviceTrackerEntity(
            coordinator=volvo_coordinator,
            description=description
        )
        for description in DEVICE_TRACKER
    )

class VolvoDeviceTrackerEntity(VolvoEntity, TrackerEntity):
    """Representation of a Volvo device tracker."""

    entity_description: VolvoDeviceTrackerEntityDescription

    def __init__(self, coordinator: VolvoUpdateCoordinator, description: VolvoDeviceTrackerEntityDescription) -> None:
        """Initiate Volvo device tracker."""
        super().__init__(coordinator)

        self.entity_description = description
        self._attr_unique_id = f"{description.key}"

    @property
    def latitude(self) -> float | None:
        return self.entity_description.latitude_fn(self.coordinator.data)

    @property
    def longitude(self) -> float | None:
        return self.entity_description.longtitude_fn(self.coordinator.data)

    @property
    def source_type(self) -> SourceType | str:
        return SourceType.GPS

