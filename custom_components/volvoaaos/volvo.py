"""Asynchronous Python client for Volvo AAOS"""
from __future__ import annotations

from dataclasses import dataclass, field, KW_ONLY
from typing import Any, cast

import asyncio
import backoff

import async_timeout
from aiohttp.client import ClientSession
from aiohttp.hdrs import METH_GET, METH_POST

from .models import AuthModel, RechargeModel, BatteryChargeLevelModel, GetVinModel, GetVehicleModel, GetDoorModel, StartClimateModel, StopClimateModel, LockModel, UnlockModel, GetWindowModel, LocationModel, BatteryChargeLevelConnectedVehicleModel
from .const import LOGGER


@dataclass
class Volvo:
    """Class for handling connection with Volvo"""

    request_timeout: int = 20
    session: ClientSession | None = None
    _close_session: bool = False

    #@backoff.on_exception(backoff.expo, aiohttp.exc max_tries=4)
    async def _request(
        self,
        url: str,
        method: str = METH_GET,
        headers: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Handle request to Volvo backend."""

        if self.session is None:
            self.session = ClientSession()
            self._close_session = True

        async with async_timeout.timeout(self.request_timeout):
            response = await self.session.request(
                method,
                url,
                data=data,
                headers=headers,
            )
            response.raise_for_status()

        return cast(dict[str, Any], await response.json())

    async def close(self) -> None:
        """Close client session"""

        if self.session and self._close_session:
            await self.session.close()

    async def __aenter__(self):
        """Async enter"""

        return self

    async def __aexit__(self, *_exc_inf: Any) -> None:
        """Async exit"""

        await self.close()


class Auth(Volvo):
    """Handles Volvo auth process"""

    async def authenticate(self, username: str, password: str) -> AuthModel:
        """Obtain credentials from Volvo"""

        url = "https://volvoid.eu.volvocars.com/as/token.oauth2"

        data = {
            "username": username,
            "password": password,
            "grant_type": "password",
            "scope": "openid email profile care_by_volvo:financial_information:invoice:read care_by_volvo:financial_information:payment_method care_by_volvo:subscription:read customer:attributes customer:attributes:write order:attributes vehicle:attributes tsp_customer_api:all conve:brake_status conve:climatization_start_stop conve:command_accessibility conve:commands conve:diagnostics_engine_status conve:diagnostics_workshop conve:doors_status conve:engine_status conve:environment conve:fuel_status conve:honk_flash conve:lock conve:lock_status conve:navigation conve:odometer_status conve:trip_statistics conve:tyre_status conve:unlock conve:vehicle_relation conve:warnings conve:windows_status energy:battery_charge_level energy:charging_connection_status energy:charging_system_status energy:electric_range energy:estimated_charging_time energy:recharge_status",
        }

        headers = {
            "authorization": "Basic aDRZZjBiOlU4WWtTYlZsNnh3c2c1WVFxWmZyZ1ZtSWFEcGhPc3kxUENhVXNpY1F0bzNUUjVrd2FKc2U0QVpkZ2ZJZmNMeXc=",
            "content-type": "application/x-www-form-urlencoded",
        }

        response = await self._request(
            url, method=METH_POST, headers=headers, data=data
        )
        return AuthModel.parse_obj(response)

    async def reauth(self, refresh_token):
        """Exchange refresh token for Bearer token"""

        url = "https://volvoid.eu.volvocars.com/as/token.oauth2"

        data = {"grant_type": "refresh_token", "refresh_token": refresh_token}

        headers = {
            "authorization": "Basic aDRZZjBiOlU4WWtTYlZsNnh3c2c1WVFxWmZyZ1ZtSWFEcGhPc3kxUENhVXNpY1F0bzNUUjVrd2FKc2U0QVpkZ2ZJZmNMeXc=",
            "content-type": "application/x-www-form-urlencoded",
        }

        response = await self._request(
            url=url, method=METH_POST, headers=headers, data=data
        )
        return AuthModel.parse_obj(response)

@dataclass
class Energy(Volvo):
    """Handling Energy API calls"""

    _: KW_ONLY
    access_token: str = None
    vcc_api_key: str = None
    content_type: str = "application/json"
    vin: str = None

    async def get_recharge_status(self):
        """Get recharge status"""

        url = f"https://api.volvocars.com/energy/v1/vehicles/{self.vin}/recharge-status"
        headers = {
            "content-type": self.content_type,
            "authorization": f"Bearer {self.access_token}",
            "vcc-api-key": self.vcc_api_key,
        }

        response = await self._request(url=url, headers=headers)
        return RechargeModel.parse_obj(response)

    async def get_battery_charge_level(self):
        """Get battery charge state."""

        url = f"https://api.volvocars.com/connected-vehicle/v2/vehicles/{self.vin}/battery-charge-level"
        headers = {
            "content-type": self.content_type,
            "authorization": f"Bearer {self.access_token}",
            "vcc-api-key": self.vcc_api_key,
        }

        response = await self._request(url=url, headers=headers)
        return BatteryChargeLevelConnectedVehicleModel.parse_obj(response)



@dataclass
class ConnectedVehicle(Volvo):
    """Handling Connected Vehicle API calls"""

    _: KW_ONLY
    access_token: str = None
    vcc_api_key: str = None
    content_type: str = "application/json"
    vin: str | None = None

    async def list_vehicles(self):
        """Get list of vehicles in relation to Volvo-id."""

        url = "https://api.volvocars.com/connected-vehicle/v2/vehicles"

        headers = {
            "content-type": self.content_type,
            "authorization": f"Bearer {self.access_token}",
            "vcc-api-key": self.vcc_api_key,
        }

        response = await self._request(url=url, headers=headers)
        return GetVinModel.parse_obj(response)

    async def get_vehicle_data(self):
        """Get data of vehicle based on VIN"""

        url = f"https://api.volvocars.com/connected-vehicle/v2/vehicles/{self.vin}"

        headers = {
            "content-type": self.content_type,
            "authorization": f"Bearer {self.access_token}",
            "vcc-api-key": self.vcc_api_key,
        }

        response = await self._request(url=url, headers=headers)
        return GetVehicleModel.parse_obj(response)

    async def get_door_status(self):
        """Get status of doors"""

        url = f"https://api.volvocars.com/connected-vehicle/v2/vehicles/{self.vin}/doors"

        headers = {
            "content-type": self.content_type,
            "authorization": f"Bearer {self.access_token}",
            "vcc-api-key": self.vcc_api_key,
        }

        response = await self._request(url=url, headers=headers)
        return GetDoorModel.parse_obj(response)

    async def get_window_status(self):
        """Get status of windows."""

        url = f"https://api.volvocars.com/connected-vehicle/v2/vehicles/{self.vin}/windows"

        headers = {
            "content-type": self.content_type,
            "authorization": f"Bearer {self.access_token}",
            "vcc-api-key": self.vcc_api_key,
        }

        response = await self._request(url=url, headers=headers)
        return GetWindowModel.parse_obj(response)

    async def lock_car(self):
        """Lock the car."""

        url = f"https://api.volvocars.com/connected-vehicle/v2/vehicles/{self.vin}/commands/lock"

        headers = {
            "content-type": self.content_type,
            "authorization": f"Bearer {self.access_token}",
            "vcc-api-key": self.vcc_api_key,
        }

        response = await self._request(url=url, headers=headers, method=METH_POST)
        return LockModel.parse_obj(response)

    async def unlock_car(self):
        """Unlock the car."""

        url = f"https://api.volvocars.com/connected-vehicle/v2/vehicles/{self.vin}/commands/unlock"

        headers = {
            "content-type": self.content_type,
            "authorization": f"Bearer {self.access_token}",
            "vcc-api-key": self.vcc_api_key,
        }

        response = await self._request(url=url, headers=headers, method=METH_POST)
        return UnlockModel.parse_obj(response)


    async def  set_climate_start(self):
        """Start climatization"""

        url = f"https://api.volvocars.com/connected-vehicle/v2/vehicles/{self.vin}/commands/climatization-start"

        headers = {
            "content-type": self.content_type,
            "authorization": f"Bearer {self.access_token}",
            "vcc-api-key": self.vcc_api_key,
        }

        response = await self._request(url=url, headers=headers, method=METH_POST)
        return StartClimateModel.parse_obj(response)

    async def  set_climate_stop(self):
        """Stop climatization"""

        url = f"https://api.volvocars.com/connected-vehicle/v2/vehicles/{self.vin}/commands/climatization-stop"

        headers = {
            "content-type": self.content_type,
            "authorization": f"Bearer {self.access_token}",
            "vcc-api-key": self.vcc_api_key,
        }

        response = await self._request(url=url, headers=headers, method=METH_POST)
        return StopClimateModel.parse_obj(response)

@dataclass
class Location(Volvo):
    """Handling Location API calls"""

    _: KW_ONLY
    access_token: str = None
    vcc_api_key: str = None
    content_type: str = "application/json"
    vin: str = None

    async def get_location(self):
        """Get location"""

        url = f"https://api.volvocars.com/location/v1/vehicles/{self.vin}/location"
        headers = {
            "content-type": self.content_type,
            "authorization": f"Bearer {self.access_token}",
            "vcc-api-key": self.vcc_api_key,
        }

        response = await self._request(url=url, headers=headers)
        return LocationModel.parse_obj(response)