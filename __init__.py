"""The Synology Download Station integration."""
import asyncio
import json
import logging
from datetime import datetime, timedelta
import aiohttp
import async_timeout
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.util import dt as dt_util

from .const import (
    DOMAIN,
    DEFAULT_PORT,
    DEFAULT_SSL,
    DEFAULT_VERIFY_SSL,
    SCAN_INTERVAL,
    SESSION_TIMEOUT,
)
from homeassistant.const import (
    CONF_HOST,
    CONF_PORT,
    CONF_SSL,
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_VERIFY_SSL,
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Synology Download Station from a config entry."""
    config = entry.data
    host = config[CONF_HOST]
    username = config[CONF_USERNAME]
    password = config[CONF_PASSWORD]
    port = config.get(CONF_PORT, DEFAULT_PORT)
    use_ssl = config.get(CONF_SSL, DEFAULT_SSL)
    verify_ssl = config.get(CONF_VERIFY_SSL, DEFAULT_VERIFY_SSL)

    coordinator = SynologyDownloadStationDataUpdateCoordinator(
        hass, host, port, username, password, use_ssl, verify_ssl
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    # Logout from Synology before unloading
    coordinator = hass.data[DOMAIN].get(entry.entry_id)
    if coordinator:
        await coordinator.async_logout()
    
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok

class SynologyDownloadStationDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the Synology Download Station API."""

    def __init__(
        self, hass, host, port, username, password, use_ssl, verify_ssl
    ):
        """Initialize global Synology Download Station data updater."""
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.use_ssl = use_ssl
        self.verify_ssl = verify_ssl
        self.sid = None
        self.sid_timestamp = None  # Track when the session was created

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
        )

    def _is_session_valid(self):
        """Check if the current session is still valid."""
        if not self.sid or not self.sid_timestamp:
            return False
        
        # Check if session has expired based on SESSION_TIMEOUT
        time_since_login = dt_util.utcnow() - self.sid_timestamp
        if time_since_login >= SESSION_TIMEOUT:
            _LOGGER.debug(
                "Session expired (age: %s, timeout: %s), will reconnect",
                time_since_login,
                SESSION_TIMEOUT
            )
            return False
        
        return True

    async def _async_login(self, force=False):
        """Login to the Synology Download Station API."""
        # Check if we have a valid session
        if not force and self._is_session_valid():
            return True

        # If we have an old session, invalidate it
        if self.sid:
            _LOGGER.debug("Invalidating old session before new login")
            self.sid = None
            self.sid_timestamp = None

        schema = "https" if self.use_ssl else "http"
        url = f"{schema}://{self.host}:{self.port}/webapi/auth.cgi"
        
        params = {
            "api": "SYNO.API.Auth",
            "version": 3,
            "method": "login",
            "account": self.username,
            "passwd": self.password,
            "session": "DownloadStation",
            "format": "cookie"
        }

        try:
            _LOGGER.debug("Attempting login to %s:%s", self.host, self.port)
            session = async_get_clientsession(self.hass, verify_ssl=self.verify_ssl)
            async with async_timeout.timeout(60):
                async with session.get(url, params=params) as response:
                    response_status = response.status
                    _LOGGER.debug(
                        "Login response received: status=%s",
                        response_status
                    )
                    
                    # Read response text first for debugging
                    response_text = await response.text()
                    
                    try:
                        data = json.loads(response_text)
                    except Exception as json_err:
                        _LOGGER.error(
                            "Failed to parse JSON response from Synology (status %s). "
                            "Response text (first 500 chars): %s. Parse error: %s (%s)",
                            response_status,
                            response_text[:500],
                            type(json_err).__name__,
                            json_err
                        )
                        return False
                    
                    if data.get("success"):
                        self.sid = data["data"]["sid"]
                        self.sid_timestamp = dt_util.utcnow()
                        _LOGGER.info(
                            "Successfully logged in to Synology Download Station at %s:%s (session valid for ~%s)",
                            self.host,
                            self.port,
                            SESSION_TIMEOUT
                        )
                        return True
                    
                    error_code = data.get("error", {}).get("code", "unknown")
                    _LOGGER.error(
                        "Failed to login to Synology Download Station at %s:%s. "
                        "Error code: %s, Full response: %s",
                        self.host,
                        self.port,
                        error_code,
                        data
                    )
                    return False
        except asyncio.TimeoutError as err:
            _LOGGER.error(
                "Timeout (60s) connecting to Synology Download Station at %s:%s. "
                "Check if the host is reachable and the port is correct. Error: %s (%s)",
                self.host,
                self.port,
                type(err).__name__,
                str(err) if str(err) else "No additional details"
            )
            return False
        except aiohttp.ClientError as err:
            _LOGGER.error(
                "Network/HTTP error connecting to Synology Download Station at %s:%s. "
                "Error type: %s, Details: %s",
                self.host,
                self.port,
                type(err).__name__,
                str(err) if str(err) else "No additional details"
            )
            return False
        except Exception as err:
            _LOGGER.exception(
                "Unexpected error during login to Synology Download Station at %s:%s. "
                "Error type: %s, Message: %s",
                self.host,
                self.port,
                type(err).__name__,
                str(err) if str(err) else "No error message"
            )
            return False

    async def async_logout(self):
        """Logout from the Synology Download Station API."""
        if not self.sid:
            return
        
        schema = "https" if self.use_ssl else "http"
        url = f"{schema}://{self.host}:{self.port}/webapi/auth.cgi"
        
        params = {
            "api": "SYNO.API.Auth",
            "version": 3,
            "method": "logout",
            "session": "DownloadStation",
            "_sid": self.sid,
        }
        
        try:
            session = async_get_clientsession(self.hass, verify_ssl=self.verify_ssl)
            async with async_timeout.timeout(60):
                async with session.get(url, params=params) as response:
                    data = await response.json(content_type=None)
                    if data.get("success"):
                        _LOGGER.info("Successfully logged out from Synology Download Station")
                    else:
                        _LOGGER.warning("Logout response: %s", data)
        except Exception as err:
            _LOGGER.debug("Error during logout (non-critical): %s", err)
        finally:
            # Always clear the session
            self.sid = None
            self.sid_timestamp = None

    async def _async_get_downloads(self, retry=True):
        """Get the list of downloads from Synology Download Station."""
        if not await self._async_login():
            return None

        schema = "https" if self.use_ssl else "http"
        url = f"{schema}://{self.host}:{self.port}/webapi/DownloadStation/task.cgi"
        
        params = {
            "api": "SYNO.DownloadStation.Task",
            "version": 3,
            "method": "list",
            "_sid": self.sid,
            "additional": "transfer"  # Réduit à transfer uniquement pour accélérer
        }

        try:
            _LOGGER.debug("Fetching downloads from %s:%s", self.host, self.port)
            session = async_get_clientsession(self.hass, verify_ssl=self.verify_ssl)
            async with async_timeout.timeout(60):
                async with session.get(url, params=params) as response:
                    response_status = response.status
                    _LOGGER.debug(
                        "Download list response received: status=%s",
                        response_status
                    )
                    
                    # Read response text first for debugging
                    response_text = await response.text()
                    
                    try:
                        data = json.loads(response_text)
                    except Exception as json_err:
                        _LOGGER.error(
                            "Failed to parse JSON response from Synology when fetching downloads (status %s). "
                            "Response text (first 500 chars): %s. Parse error: %s (%s)",
                            response_status,
                            response_text[:500],
                            type(json_err).__name__,
                            json_err
                        )
                        return None
                    
                    if data.get("success"):
                        tasks = data.get("data", {}).get("tasks", [])
                        _LOGGER.debug("Successfully fetched %d tasks from Synology", len(tasks))
                        return tasks
                    
                    # Check for session expired error (error code 119)
                    error_code = data.get("error", {}).get("code")
                    if error_code == 119 and retry:
                        _LOGGER.warning(
                            "Synology Download Station session expired (error 119) at %s:%s, retrying with new login...",
                            self.host,
                            self.port
                        )
                        # Force new login by clearing session
                        self.sid = None
                        self.sid_timestamp = None
                        return await self._async_get_downloads(retry=False)
                    
                    _LOGGER.error(
                        "Failed to fetch downloads from Synology Download Station at %s:%s. "
                        "Error code: %s, Full response: %s",
                        self.host,
                        self.port,
                        error_code,
                        data
                    )
                    return None
        except asyncio.TimeoutError as err:
            _LOGGER.error(
                "Timeout (60s) fetching downloads from Synology Download Station at %s:%s. "
                "The NAS may be slow or unresponsive. Error: %s (%s)",
                self.host,
                self.port,
                type(err).__name__,
                str(err) if str(err) else "No additional details"
            )
            return None
        except aiohttp.ClientError as err:
            _LOGGER.error(
                "Network/HTTP error fetching downloads from Synology Download Station at %s:%s. "
                "Check network connectivity. Error type: %s, Details: %s",
                self.host,
                self.port,
                type(err).__name__,
                str(err) if str(err) else "No additional details"
            )
            return None
        except Exception as err:
            _LOGGER.exception(
                "Unexpected error fetching downloads from Synology Download Station at %s:%s. "
                "Error type: %s, Message: %s",
                self.host,
                self.port,
                type(err).__name__,
                str(err) if str(err) else "No error message"
            )
            return None

    async def _async_update_data(self):
        """Update data via library."""
        try:
            _LOGGER.debug("Starting data update for Synology Download Station at %s:%s", self.host, self.port)
            
            downloads = await self._async_get_downloads()
            if downloads is None:
                error_msg = (
                    f"Failed to fetch data from Synology Download Station at {self.host}:{self.port}. "
                    f"Check previous error messages for details."
                )
                _LOGGER.error(error_msg)
                raise UpdateFailed(error_msg)
            
            # Calculate totals
            total_size = 0
            total_downloaded = 0
            total_speed = 0
            active_downloads = 0
            active_uploads = 0
            
            for download in downloads:
                try:
                    status = download.get("status")
                    size = download.get("size", 0)
                    transfer = download.get("additional", {}).get("transfer", {})
                    size_downloaded = transfer.get("size_downloaded", 0)
                    speed_download = transfer.get("speed_download", 0)
                    
                    total_size += size
                    total_downloaded += size_downloaded
                    total_speed += speed_download
                    
                    if status == "downloading":
                        active_downloads += 1
                    elif status == "seeding":
                        active_uploads += 1
                except Exception as task_err:
                    _LOGGER.warning(
                        "Error processing task data: %s. Task data: %s",
                        task_err,
                        download
                    )
                    continue
            
            _LOGGER.debug(
                "Synology Download Station update successful: %d active downloads, %d seeding, %d total tasks",
                active_downloads,
                active_uploads,
                len(downloads)
            )
            
            return {
                "tasks": downloads,
                "total_size": total_size,
                "total_downloaded": total_downloaded,
                "total_speed": total_speed,
                "active_downloads": active_downloads,
                "active_uploads": active_uploads,
            }
        except UpdateFailed:
            # Re-raise UpdateFailed as-is
            raise
        except Exception as err:
            error_msg = (
                f"Unexpected error updating Synology Download Station data at {self.host}:{self.port}. "
                f"Error type: {type(err).__name__}, Message: {err}"
            )
            _LOGGER.exception(error_msg)
            raise UpdateFailed(error_msg) from err
