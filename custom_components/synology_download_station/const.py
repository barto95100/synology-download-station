"""Constants for the Synology Download Station integration."""
from datetime import timedelta

DOMAIN = "synology_download_station"
DEFAULT_NAME = "Synology Download Station"
DEFAULT_PORT = 5000
DEFAULT_SSL = False
DEFAULT_VERIFY_SSL = False
DEFAULT_TIMEOUT = 30
SCAN_INTERVAL = timedelta(seconds=60)  # Réduit la fréquence pour moins stresser le NAS

# Session management
# Synology sessions typically expire after 10-15 minutes of inactivity
# We'll refresh proactively after 8 minutes to be safe
SESSION_TIMEOUT = timedelta(minutes=8)

# API endpoints
API_AUTH = "auth.cgi"
API_DOWNLOAD = "DownloadStation/task.cgi"

# API parameters
API_AUTH_METHOD = "login"
API_AUTH_VERSION = 3
API_DOWNLOAD_METHOD = "list"
API_DOWNLOAD_VERSION = 3

# Sensor attributes
ATTR_TASKS = "tasks"
ATTR_TOTAL_SIZE = "total_size"
ATTR_TOTAL_DOWNLOADED = "total_downloaded"
ATTR_TOTAL_SPEED = "total_speed"
ATTR_ACTIVE_DOWNLOADS = "active_downloads"
ATTR_ACTIVE_UPLOADS = "active_uploads"
