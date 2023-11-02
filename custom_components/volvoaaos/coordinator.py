"""Data update coordinator for Volvo AAOS"""

from dataclasses import dataclass

from datetime import timedelta, datetime

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ACCESS_TOKEN
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN, LOGGER, CONF_VCC_API_KEY, CONF_VIN, CONF_REFRESH_TOKEN, CONF_ALL_RECHARGE_AVAILABLE

from .models import RechargeModel, ConnectedVehicleModel, GetDoorModel, GetWindowModel, LocationModel, BatteryChargeLevelModel
from .volvo import Auth, Energy, ConnectedVehicle, Location

@dataclass
class VolvoData:
    """Volvo data stored in DataUpdateCoordinator"""

    energy: RechargeModel
    connected_vehicle_door_status: GetDoorModel
    connected_vehicle_window_status: GetWindowModel
    location: LocationModel

class VolvoUpdateCoordinator(DataUpdateCoordinator[VolvoData]):
    """Class to manage fetching data for Volvo AAOS."""

    config_entry = ConfigEntry

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize coordinator."""

        self.hass = hass
        self.config_entry = entry
        self.listeners = []
        self.session = async_get_clientsession(hass)
        self.energy = Energy(session=self.session)
        self.auth = Auth(session=self.session)
        self.connected_vehicle = ConnectedVehicle(session=self.session)
        self.location = Location(session=self.session)

        self.listeners.append(
            async_track_time_interval(self.hass, self.update_coordinator_data, timedelta(seconds=60))
        )

        self.listeners.append(
            async_track_time_interval(self.hass, self.update_access_token, timedelta(minutes=7))
        )

        super().__init__(
            hass,
            LOGGER,
            name=f"{DOMAIN}",
            update_interval=None,
            update_method=None
        )

    def set_tokens(self):
        self.energy.access_token = self.config_entry.data[CONF_ACCESS_TOKEN]
        self.energy.vcc_api_key = self.config_entry.data[CONF_VCC_API_KEY]
        self.energy.vin = self.config_entry.data[CONF_VIN]
        self.connected_vehicle.access_token = self.config_entry.data[CONF_ACCESS_TOKEN]
        self.connected_vehicle.vcc_api_key = self.config_entry.data[CONF_VCC_API_KEY]
        self.connected_vehicle.vin = self.config_entry.data[CONF_VIN]
        self.location.access_token = self.config_entry.data[CONF_ACCESS_TOKEN]
        self.location.vcc_api_key = self.config_entry.data[CONF_VCC_API_KEY]
        self.location.vin = self.config_entry.data[CONF_VIN]

    @callback
    async def update_coordinator_data(self, datetime):
        self.set_tokens()
        energy_data = await update_energy(energy=self.energy, all_recharge_available=self.config_entry.data[CONF_ALL_RECHARGE_AVAILABLE])
        connected_vehicle = await update_connected_vehicle(self.connected_vehicle)
        location = await update_location(self.location)
        self.async_set_updated_data(VolvoData(energy=energy_data, connected_vehicle_door_status=connected_vehicle['door_status'], connected_vehicle_window_status=connected_vehicle['window_status'], location=location))

    @callback
    async def update_access_token(self, datetime):
        auth_update = await self.auth.reauth(refresh_token=self.config_entry.data[CONF_REFRESH_TOKEN])
        new_data = {**self.config_entry.data, CONF_ACCESS_TOKEN: auth_update.access_token, CONF_REFRESH_TOKEN:auth_update.refresh_token}
        self.hass.config_entries.async_update_entry(self.config_entry, data=new_data)
        LOGGER.debug("Access and refresh token updated")


async def update_energy(energy: Energy, all_recharge_available: bool) -> RechargeModel | BatteryChargeLevelModel:
    energy_call = energy
    if all_recharge_available is True:
        energy_data = await energy_call.get_recharge_status()
    else:
        energy_data = await energy_call.get_battery_charge_level()

    return energy_data

async def update_connected_vehicle(connected_vehicle: ConnectedVehicle) -> ConnectedVehicleModel:
    connected_vehicle_call = connected_vehicle
    door_status = await connected_vehicle_call.get_door_status()
    window_status = await connected_vehicle_call.get_window_status()

    return {'door_status': door_status, 'window_status': window_status}

async def update_location(location: Location) -> LocationModel:
    location_call = location
    location_data = await location_call.get_location()
    return location_data