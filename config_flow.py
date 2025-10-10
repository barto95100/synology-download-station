"""Config flow for Synology Download Station integration."""
from __future__ import annotations

import logging
from typing import Any

import aiohttp
import async_timeout
import voluptuous as vol

from homeassistant import config_entries, exceptions
from homeassistant.const import (
    CONF_HOST,
    CONF_PASSWORD,
    CONF_PORT,
    CONF_SSL,
    CONF_USERNAME,
    CONF_VERIFY_SSL,
)
from homeassistant.data_entry_flow import FlowResult

from .const import (
    DEFAULT_PORT,
    DEFAULT_SSL,
    DEFAULT_VERIFY_SSL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Required(CONF_PORT, default=DEFAULT_PORT): int,
        vol.Required(CONF_SSL, default=DEFAULT_SSL): bool,
        vol.Required(CONF_VERIFY_SSL, default=DEFAULT_VERIFY_SSL): bool,
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): str,
    }
)


async def validate_input(data: dict[str, Any]) -> dict[str, str]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    session = aiohttp.ClientSession()
    
    schema = "https" if data[CONF_SSL] else "http"
    url = f"{schema}://{data[CONF_HOST]}:{data[CONF_PORT]}/webapi/auth.cgi"
    
    params = {
        "api": "SYNO.API.Auth",
        "version": 3,
        "method": "login",
        "account": data[CONF_USERNAME],
        "passwd": data[CONF_PASSWORD],
        "session": "DownloadStation",
        "format": "cookie"
    }
    
    try:
        async with async_timeout.timeout(10):
            async with session.get(
                url, params=params, ssl=not data[CONF_VERIFY_SSL]
            ) as response:
                result = await response.json()
                if result.get("success"):
                    return {"title": f"Synology Download Station ({data[CONF_HOST]})"}
                raise InvalidAuth
    except aiohttp.ClientError as err:
        _LOGGER.error("Error connecting to Synology Download Station: %s", err)
        raise CannotConnect from err
    except asyncio.TimeoutError as err:
        _LOGGER.error("Timeout connecting to Synology Download Station: %s", err)
        raise CannotConnect from err
    finally:
        await session.close()


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Synology Download Station."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        
        if user_input is not None:
            try:
                info = await validate_input(user_input)
                
                # Ensure we don't configure the same host twice
                await self.async_set_unique_id(user_input[CONF_HOST])
                self._abort_if_unique_id_configured()
                
                return self.async_create_entry(title=info["title"], data=user_input)
                
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(exceptions.HomeAssistantError):
    """Error to indicate there is invalid auth."""
