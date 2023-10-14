"""Base entities for Volvo AAOS"""

from __future__ import annotations

from homeassistant.const import CONF_NAME
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import VolvoUpdateCoordinator

class VolvoEntity(CoordinatorEntity[VolvoUpdateCoordinator]):
    """Defines a Volvo AAOS entity."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: VolvoUpdateCoordinator) -> None:
        """Initialize Volvo AAOS entity."""
        super().__init__(coordinator)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.config_entry.data[CONF_NAME])},
            manufacturer="Volvo"
        )
