# Synology Download Station for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub Release](https://img.shields.io/github/v/release/barto95100/synology-download-station)](https://github.com/barto95100/synology-download-station/releases)
[![License](https://img.shields.io/github/license/barto95100/synology-download-station)](LICENSE)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/barto95100/synology-download-station/graphs/commit-activity)

Home Assistant integration to monitor and control Synology Download Station in real-time.

> 🇫🇷 [Version française / French version](README.md)

---

## ✨ Features

- 📊 **Real-time sensors**:
  - Number of active downloads
  - Number of active uploads (seeding)
  - Total download speed
  - Total download size
  - Downloaded data
  - Overall progress

- 🔄 **Automatic updates** every 60 seconds
- 🔐 **Secure authentication** with session management
- 🌐 **SSL/HTTPS support**
- 📝 **Download details** in sensor attributes

## Installation

### Method 1: Manual Installation

1. Copy the `synology_download_station` folder into your Home Assistant `custom_components` directory:
   ```
   /config/custom_components/synology_download_station/
   ```

2. Restart Home Assistant

3. Add the integration via the UI:
   - Go to **Settings** → **Devices & Services**
   - Click **+ Add Integration**
   - Search for "Synology Download Station"
   - Follow the configuration instructions

### Method 2: Via HACS (Coming Soon)

This integration will be available via HACS soon.

## Configuration

When adding the integration, you will need to provide:

- **Host**: IP address or hostname of your Synology NAS (e.g., `192.168.1.10`)
- **Port**: API port (default `5000` for HTTP, `5001` for HTTPS)
- **SSL**: Check if using HTTPS
- **Verify SSL**: Uncheck if using a self-signed certificate
- **Username**: Your Synology username
- **Password**: Your Synology password

### Configuration Example

```
Host: 192.168.1.10
Port: 5000
SSL: No
Verify SSL: No
Username: your_username
Password: your_password
```

## Available Sensors

Once configured, the integration will create the following sensors:

| Sensor | Description | Unit |
|--------|-------------|------|
| `sensor.synology_download_station_active_downloads` | Number of active downloads | - |
| `sensor.synology_download_station_active_uploads` | Number of active uploads | - |
| `sensor.synology_download_station_total_speed` | Total download speed | MB/s |
| `sensor.synology_download_station_total_size` | Total download size | GB |
| `sensor.synology_download_station_total_downloaded` | Downloaded data | GB |
| `sensor.synology_download_station_download_progress` | Overall progress | % |

## Usage Examples

### Lovelace Card

```yaml
type: entities
title: Synology Download Station
entities:
  - entity: sensor.synology_download_station_active_downloads
    name: Active Downloads
  - entity: sensor.synology_download_station_total_speed
    name: Speed
  - entity: sensor.synology_download_station_download_progress
    name: Progress
```

### Automation - Download Complete Notification

```yaml
automation:
  - alias: "Download Complete Notification"
    trigger:
      - platform: state
        entity_id: sensor.synology_download_station_download_progress
        to: "100"
    action:
      - service: notify.mobile_app
        data:
          title: "Download Complete"
          message: "All your downloads are finished!"
```

## Troubleshooting

### Integration won't connect

1. Check that your Synology NAS is accessible from Home Assistant
2. Verify credentials (username and password)
3. Check that Download Station is installed and running on your NAS
4. If using SSL, try unchecking "Verify SSL"

### Sensors not updating

1. Check Home Assistant logs for errors
2. Restart the integration from **Settings** → **Devices & Services**

### Enable Debug Logging

Add this to your `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.synology_download_station: debug
```

## Support

To report a bug or request a feature, please open an issue on GitHub.

## License

MIT License

## Credits

Developed for Home Assistant with ❤️ by HACF

