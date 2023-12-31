"""Support for Volvo AAOS."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform, CONF_USERNAME, CONF_ACCESS_TOKEN, CONF_PASSWORD
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, LOGGER, CONF_VCC_API_KEY, CONF_VIN, CONF_REFRESH_TOKEN, CONF_ALL_RECHARGE_AVAILABLE
from .volvo import Auth, Energy, ConnectedVehicle, Location
from .coordinator import VolvoUpdateCoordinator, VolvoData, update_energy

PLATFORMS = [Platform.SENSOR, Platform.LOCK, Platform.BINARY_SENSOR, Platform.DEVICE_TRACKER, Platform.BUTTON]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Setup Volvo AAOS from config entry."""

    coordinator = VolvoUpdateCoordinator(hass, entry)
    session = async_get_clientsession(hass)

    # Exchange reauth token else auth from username and password

    auth = Auth(session=session)
    try:
        reauth = await auth.reauth(refresh_token=entry.data[CONF_REFRESH_TOKEN])
        new_data = {**entry.data, CONF_ACCESS_TOKEN: reauth.access_token, CONF_REFRESH_TOKEN: reauth.refresh_token}
        hass.config_entries.async_update_entry(entry, data=new_data)
        LOGGER.debug('Refresh token still valid. Updated access token.')
    except Exception as e:
        LOGGER.debug(e)
        LOGGER.debug('Refresh token invalid - retry login using username and password')
        try:
            authenticate = await auth.authenticate(username=entry.data[CONF_USERNAME], password=entry.data[CONF_PASSWORD])
            new_data = {**entry.data, CONF_ACCESS_TOKEN: authenticate.access_token, CONF_REFRESH_TOKEN: authenticate.refresh_token}
            hass.config_entries.async_update_entry(entry, data=new_data)
            LOGGER.debug('Logged in using username and password.')
        except Exception as e:
            LOGGER.debug(e)
            LOGGER.debug('Could not login. Try reinstall the component.')

    energy = Energy(session=session, access_token=entry.data[CONF_ACCESS_TOKEN], vcc_api_key=entry.data[CONF_VCC_API_KEY], vin=entry.data[CONF_VIN])
    energy_data = await update_energy(energy=energy, all_recharge_available=entry.data[CONF_ALL_RECHARGE_AVAILABLE])

    connected_vehicle = ConnectedVehicle(session=session, access_token=entry.data[CONF_ACCESS_TOKEN], vcc_api_key=entry.data[CONF_VCC_API_KEY], vin=entry.data[CONF_VIN])
    connected_vehicle_door_status_data = await connected_vehicle.get_door_status()
    connected_vehicle_window_status_data = await connected_vehicle.get_window_status()

    location = Location(session=session, access_token=entry.data[CONF_ACCESS_TOKEN], vcc_api_key=entry.data[CONF_VCC_API_KEY], vin=entry.data[CONF_VIN])
    location_data = await location.get_location()

    coordinator.async_set_updated_data(VolvoData(energy=energy_data, connected_vehicle_door_status=connected_vehicle_door_status_data, connected_vehicle_window_status=connected_vehicle_window_status_data, location=location_data))

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload Volvo AAOS config entry."""

    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        del hass.data[DOMAIN][entry.entry_id]
    return unload_ok
