"""Support for Volvo AAOS sensors."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfEnergy, PERCENTAGE, LENGTH_KILOMETERS, TIME_MINUTES
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback


from .const import DOMAIN, LOGGER

from .coordinator import VolvoData, VolvoUpdateCoordinator

from .entity import VolvoEntity

@dataclass
class VolvoEntityMixin:
    """Mixin values for Volvo entities."""

    value_fn: Callable[[VolvoData], float]
    attr_name: str | None
    attr_fn: Callable[[VolvoData], float | None]

@dataclass
class VolvoEntityDescription(SensorEntityDescription, VolvoEntityMixin):
    """Class describing Volvo AAOS sensor entities"""

SENSORS = [
    VolvoEntityDescription(
        key="battery_level",
        name="Battery Level",
        device_class=SensorDeviceClass.BATTERY,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
        value_fn=lambda x: x.energy.data.battery_charge_level.value if hasattr(x.energy.data, 'battery_charge_level') else None,
        attr_name=None,
        attr_fn=None,
    ),
    VolvoEntityDescription(
        key="electric_range",
        name="Electric range",
        device_class=SensorDeviceClass.DISTANCE,
        native_unit_of_measurement=LENGTH_KILOMETERS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
        value_fn=lambda x: x.energy.data.electric_range.value if hasattr(x.energy.data, 'electric_range') else None,
        attr_name=None,
        attr_fn=None,
    ),
    VolvoEntityDescription(
        key="estimated_charging_time",
        name="Estimated Charging Time",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=TIME_MINUTES,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
        value_fn=lambda x: x.energy.data.estimated_charging_time.value if hasattr(x.energy.data, 'estimated_charging_time') else None,
        attr_name=None,
        attr_fn=None,
    ),
    VolvoEntityDescription(
        key="charging_connection_status",
        name="Charging Connection Status",
        value_fn=lambda x: x.energy.data.charging_connection_status.value if hasattr(x.energy.data, 'charging_connection_status') else None,
        attr_name=None,
        attr_fn=None,
    ),
    VolvoEntityDescription(
        key="charging_system_status",
        name="Charging System Status",
        value_fn=lambda x: x.energy.data.charging_system_status.value if hasattr(x.energy.data, 'charging_system_status') else None,
        attr_name=None,
        attr_fn=None,
    )
]

async def async_setup_entry(
        hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Setup Volvo AAOS sensors from config entry"""
    volvo_coordinator: VolvoUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        VolvoSensorEntity(
            coordinator=volvo_coordinator,
            description=description
        )
        for description in SENSORS
    )

class VolvoSensorEntity(VolvoEntity, SensorEntity):
    """Representation of a Volvo AAOS sensor."""

    entity_description: VolvoEntityDescription

    def __init__(self, coordinator: VolvoUpdateCoordinator, description: VolvoEntityDescription) -> None:
        """Initiate Volvo AAOS sensor."""
        super().__init__(coordinator)

        self.entity_description = description
        self._attr_unique_id = f"{description.key}"

    @property
    def native_value(self):
        """Return sensor value."""
        return self.entity_description.value_fn(self.coordinator.data)