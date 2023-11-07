"""Constants for Volvo AAOS custom component"""

from __future__ import annotations

import logging

### Home Assistant constants ###
DOMAIN = "volvoaaos"

LOGGER = logging.getLogger(__package__)

CONF_VCC_API_KEY = "vcc_api_key"
CONF_VIN = "vin"
CONF_REFRESH_TOKEN = "refresh_token"
CONF_ALL_RECHARGE_AVAILABLE = "all_recharge_available"


### Volvo constants ###
AUTH_URL = "https://volvoid.eu.volvocars.com/as/token.oauth2"
REFRESH_TOKEN = "refresh_token"
