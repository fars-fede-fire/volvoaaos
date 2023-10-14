"""Constants for Volvo AAOS custom component"""

from __future__ import annotations

import logging

### Home Assistant constants ###
DOMAIN = "volvoaaos"

LOGGER = logging.getLogger(__package__)

CONF_VCC_API_KEY = "vcc_api_key"
CONF_VIN = "vin"
CONF_REFRESH_TOKEN = "refresh_token"

SERVICE_START_CLIMATIZATION = "start_climatization"


### Volvo constants ###
AUTH_URL = "https://volvoid.eu.volvocars.com/as/token.oauth2"
REFRESH_TOKEN = "refresh_token"
