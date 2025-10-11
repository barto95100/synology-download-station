# Lovelace Card Examples

This document presents various card examples to display your Synology Download Station data in Home Assistant.

**🇫🇷 Version française disponible :** [LOVELACE_EXAMPLES.md](LOVELACE_EXAMPLES.md)

---

## 📊 Simple Overview

A simple card displaying all main sensors.

<details >

<summary> ℹ️ Code here</summary>

```yaml
type: entities
title: Synology Download Station
entities:
  - entity: sensor.synology_download_station_active_downloads
    name: Active Downloads
    icon: mdi:download
  - entity: sensor.synology_download_station_total_speed
    name: Total Speed
    icon: mdi:speedometer
  - entity: sensor.synology_download_station_download_progress
    name: Progress
    icon: mdi:progress-download
  - entity: sensor.synology_download_station_total_downloaded
    name: Total Downloaded
    icon: mdi:download-network
  - entity: sensor.synology_download_station_total_size
    name: Total Size
    icon: mdi:harddisk
```

</details>
## 🎯 Compact View with Icons

Compact display with large icons, perfect for a dashboard.

<details >

<summary> ℹ️ Code here</summary>

```yaml
type: glance
title: Download Station
entities:
  - entity: sensor.synology_download_station_active_downloads
    name: Active
  - entity: sensor.synology_download_station_total_speed
    name: Speed
  - entity: sensor.synology_download_station_download_progress
    name: Progress
  - entity: sensor.synology_download_station_total_downloaded
    name: Downloaded
show_name: true
show_icon: true
show_state: true
```

</details>
## 📈 Progress Gauge

Displays download progress as a circular gauge.

<details >

<summary> ℹ️ Code here</summary>

```yaml
type: gauge
entity: sensor.synology_download_station_download_progress
name: Download Progress
min: 0
max: 100
severity:
  green: 80
  yellow: 50
  red: 0
needle: true
```

</details>

## 🚀 Statistics Card

Modern cards with integrated graphs (requires `statistic` configured on sensors).

<details >

<summary> ℹ️ Code here</summary>

```yaml
type: statistic
entity: sensor.synology_download_station_total_speed
period:
  calendar:
    period: hour
stat_type: mean
name: Average Speed
```

</details>

## 📋 Detailed Download List

Displays each download with all its information (like in the Synology interface).

### Version 1: Compact list with progress bars

<details >

<summary> ℹ️ Code here</summary>

```yaml
type: markdown
title: 📥 Active Downloads
content: |
  {% set downloads = state_attr('sensor.synology_download_station_active_downloads', 'downloads') %}
  {% if downloads and downloads|length > 0 %}
    {% for download in downloads %}
  <div style="background: rgba(100,100,100,0.2); padding: 10px; margin: 10px 0; border-radius: 8px;">
  <h3 style="margin: 0 0 10px 0; color: #fff;">📁 {{ download.title }}</h3>
  
  **Speed:** {{ (download.speed / (1024**2)) | round(2) }} MB/s | 
  **Status:** {{ download.status }} | 
  **Size:** {{ (download.size / (1024**3)) | round(2) }} GB | 
  **Progress:** {{ download.progress | round(1) }}%
  
  **Downloaded:** {{ (download.downloaded / (1024**3)) | round(2) }} GB
  
  <div style="background: rgba(50,50,50,0.5); height: 20px; border-radius: 10px; overflow: hidden; margin-top: 10px;">
    <div style="background: linear-gradient(90deg, #4CAF50, #8BC34A); height: 100%; width: {{ download.progress }}%; transition: width 0.3s;"></div>
  </div>
  </div>
    {% endfor %}
  {% else %}
  <div style="text-align: center; padding: 20px; color: #999;">
  *No active downloads*
  </div>
  {% endif %}
```

</details>

### Version 2: Detailed table style

<details >

<summary> ℹ️ Code here</summary>

```yaml
type: markdown
title: 📥 Downloads in Progress
content: |
  {% set downloads = state_attr('sensor.synology_download_station_active_downloads', 'downloads') %}
  {% if downloads and downloads|length > 0 %}
  | File | Speed | Status | Size | Downloaded | Progress |
  |------|-------|--------|------|------------|----------|
    {% for download in downloads %}
  | {{ download.title[:30] }}... | {{ (download.speed / (1024**2)) | round(2) }} MB/s | {{ download.status }} | {{ (download.size / (1024**3)) | round(2) }} GB | {{ (download.downloaded / (1024**3)) | round(2) }} GB | {{ download.progress | round(1) }}% |
    {% endfor %}
  {% else %}
  *No active downloads*
  {% endif %}
```

</details>

### Version 3: Individual cards

<details >

<summary> ℹ️ Code here</summary>

```yaml
type: markdown
title: Downloads
content: |
  {% set downloads = state_attr('sensor.synology_download_station_active_downloads', 'downloads') %}
  {% if downloads and downloads|length > 0 %}
    {% for download in downloads %}
  ---
  ### 📥 {{ download.title }}
  
  | Info | Value |
  |------|-------|
  | **Speed** | {{ (download.speed / (1024**2)) | round(2) }} MB/s |
  | **Status** | {{ download.status }} |
  | **Size** | {{ (download.size / (1024**3)) | round(2) }} GB |
  | **Downloaded** | {{ (download.downloaded / (1024**3)) | round(2) }} GB |
  | **Progress** | {{ download.progress | round(1) }}% |
  
    {% endfor %}
  {% else %}
  *No active downloads*
  {% endif %}
```

</details>

### Version 4: Complete dashboard with integrated graph

<details >

<summary> ℹ️ Code here</summary>

```yaml
type: vertical-stack
cards:
  # Global summary
  - type: glance
    entities:
      - entity: sensor.synology_download_station_active_downloads
        name: Downloads
      - entity: sensor.synology_download_station_total_speed
        name: Total Speed
    
  # Download list
  - type: markdown
    title: 📋 Download Details
    content: |
      {% set downloads = state_attr('sensor.synology_download_station_active_downloads', 'downloads') %}
      {% if downloads and downloads|length > 0 %}
        {% for download in downloads %}
      <details style="background: rgba(100,100,100,0.2); padding: 10px; margin: 10px 0; border-radius: 8px;">
      <summary style="cursor: pointer; font-weight: bold; font-size: 16px;">
        📥 {{ download.title }} - {{ download.progress | round(1) }}%
      </summary>
      <div style="padding: 10px 0;">
        <table style="width: 100%; margin-top: 10px;">
          <tr>
            <td style="padding: 5px;"><strong>🚀 Speed:</strong></td>
            <td style="padding: 5px;">{{ (download.speed / (1024**2)) | round(2) }} MB/s</td>
          </tr>
          <tr>
            <td style="padding: 5px;"><strong>📊 Status:</strong></td>
            <td style="padding: 5px;">{{ download.status }}</td>
          </tr>
          <tr>
            <td style="padding: 5px;"><strong>💾 Size:</strong></td>
            <td style="padding: 5px;">{{ (download.size / (1024**3)) | round(2) }} GB</td>
          </tr>
          <tr>
            <td style="padding: 5px;"><strong>⬇️ Downloaded:</strong></td>
            <td style="padding: 5px;">{{ (download.downloaded / (1024**3)) | round(2) }} GB</td>
          </tr>
          <tr>
            <td style="padding: 5px;"><strong>📈 Progress:</strong></td>
            <td style="padding: 5px;">
              <div style="background: rgba(50,50,50,0.5); height: 20px; border-radius: 10px; overflow: hidden;">
                <div style="background: linear-gradient(90deg, #4CAF50, #8BC34A); height: 100%; width: {{ download.progress }}%;"></div>
              </div>
              {{ download.progress | round(1) }}%
            </td>
          </tr>
        </table>
      </div>
      </details>
        {% endfor %}
      {% else %}
      <div style="text-align: center; padding: 30px; color: #999;">
        ℹ️ No downloads in progress
      </div>
      {% endif %}
```

</details>

### Version 5: Modern style with icons and colors

<details >

<summary> ℹ️ Code here</summary>

```yaml
type: markdown
title: 📥 Download Station
content: |
  {% set downloads = state_attr('sensor.synology_download_station_active_downloads', 'downloads') %}
  {% if downloads and downloads|length > 0 %}
    {% for download in downloads %}
  <div style="background: linear-gradient(135deg, rgba(30,60,114,0.8) 0%, rgba(42,82,152,0.8) 100%); padding: 15px; margin: 15px 0; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
      <h3 style="margin: 0; color: #fff; flex: 1;">{{ download.title }}</h3>
      <span style="background: rgba(76,175,80,0.8); padding: 5px 15px; border-radius: 20px; font-weight: bold; color: #fff;">
        {{ download.progress | round(1) }}%
      </span>
    </div>
    
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 10px;">
      <div>
        <div style="color: #aaa; font-size: 12px;">SPEED</div>
        <div style="color: #fff; font-size: 18px; font-weight: bold;">{{ (download.speed / (1024**2)) | round(2) }} <span style="font-size: 12px;">MB/s</span></div>
      </div>
      <div>
        <div style="color: #aaa; font-size: 12px;">DOWNLOADED</div>
        <div style="color: #fff; font-size: 18px; font-weight: bold;">{{ (download.downloaded / (1024**3)) | round(2) }} <span style="font-size: 12px;">/ {{ (download.size / (1024**3)) | round(2) }} GB</span></div>
      </div>
    </div>
    
    <div style="background: rgba(0,0,0,0.3); height: 8px; border-radius: 10px; overflow: hidden;">
      <div style="background: linear-gradient(90deg, #4CAF50, #8BC34A); height: 100%; width: {{ download.progress }}%; transition: width 0.5s ease;"></div>
    </div>
  </div>
    {% endfor %}
  {% else %}
  <div style="text-align: center; padding: 40px; background: rgba(100,100,100,0.2); border-radius: 12px; color: #999;">
    <div style="font-size: 48px; margin-bottom: 10px;">✓</div>
    <div style="font-size: 18px;">No downloads in progress</div>
  </div>
  {% endif %}
```

</details>

### Version 6: Button-Card interactive (full width)

**⚠️ Requires [button-card](https://github.com/custom-cards/button-card) via HACS**

<details >

<summary> ℹ️ Code here</summary>

```yaml
type: custom:button-card
entity: sensor.synology_download_station_active_downloads
name: Synology Downloads
show_name: true
show_state: false
show_icon: true
icon: mdi:download
tap_action:
  action: none
styles:
  card:
    - width: 100%
    - height: auto
    - padding: 15px
    - background: rgba(30, 30, 30, 0.8)
    - border-radius: 12px
  icon:
    - color: var(--primary-color)
  name:
    - font-size: 18px
    - font-weight: bold
    - text-align: left
    - padding-bottom: 10px
custom_fields:
  downloads: |
    [[[
      const downloads = entity.attributes.downloads || [];
      
      // Function to automatically format size in MB or GB
      const formatSize = (bytes) => {
        const gb = bytes / (1024 ** 3);
        const mb = bytes / (1024 ** 2);
        if (gb >= 1) {
          return `${gb.toFixed(2)} GB`;
        } else {
          return `${mb.toFixed(2)} MB`;
        }
      };
      
      // Function to format speed
      const formatSpeed = (bytesPerSec) => {
        const mbps = bytesPerSec / (1024 ** 2);
        if (mbps >= 1) {
          return `${mbps.toFixed(2)} MB/s`;
        } else {
          const kbps = bytesPerSec / 1024;
          return `${kbps.toFixed(2)} KB/s`;
        }
      };
      
      if (downloads.length === 0) {
        return `
          <div style="
            padding: 30px; 
            text-align: center; 
            color: #888;
            background: rgba(100,100,100,0.1);
            border-radius: 8px;
            margin-top: 10px;
          ">
            <div style="font-size: 40px; margin-bottom: 10px;">✓</div>
            <div style="font-size: 14px;">No active downloads</div>
          </div>
        `;
      }
      
      return downloads.map(dl => `
        <div style="
          border: 1px solid rgba(255,255,255,0.1);
          border-radius: 10px;
          padding: 12px;
          margin: 8px 0;
          background: linear-gradient(135deg, rgba(30,60,114,0.6) 0%, rgba(42,82,152,0.6) 100%);
          position: relative;
          overflow: hidden;
        ">
          <!-- Background progress bar -->
          <div style="
            position: absolute;
            top: 0;
            left: 0;
            height: 100%;
            width: ${dl.progress.toFixed(2)}%;
            background: linear-gradient(90deg, rgba(76,175,80,0.3), rgba(139,195,74,0.3));
            transition: width 0.5s ease;
            z-index: 0;
          "></div>
          
          <!-- Content -->
          <div style="position: relative; z-index: 1;">
            <!-- Title and progress -->
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
              <div style="font-weight: bold; font-size: 13px; color: #fff; flex: 1; padding-right: 10px;">
                ${dl.title.length > 50 ? dl.title.substring(0, 50) + '...' : dl.title}
              </div>
              <div style="
                background: rgba(76,175,80,0.8);
                padding: 4px 12px;
                border-radius: 20px;
                font-weight: bold;
                font-size: 12px;
                color: #fff;
                white-space: nowrap;
              ">
                ${dl.progress.toFixed(2)}%
              </div>
            </div>
            
            <!-- Detailed information -->
            <div style="
              display: grid;
              grid-template-columns: repeat(3, 1fr);
              gap: 8px;
              font-size: 11px;
              color: #ddd;
            ">
              <div>
                <span style="color: #aaa;">⚡ Speed:</span><br/>
                <strong style="color: #fff;">${formatSpeed(dl.speed)}</strong>
              </div>
              <div>
                <span style="color: #aaa;">📁 Size:</span><br/>
                <strong style="color: #fff;">${formatSize(dl.size)}</strong>
              </div>
              <div>
                <span style="color: #aaa;">⬇️ Downloaded:</span><br/>
                <strong style="color: #fff;">${formatSize(dl.downloaded)}</strong>
              </div>
            </div>
            
            <!-- Visual progress bar -->
            <div style="
              height: 6px;
              background: rgba(0,0,0,0.3);
              border-radius: 10px;
              overflow: hidden;
              margin-top: 8px;
            ">
              <div style="
                height: 100%;
                width: ${dl.progress.toFixed(2)}%;
                background: linear-gradient(90deg, #4CAF50, #8BC34A);
                transition: width 0.5s ease;
              "></div>
            </div>
          </div>
        </div>
      `).join('');
    ]]]
card_size: auto
```

</details>

### Version 7: Mushroom Cards (Modern style)

**⚠️ Requires [mushroom](https://github.com/piitaya/lovelace-mushroom) via HACS**

<details >

<summary> ℹ️ Code here</summary>

```yaml
type: vertical-stack
cards:
  # Header with chip
  - type: custom:mushroom-title-card
    title: 📥 Download Station
    subtitle: Synology NAS
  
  # Global statistics
  - type: horizontal-stack
    cards:
      - type: custom:mushroom-entity-card
        entity: sensor.synology_download_station_active_downloads
        name: Active
        icon: mdi:download
        icon_color: blue
        layout: vertical
      - type: custom:mushroom-entity-card
        entity: sensor.synology_download_station_total_speed
        name: Speed
        icon: mdi:speedometer
        icon_color: green
        layout: vertical
      - type: custom:mushroom-entity-card
        entity: sensor.synology_download_station_download_progress
        name: Progress
        icon: mdi:progress-download
        icon_color: orange
        layout: vertical
  
  # Download list
  - type: markdown
    content: |
      {% set downloads = state_attr('sensor.synology_download_station_active_downloads', 'downloads') %}
      {% if downloads and downloads|length > 0 %}
        {% for download in downloads %}
      <ha-card style="background: var(--card-background-color); padding: 12px; margin: 8px 0; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
        <div style="display: flex; align-items: center; gap: 12px;">
          <div style="
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #4CAF50, #8BC34A);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
          ">📥</div>
          <div style="flex: 1;">
            <div style="font-weight: 600; font-size: 14px; margin-bottom: 4px;">
              {{ download.title[:45] }}...
            </div>
            <div style="font-size: 12px; color: var(--secondary-text-color); display: flex; gap: 12px;">
              <span>⚡ {{ (download.speed / (1024**2)) | round(2) }} MB/s</span>
              <span>📦 {{ (download.size / (1024**3)) | round(2) }} GB</span>
              <span style="color: #4CAF50; font-weight: bold;">{{ download.progress | round(1) }}%</span>
            </div>
          </div>
        </div>
        <div style="
          height: 4px;
          background: rgba(0,0,0,0.1);
          border-radius: 10px;
          overflow: hidden;
          margin-top: 8px;
        ">
          <div style="
            height: 100%;
            width: {{ download.progress }}%;
            background: linear-gradient(90deg, #4CAF50, #8BC34A);
          "></div>
        </div>
      </ha-card>
        {% endfor %}
      {% else %}
      <ha-card style="text-align: center; padding: 30px; background: var(--card-background-color);">
        <div style="font-size: 48px; margin-bottom: 10px;">✓</div>
        <div style="color: var(--secondary-text-color);">No downloads</div>
      </ha-card>
      {% endif %}
```

</details>

### Version 8: Auto-Entities with dynamic cards

**⚠️ Requires [auto-entities](https://github.com/thomasloven/lovelace-auto-entities) and [card-mod](https://github.com/thomasloven/lovelace-card-mod) via HACS**

<details >

<summary> ℹ️ Code here</summary>

```yaml
type: vertical-stack
cards:
  # Summary
  - type: custom:mod-card
    style: |
      ha-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
      }
    card:
      type: glance
      show_name: true
      show_icon: true
      show_state: true
      entities:
        - entity: sensor.synology_download_station_active_downloads
          name: Downloads
        - entity: sensor.synology_download_station_total_speed
          name: Speed
        - entity: sensor.synology_download_station_download_progress
          name: Progress
  
  # Auto-generation of related sensors
  - type: custom:auto-entities
    filter:
      include:
        - entity_id: sensor.synology_download_station_*
    card:
      type: entities
      title: All Sensors
```

</details>

### Version 9: Media Player Style (Elegant)

**⚠️ Requires [button-card](https://github.com/custom-cards/button-card) via HACS**

<details >

<summary> ℹ️ Code here</summary>

```yaml
type: custom:button-card
entity: sensor.synology_download_station_active_downloads
show_name: false
show_icon: false
show_state: false
styles:
  card:
    - width: 100%
    - height: auto
    - background: |
        [[[
          return 'linear-gradient(to bottom, rgba(20,20,20,0.95), rgba(30,30,30,0.95))';
        ]]]
    - border-radius: 16px
    - padding: 0
    - box-shadow: 0 8px 16px rgba(0,0,0,0.3)
custom_fields:
  header: |
    [[[
      return `
        <div style="
          padding: 20px;
          background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
          border-radius: 16px 16px 0 0;
        ">
          <div style="display: flex; align-items: center; gap: 15px;">
            <div style="
              width: 60px;
              height: 60px;
              background: rgba(255,255,255,0.2);
              border-radius: 12px;
              display: flex;
              align-items: center;
              justify-content: center;
              font-size: 30px;
            ">📥</div>
            <div style="flex: 1;">
              <div style="font-size: 20px; font-weight: bold; color: white; margin-bottom: 4px;">
                Download Station
              </div>
              <div style="font-size: 14px; color: rgba(255,255,255,0.8);">
                ${states['sensor.synology_download_station_active_downloads'].state} active download(s)
              </div>
            </div>
            <div style="text-align: right;">
              <div style="font-size: 24px; font-weight: bold; color: white;">
                ${states['sensor.synology_download_station_total_speed'].state}
              </div>
              <div style="font-size: 12px; color: rgba(255,255,255,0.8);">MB/s</div>
            </div>
          </div>
        </div>
      `;
    ]]]
  downloads: |
    [[[
      const downloads = entity.attributes.downloads || [];
      
      if (downloads.length === 0) {
        return `
          <div style="padding: 40px; text-align: center; color: #888;">
            <div style="font-size: 60px; margin-bottom: 15px;">✓</div>
            <div style="font-size: 16px;">All downloads completed</div>
          </div>
        `;
      }
      
      return downloads.map((dl, index) => {
        const sizeGb = (dl.size / (1024 ** 3)).toFixed(2);
        const downloadedGb = (dl.downloaded / (1024 ** 3)).toFixed(2);
        const speedMb = (dl.speed / (1024 ** 2)).toFixed(2);
        
        return `
          <div style="
            padding: 16px 20px;
            ${index < downloads.length - 1 ? 'border-bottom: 1px solid rgba(255,255,255,0.1);' : ''}
          ">
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;">
              <div style="flex: 1; padding-right: 15px;">
                <div style="color: white; font-weight: 500; font-size: 14px; margin-bottom: 6px; line-height: 1.4;">
                  ${dl.title}
                </div>
                <div style="display: flex; gap: 16px; font-size: 12px; color: rgba(255,255,255,0.6);">
                  <span>⚡ ${speedMb} MB/s</span>
                  <span>📦 ${downloadedGb} / ${sizeGb} GB</span>
                </div>
              </div>
              <div style="
                min-width: 60px;
                text-align: center;
                background: ${dl.progress >= 80 ? 'rgba(76,175,80,0.2)' : 'rgba(33,150,243,0.2)'};
                padding: 8px 12px;
                border-radius: 12px;
              ">
                <div style="font-size: 16px; font-weight: bold; color: ${dl.progress >= 80 ? '#4CAF50' : '#2196F3'};">
                  ${dl.progress.toFixed(1)}%
                </div>
              </div>
            </div>
            
            <div style="position: relative; height: 6px; background: rgba(255,255,255,0.1); border-radius: 10px; overflow: hidden;">
              <div style="
                position: absolute;
                height: 100%;
                width: ${dl.progress}%;
                background: linear-gradient(90deg, 
                  ${dl.progress >= 80 ? '#4CAF50, #8BC34A' : '#2196F3, #64B5F6'}
                );
                border-radius: 10px;
                transition: width 0.5s ease;
              "></div>
            </div>
          </div>
        `;
      }).join('');
    ]]]
```

</details>

### Version 10: Compact Grid Style

**⚠️ Requires [button-card](https://github.com/custom-cards/button-card) via HACS**

<details >

<summary> ℹ️ Code here</summary>

```yaml
type: custom:button-card
entity: sensor.synology_download_station_active_downloads
show_name: false
show_state: false
show_icon: false
styles:
  card:
    - width: 100%
    - padding: 16px
    - background: rgba(30,30,30,0.9)
    - border-radius: 16px
custom_fields:
  content: |
    [[[
      const downloads = entity.attributes.downloads || [];
      
      if (downloads.length === 0) {
        return `
          <div style="text-align: center; padding: 30px; color: #666;">
            <div style="font-size: 40px; margin-bottom: 10px;">💤</div>
            <div>No downloads</div>
          </div>
        `;
      }
      
      return `
        <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 12px;">
          ${downloads.map(dl => {
            const progress = dl.progress.toFixed(1);
            const speed = (dl.speed / (1024 ** 2)).toFixed(2);
            const size = (dl.size / (1024 ** 3)).toFixed(2);
            
            return `
              <div style="
                background: linear-gradient(135deg, rgba(50,50,70,0.8), rgba(40,40,60,0.8));
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 12px;
                padding: 14px;
                position: relative;
                overflow: hidden;
              ">
                <!-- Background progress -->
                <div style="
                  position: absolute;
                  top: 0;
                  left: 0;
                  width: ${progress}%;
                  height: 100%;
                  background: linear-gradient(90deg, rgba(76,175,80,0.15), rgba(139,195,74,0.15));
                  transition: width 0.5s;
                "></div>
                
                <!-- Content -->
                <div style="position: relative; z-index: 1;">
                  <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 10px;">
                    <div style="flex: 1; font-size: 13px; font-weight: 600; color: #fff; line-height: 1.3; padding-right: 10px;">
                      ${dl.title.length > 35 ? dl.title.substring(0, 35) + '...' : dl.title}
                    </div>
                    <div style="
                      background: linear-gradient(135deg, #4CAF50, #8BC34A);
                      padding: 4px 10px;
                      border-radius: 20px;
                      font-size: 11px;
                      font-weight: bold;
                      color: white;
                      white-space: nowrap;
                    ">${progress}%</div>
                  </div>
                  
                  <div style="
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 8px;
                    font-size: 11px;
                    color: rgba(255,255,255,0.7);
                    margin-bottom: 8px;
                  ">
                    <div>
                      <div style="color: rgba(255,255,255,0.5); margin-bottom: 2px;">Speed</div>
                      <div style="color: #4CAF50; font-weight: bold;">${speed} MB/s</div>
                    </div>
                    <div>
                      <div style="color: rgba(255,255,255,0.5); margin-bottom: 2px;">Size</div>
                      <div style="color: #2196F3; font-weight: bold;">${size} GB</div>
                    </div>
                  </div>
                  
                  <div style="
                    height: 4px;
                    background: rgba(0,0,0,0.3);
                    border-radius: 10px;
                    overflow: hidden;
                  ">
                    <div style="
                      height: 100%;
                      width: ${progress}%;
                      background: linear-gradient(90deg, #4CAF50, #8BC34A);
                      transition: width 0.5s;
                    "></div>
                  </div>
                </div>
              </div>
            `;
          }).join('')}
        </div>
      `;
    ]]]
```

</details>

### Version 11: Swipe Card (Horizontal navigation)

**⚠️ Requires [swipe-card](https://github.com/bramkragten/swipe-card) via HACS**

<details >

<summary> ℹ️ Code here</summary>

```yaml
type: custom:swipe-card
parameters:
  effect: coverflow
  grabCursor: true
  centeredSlides: true
  slidesPerView: auto
  coverflowEffect:
    rotate: 50
    stretch: 0
    depth: 100
    modifier: 1
    slideShadows: true
cards:
  - type: markdown
    content: |
      {% set downloads = state_attr('sensor.synology_download_station_active_downloads', 'downloads') %}
      {% if downloads and downloads|length > 0 %}
        {% for download in downloads %}
      <ha-card style="
        width: 300px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 16px;
        color: white;
      ">
        <div style="text-align: center;">
          <div style="font-size: 60px; margin-bottom: 10px;">📥</div>
          <div style="font-size: 16px; font-weight: bold; margin-bottom: 15px; line-height: 1.4;">
            {{ download.title[:40] }}...
          </div>
          
          <div style="
            width: 120px;
            height: 120px;
            margin: 20px auto;
            border-radius: 50%;
            background: conic-gradient(
              #4CAF50 {{ download.progress }}%,
              rgba(255,255,255,0.2) {{ download.progress }}%
            );
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
          ">
            <div style="
              width: 100px;
              height: 100px;
              background: rgba(0,0,0,0.3);
              border-radius: 50%;
              display: flex;
              align-items: center;
              justify-content: center;
              font-size: 24px;
              font-weight: bold;
            ">{{ download.progress | round(1) }}%</div>
          </div>
          
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 20px;">
            <div>
              <div style="font-size: 12px; opacity: 0.8;">Speed</div>
              <div style="font-size: 18px; font-weight: bold;">{{ (download.speed / (1024**2)) | round(2) }}</div>
              <div style="font-size: 10px; opacity: 0.8;">MB/s</div>
            </div>
            <div>
              <div style="font-size: 12px; opacity: 0.8;">Size</div>
              <div style="font-size: 18px; font-weight: bold;">{{ (download.size / (1024**3)) | round(2) }}</div>
              <div style="font-size: 10px; opacity: 0.8;">GB</div>
            </div>
          </div>
        </div>
      </ha-card>
        {% endfor %}
      {% else %}
      <ha-card style="width: 300px; text-align: center; padding: 40px;">
        <div style="font-size: 60px; margin-bottom: 10px;">✓</div>
        <div>No downloads</div>
      </ha-card>
      {% endif %}
```

</details>

### Version 12: Bar Card (Horizontal bars)

**⚠️ Requires [bar-card](https://github.com/custom-cards/bar-card) via HACS**

<details >

<summary> ℹ️ Code here</summary>

```yaml
type: vertical-stack
cards:
  # Header
  - type: markdown
    content: |
      <div style="text-align: center; padding: 10px; font-size: 20px; font-weight: bold;">
        📥 Download Station - {{ states('sensor.synology_download_station_active_downloads') }} download(s)
      </div>
  
  # List with bars
  - type: markdown
    content: |
      {% set downloads = state_attr('sensor.synology_download_station_active_downloads', 'downloads') %}
      {% if downloads and downloads|length > 0 %}
        {% for download in downloads %}
      <div style="background: rgba(50,50,50,0.3); padding: 12px; margin: 8px 0; border-radius: 10px;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
          <strong>{{ download.title[:40] }}...</strong>
          <span style="color: #4CAF50; font-weight: bold;">{{ download.progress | round(1) }}%</span>
        </div>
        
        <div style="
          height: 30px;
          background: linear-gradient(90deg, 
            #4CAF50 0%, 
            #4CAF50 {{ download.progress }}%, 
            rgba(100,100,100,0.3) {{ download.progress }}%, 
            rgba(100,100,100,0.3) 100%
          );
          border-radius: 8px;
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 0 12px;
          font-size: 12px;
          font-weight: bold;
          color: white;
          text-shadow: 0 1px 2px rgba(0,0,0,0.5);
        ">
          <span>⚡ {{ (download.speed / (1024**2)) | round(2) }} MB/s</span>
          <span>📦 {{ (download.size / (1024**3)) | round(2) }} GB</span>
        </div>
      </div>
        {% endfor %}
      {% endif %}
```

</details>

## 🔥 Mini Graph Card (Custom card)

Displays a graph of download speed over time.

**⚠️ Requires [mini-graph-card](https://github.com/kalkih/mini-graph-card) installation via HACS**

<details >

<summary> ℹ️ Code here</summary>

```yaml
type: custom:mini-graph-card
name: Download Speed
icon: mdi:speedometer
entities:
  - entity: sensor.synology_download_station_total_speed
    name: Speed
    color: '#3498db'
hours_to_show: 24
points_per_hour: 4
line_width: 3
font_size: 75
animate: true
show:
  name: true
  icon: true
  state: true
  legend: false
  fill: fade
```

</details>

## 📊 ApexCharts (Advanced custom card)

Advanced chart with multiple metrics.

**⚠️ Requires [apexcharts-card](https://github.com/RomRider/apexcharts-card) installation via HACS**

<details >

<summary> ℹ️ Code here</summary>

```yaml
type: custom:apexcharts-card
header:
  show: true
  title: Synology Download Station
  show_states: true
  colorize_states: true
graph_span: 24h
span:
  start: day
series:
  - entity: sensor.synology_download_station_total_speed
    name: Speed
    color: '#2196F3'
    stroke_width: 2
    type: area
    opacity: 0.3
    yaxis_id: speed
    group_by:
      func: avg
      duration: 5min
  - entity: sensor.synology_download_station_download_progress
    name: Progress
    color: '#4CAF50'
    stroke_width: 2
    type: line
    yaxis_id: progress
yaxis:
  - id: speed
    apex_config:
      tickAmount: 4
  - id: progress
    opposite: true
    min: 0
    max: 100
    apex_config:
      tickAmount: 4
```

</details>

## 🎯 Conditional Card

Displays an alert only when downloads are active.

<details >

<summary> ℹ️ Code here</summary>

```yaml
type: conditional
conditions:
  - entity: sensor.synology_download_station_active_downloads
    state_not: "0"
card:
  type: markdown
  content: |
    ## 🚀 Download in progress!
    
    **{{ states('sensor.synology_download_station_active_downloads') }}** file(s) downloading
    
    **Current speed:** {{ states('sensor.synology_download_station_total_speed') }} MB/s
    
    **Progress:** {{ states('sensor.synology_download_station_download_progress') }}%
  title: Download Station
```

</details>

## 🔔 Notification Card

Displays a banner at the top of the screen when a download is complete.

<details >

<summary> ℹ️ Code here</summary>

```yaml
type: conditional
conditions:
  - entity: sensor.synology_download_station_download_progress
    state: "100"
  - entity: sensor.synology_download_station_active_downloads
    state: "0"
card:
  type: markdown
  content: |
    ✅ **All downloads completed!**
    
    Total downloaded: {{ states('sensor.synology_download_station_total_downloaded') }} GB
  card_mod:
    style: |
      ha-card {
        background-color: #4CAF50;
        color: white;
        text-align: center;
      }
```

</details>

## 🎨 Complete Dashboard

A complete view combining multiple cards for a full overview.

<details >

<summary> ℹ️ Code here</summary>

```yaml
type: vertical-stack
cards:
  # Header with main statistics
  - type: glance
    title: Download Station - Overview
    entities:
      - entity: sensor.synology_download_station_active_downloads
        name: Active
      - entity: sensor.synology_download_station_active_uploads
        name: Seeds
      - entity: sensor.synology_download_station_total_speed
        name: Speed
    show_name: true
    show_icon: true
    show_state: true

  # Progress bar
  - type: custom:bar-card
    entity: sensor.synology_download_station_download_progress
    name: Overall Progress
    icon: mdi:progress-download
    positions:
      icon: inside
      indicator: inside
      name: inside
    height: 50px
    color: '#4CAF50'

  # Download details
  - type: markdown
    title: 📥 Active Downloads
    content: |
      {% set downloads = state_attr('sensor.synology_download_station_active_downloads', 'downloads') %}
      {% if downloads and downloads|length > 0 %}
        {% for download in downloads %}
      **{{ download.title }}**
      `{{ download.progress | round(1) }}%` • {{ (download.speed / (1024**2)) | round(2) }} MB/s
      ---
        {% endfor %}
      {% else %}
      *No downloads in progress*
      {% endif %}

  # Detailed information
  - type: entities
    title: Details
    entities:
      - entity: sensor.synology_download_station_total_downloaded
        name: Total Downloaded
        icon: mdi:download-network
      - entity: sensor.synology_download_station_total_size
        name: Total Size
        icon: mdi:harddisk
      - type: divider
      - entity: sensor.synology_download_station_active_uploads
        name: Files seeding
        icon: mdi:upload
```

</details>

## 💡 Usage Tips

### Data Refresh
Sensors update every **60 seconds** by default.

### Suggested Automations

**Notification when download completes:**

<details >

<summary> ℹ️ Code here</summary>

```yaml
alias: Download Completed Notification
trigger:
  - platform: state
    entity_id: sensor.synology_download_station_download_progress
    to: "100"
condition:
  - condition: state
    entity_id: sensor.synology_download_station_active_downloads
    state: "0"
action:
  - service: notify.mobile_app_your_phone
    data:
      title: "Download Station"
      message: "All downloads are complete!"
```
</details>

**Slow speed alert:**

<details >

<summary> ℹ️ Code here</summary>

```yaml
alias: Slow Download Speed Alert
trigger:
  - platform: numeric_state
    entity_id: sensor.synology_download_station_total_speed
    below: 1
    for:
      minutes: 5
condition:
  - condition: numeric_state
    entity_id: sensor.synology_download_station_active_downloads
    above: 0
action:
  - service: notify.mobile_app_your_phone
    data:
      title: "Download Station"
      message: "Download speed is abnormally low"
```

</details>

## 🎨 Customization with Card-mod

You can customize the appearance of any card with [card-mod](https://github.com/thomasloven/lovelace-card-mod).

**Example:**

<details >

<summary> ℹ️ Code here</summary>

```yaml
type: entities
title: Download Station
entities:
  - entity: sensor.synology_download_station_active_downloads
  - entity: sensor.synology_download_station_total_speed
card_mod:
  style: |
    ha-card {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      border-radius: 15px;
    }
```

</details>

**💡 Tip:** Combine multiple cards to create your custom dashboard!

**🇫🇷 Version française :** [LOVELACE_EXAMPLES.md](LOVELACE_EXAMPLES.md)

