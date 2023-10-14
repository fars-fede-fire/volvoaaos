"""Data update coordinator for Volvo AAOS"""

from dataclasses import dataclass

from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ACCESS_TOKEN
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN, LOGGER, CONF_VCC_API_KEY, CONF_VIN, CONF_REFRESH_TOKEN

from .models import RechargeModel, ConnectedVehicleModel, GetDoorModel
from .volvo import Auth, Energy, ConnectedVehicle

@dataclass
class VolvoData:
    """Volvo data stored in DataUpdateCoordinator"""

    energy: RechargeModel
    connected_vehicle_door_status: GetDoorModel

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

    @callback
    async def update_coordinator_data(self, datetime):
        access_token = self.config_entry.data[CONF_ACCESS_TOKEN]
        vcc_api_key = self.config_entry.data[CONF_VCC_API_KEY]
        vin = self.config_entry.data[CONF_VIN]
        energy = await update_energy(self.energy, access_token, vcc_api_key, vin)
        connected_vehicle = await update_connected_vehicle(self.connected_vehicle, access_token, vcc_api_key, vin)
        self.async_set_updated_data(VolvoData(energy=energy, connected_vehicle_door_status=connected_vehicle))

    @callback
    async def update_access_token(self, datetime):
        auth_update = await self.auth.reauth(refresh_token=self.config_entry.data[CONF_REFRESH_TOKEN])
        new_data = {**self.config_entry.data, CONF_ACCESS_TOKEN: auth_update.access_token, CONF_REFRESH_TOKEN:auth_update.refresh_token}
        self.hass.config_entries.async_update_entry(self.config_entry, data=new_data)
        LOGGER.debug("Access and refresh token updated")


async def update_energy(energy: Energy, access_token: str, vcc_api_key: str, vin: str) -> RechargeModel:
    energy_call = energy
    energy_call.access_token = access_token
    energy_call.vcc_api_key = vcc_api_key
    energy_call.vin = vin
    energy_data = await energy_call.get_recharge_status()
    return energy_data

async def update_connected_vehicle(connected_vehicle: ConnectedVehicle, access_token: str, vcc_api_key: str, vin: str) -> ConnectedVehicleModel:
    connected_vehicle_call = connected_vehicle
    connected_vehicle_call.access_token = access_token
    connected_vehicle_call.vcc_api_key = vcc_api_key
    connected_vehicle_call.vin = vin
    door_status = await connected_vehicle_call.get_door_status()
    return door_status