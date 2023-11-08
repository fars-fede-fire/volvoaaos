"""Support for Volvo AAOS lock."""

from __future__ import annotations
from collections.abc import Callable, Awaitable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.lock import (
    LockEntity,
    LockEntityDescription,
    LockEntityFeature
)

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback


from .const import DOMAIN, LOGGER
from .coordinator import VolvoData, VolvoUpdateCoordinator
from .entity import VolvoEntity
from .volvo import ConnectedVehicle


@dataclass
class VolvoLockEntityMixin:
    """Mixin values for Volvo lock entities."""
    value_fn: Callable[[VolvoData], float]
    lock_fn: Callable[[ConnectedVehicle], Awaitable[Any]]
    unlock_fn: Callable[[ConnectedVehicle], Awaitable[Any]]

@dataclass
class VolvoLockEntityDescription(LockEntityDescription, VolvoLockEntityMixin):
    """Class describing Volvo lock entities."""

LOCKS = [
    VolvoLockEntityDescription(
        key="lock",
        name="Lock",
        value_fn=lambda x: True if x.connected_vehicle_door_status.data.central_lock.value == 'LOCKED' else False,
        lock_fn=lambda client: client.lock_car(),
        unlock_fn=lambda client: client.unlock_car(),
    )
]

async def async_setup_entry(
        hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Setup Volvo AAOS lock from config entry"""

    volvo_coordinator: VolvoUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        VolvoLockEntity(
            coordinator = volvo_coordinator,
            description=description
        )
        for description in LOCKS
    )

class VolvoLockEntity(VolvoEntity, LockEntity):
    """Representation of a Volvo lock."""

    entity_description: VolvoLockEntityDescription

    def __init__(self, coordinator: VolvoUpdateCoordinator, description: VolvoLockEntityDescription) -> None:
        super().__init__(coordinator)

        self.entity_description = description
        self._attr_unique_id = f"{description.key}"

    @property
    def is_locked(self) -> bool | None:
        return self.entity_description.value_fn(self.coordinator.data)

    async def async_lock(self, **kwargs: Any) -> None:
        """Lock"""
        self.coordinator.set_tokens()
        await self.entity_description.lock_fn(self.coordinator.connected_vehicle)
        await self.coordinator.update_coordinator_data(datetime=None)

    async def async_unlock(self, **kwargs: Any) -> None:
        """Unlock"""
        self.coordinator.set_tokens()
        await self.entity_description.unlock_fn(self.coordinator.connected_vehicle)
        await self.coordinator.update_coordinator_data(datetime=None)
