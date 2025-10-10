"""Sensor platform for Synology Download Station."""
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfDataRate, UnitOfInformation
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import (
    ATTR_ACTIVE_DOWNLOADS,
    ATTR_ACTIVE_UPLOADS,
    ATTR_TASKS,
    ATTR_TOTAL_DOWNLOADED,
    ATTR_TOTAL_SIZE,
    ATTR_TOTAL_SPEED,
    DOMAIN,
)

SENSOR_TYPES = {
    "active_downloads": {
        "name": "Active Downloads",
        "unit_of_measurement": "",
        "icon": "mdi:download",
        "value": lambda data: data[ATTR_ACTIVE_DOWNLOADS],
    },
    "active_uploads": {
        "name": "Active Uploads",
        "unit_of_measurement": "",
        "icon": "mdi:upload",
        "value": lambda data: data[ATTR_ACTIVE_UPLOADS],
    },
    "total_speed": {
        "name": "Total Speed",
        "unit_of_measurement": UnitOfDataRate.MEGABYTES_PER_SECOND,
        "device_class": SensorDeviceClass.DATA_RATE,
        "icon": "mdi:speedometer",
        "value": lambda data: round(data[ATTR_TOTAL_SPEED] / (1024 * 1024), 2),  # B/s to MB/s
    },
    "total_size": {
        "name": "Total Size",
        "unit_of_measurement": UnitOfInformation.GIGABYTES,
        "device_class": SensorDeviceClass.DATA_SIZE,
        "icon": "mdi:harddisk",
        "value": lambda data: round(data[ATTR_TOTAL_SIZE] / (1024 ** 3), 2),  # B to GB
    },
    "total_downloaded": {
        "name": "Total Downloaded",
        "unit_of_measurement": UnitOfInformation.GIGABYTES,
        "device_class": SensorDeviceClass.DATA_SIZE,
        "icon": "mdi:download-network",
        "value": lambda data: round(data[ATTR_TOTAL_DOWNLOADED] / (1024 ** 3), 2),  # B to GB
    },
    "download_progress": {
        "name": "Download Progress",
        "unit_of_measurement": PERCENTAGE,
        "icon": "mdi:progress-download",
        "value": lambda data: round(
            (data[ATTR_TOTAL_DOWNLOADED] / data[ATTR_TOTAL_SIZE] * 100) if data[ATTR_TOTAL_SIZE] > 0 else 0,
            2,
        ),
    },
}


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the Synology Download Station sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    entities = [
        SynologyDownloadStationSensor(coordinator, sensor_type, entry.entry_id)
        for sensor_type in SENSOR_TYPES
    ]
    
    async_add_entities(entities, True)


class SynologyDownloadStationSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Synology Download Station sensor."""

    _attr_has_entity_name = True
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator: DataUpdateCoordinator, sensor_type: str, entry_id: str) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_type = sensor_type
        self._entry_id = entry_id
        self._attr_name = SENSOR_TYPES[sensor_type]["name"]
        self._attr_icon = SENSOR_TYPES[sensor_type].get("icon")
        self._attr_native_unit_of_measurement = SENSOR_TYPES[sensor_type].get("unit_of_measurement")
        if "device_class" in SENSOR_TYPES[sensor_type]:
            self._attr_device_class = SENSOR_TYPES[sensor_type]["device_class"]
        self._attr_unique_id = f"{entry_id}_{sensor_type}"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None
        return SENSOR_TYPES[self._sensor_type]["value"](self.coordinator.data)

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        if not self.coordinator.data:
            return {}
            
        attrs = {}
        if self._sensor_type == "active_downloads" and ATTR_TASKS in self.coordinator.data:
            tasks = [
                {
                    "title": task["title"],
                    "status": task["status"],
                    "size": task["size"],
                    "downloaded": task["additional"]["transfer"]["size_downloaded"],
                    "speed": task["additional"]["transfer"]["speed_download"],
                    "progress": (
                        task["additional"]["transfer"]["size_downloaded"] / task["size"] * 100
                        if task["size"] > 0
                        else 0
                    ),
                }
                for task in self.coordinator.data[ATTR_TASKS]
                if task["status"] == "downloading"
            ]
            attrs["downloads"] = tasks
            
        return attrs

    @property
    def device_info(self):
        """Return the device info."""
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": "Synology Download Station",
            "manufacturer": "Synology",
        }
