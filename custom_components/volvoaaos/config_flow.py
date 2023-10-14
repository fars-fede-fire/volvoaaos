"""Config flow for Volvo AAOS."""

from __future__ import annotations

from typing import Any
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD, CONF_ACCESS_TOKEN, CONF_NAME
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers import selector

from .const import DOMAIN, LOGGER, CONF_VIN, CONF_REFRESH_TOKEN, CONF_VCC_API_KEY

from .volvo import Auth, ConnectedVehicle

SETUP_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME): selector.TextSelector(),
        vol.Required(CONF_PASSWORD): selector.TextSelector(),
        vol.Required(CONF_VCC_API_KEY): selector.TextSelector(),
    }
)

SELECT_NAME_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME): selector.TextSelector(),
    }
)




class VolvoaaosConfigFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle Volvo AAOS config flow."""

    VERSION = 1

    username: str
    password: str
    vcc_api_key: str
    access_token: str = None
    refresh_token: str = None
    vin: str = None
    name: str = None

    def __init__(self) -> None:
        """Initialize Volvo AAOS flow."""
        self.device = None

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Define a Volvo AAOS device for config flow."""

        errors = {}

        if user_input is not None:
            self.username = user_input[CONF_USERNAME]
            self.password = user_input[CONF_PASSWORD]
            self.vcc_api_key = user_input[CONF_VCC_API_KEY]
            session = async_get_clientsession(self.hass)

            auth = Auth(session=session)

            response = await auth.authenticate(
                username=self.username, password=self.password
            )

            self.access_token = response.access_token
            self.refresh_token = response.refresh_token

            return await self.async_step_select_vin()

        return self.async_show_form(
            step_id="user", data_schema=SETUP_SCHEMA, errors=errors
        )

    async def async_step_select_vin(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Select which car to setup."""

        errors = {}

        if user_input is not None:
            self.vin = user_input[CONF_VIN]



            return await self.async_step_set_name()

        session = async_get_clientsession(self.hass)

        connected_vehicle = ConnectedVehicle(session=session, access_token=self.access_token, vcc_api_key=self.vcc_api_key)

        response = await connected_vehicle.list_vehicles()

        list_of_vins = []
        for item in response.data:
            list_of_vins.append(item.vin)


        SELECT_VIN_SCHEMA = vol.Schema(
            {
                vol.Required(CONF_VIN): selector.SelectSelector(selector.SelectSelectorConfig(options=list_of_vins))
            }
        )
        return self.async_show_form(
            step_id="select_vin", data_schema=SELECT_VIN_SCHEMA, errors=errors
        )

    async def async_step_set_name(self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Set name for car"""

        errors = {}

        if user_input is not None:
            self.name = user_input[CONF_NAME]

            data = {
                CONF_USERNAME: self.username,
                CONF_PASSWORD: self.password,
                CONF_VCC_API_KEY: self.vcc_api_key,
                CONF_ACCESS_TOKEN: self.access_token,
                CONF_REFRESH_TOKEN: self.refresh_token,
                CONF_VIN:self.vin,
                CONF_NAME: self.name
            }

            await self.async_set_unique_id(self.vin)

            return self.async_create_entry(title=f"Volvo - {self.name}", data=data)

        return self.async_show_form(
            step_id="set_name", data_schema=SELECT_NAME_SCHEMA, errors=errors
        )