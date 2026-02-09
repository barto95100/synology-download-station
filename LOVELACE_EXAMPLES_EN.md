# Lovelace Card Examples

This document presents various card examples to display your Synology Download Station data in Home Assistant.

**🇫🇷 Version française disponible:** [LOVELACE_EXAMPLES.md](LOVELACE_EXAMPLES.md)

---  


## 📋 Detailed Download List

Displays each download with all its information (like in the Synology interface).


### Version 1: Download details with collapse
  
![Alt text](/images%20card/image4.png "a title")

![Alt text](/images%20card/image5.png "a title")

![Alt text](/images%20card/image10.png "a title")
<details >

<summary> ℹ️ Code available</summary>

```yaml
type: markdown
title: 📋 Download Details
content: >
  {% set downloads =
  state_attr('sensor.synology_download_station_active_downloads', 'downloads')
  %}

  {% if downloads and downloads|length > 0 %}
    {% for download in downloads %}
  <details style="background: rgba(100,100,100,0.2); padding: 10px; margin: 10px
  0; border-radius: 8px;">

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

### Version 2: Interactive Button-Card

**⚠️ Requires [button-card](https://github.com/custom-cards/button-card) via HACS**

![Alt text](/images%20card/image2.png "a title")


<details >

<summary> ℹ️ Code available</summary>

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


### Version 3: Interactive Button-Card

![Alt text](/images%20card/image3.png "a title")


<details >

<summary> ℹ️ Code available</summary>

```yaml
type: custom:button-card
entity: sensor.synology_download_station_active_downloads
show_state: false
show_name: false
show_icon: true
icon: mdi:download
styles:
  card:
    - height: auto
    - padding: 0 0 0 0
    - margin: 0
    - box-sizing: border-box
  name:
    - font-size: 20px
    - font-weight: bold
    - margin-bottom: 20px
custom_fields:
  downloads: |
    [[[
      const downloads = entity.attributes.downloads || [];
      if (downloads.length === 0) {
        return '<div style="padding: 10px; text-align: center; color: #888;">No active downloads</div>';
      }

      return downloads.map(dl => {
        const percent = (typeof dl.progress === 'number' ? dl.progress : 0);
        const percentStr = percent.toFixed(1);
        const pctClamp = Math.min(Math.max(percent, 0), 100);

        const speed = (dl.speed / 1048576).toFixed(2);

        // Dynamic size calculation
        let sizeStr = '';
        if (dl.size >= 1073741824) { // 1 GB = 1024*1024*1024 = 1073741824 bytes
          sizeStr = (dl.size / 1073741824).toFixed(2) + ' GB';
        } else {
          sizeStr = (dl.size / 1048576).toFixed(0) + ' MB';
        }

        return `
        <div style="
          width: 100%;
          border: 1px solid #444;
          border-radius: 8px;
          padding: 12px 8px 12px 8px;
          margin: 8px 0;
          background: #232323;
          color: white;
          box-sizing: border-box;
        ">
          <div style="font-weight:bold;font-size:15px;margin-bottom:10px;text-overflow:ellipsis;overflow:hidden;white-space:nowrap;max-width:100%;">
            ${dl.title.length > 50 ? dl.title.substring(0, 50) + '...' : dl.title}
          </div>
          <div style="
              width: 100%; 
              background: #282828; 
              border-radius: 6px; 
              height: 15px; 
              position: relative; 
              margin-bottom: 12px; 
              overflow: hidden;
            ">
            <div style="
              background: #39c447;
              width: ${pctClamp}%;
              height: 100%;
              border-radius: 6px;
              transition: width 0.5s;
              position: absolute; left: 0; top: 0;
            "></div>
            <span style="
              position: absolute;
              left: 50%; top: 50%; 
              transform: translate(-50%,-50%);
              font-size: 12px;
              color: white;
              font-weight: bold;
              z-index: 1;
              text-shadow: 1px 1px 2px #222;
            ">${percentStr}%</span>
          </div>
          <div style="display: flex; justify-content: space-between; font-size: 13px;">
            <span>⚡ ${speed} MB/s</span>
            <span>📁 ${sizeStr}</span>
            <span>📤 ${dl.status === 'downloading' ? '⬇️' : '🌱'}</span>
          </div>
        </div>
        `;
      }).join('');
    ]]]
layout: vertical

```

</details>

### Version 4: Interactive Button-Card

![Alt text](/images%20card/image6.png "a title")


<details >

<summary> ℹ️ Code available</summary>

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

### Version 5: Interactive Button-Card

![Alt text](/images%20card/image8.png "a title")

![Alt text](/images%20card/image9.png "a title")

<details >

<summary> ℹ️ Code available</summary>

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
    - background: 'linear-gradient(to bottom, rgba(20,20,20,0.95), rgba(30,30,30,0.95))'
    - border-radius: 16px
    - padding: 0
    - box-shadow: 0 8px 16px rgba(0,0,0,0.3)
  custom_fields:
    content:
      - padding: 0
custom_fields:
  content: |
    [[[
      const downloads = entity.attributes.downloads || [];
      
      // Header
      let output = `
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
                ${states['sensor.synology_download_station_total_download_speed'].state}
              </div>
              <div style="font-size: 12px; color: rgba(255,255,255,0.8);">MB/s</div>
            </div>
          </div>
        </div>
      `;
      
      // Downloads list
      if (downloads.length === 0) {
        output += `
          <div style="padding: 40px; text-align: center; color: #888;">
            <div style="font-size: 60px; margin-bottom: 15px;">✓</div>
            <div style="font-size: 16px;">All downloads completed</div>
          </div>
        `;
      } else {
        output += downloads.map((dl, index) => {
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
      }
      
      return output;
    ]]]

```

</details>


### Version 6: Markdown / Vertical Stack Card

**⚠️ Requires [bar-card](https://github.com/custom-cards/bar-card) via HACS**


![Alt text](/images%20card/image7.png "a title")

<details >

<summary> ℹ️ Code available</summary>

```yaml
type: vertical-stack
cards:
  # Header
  - type: markdown
    content: |
      <div style="text-align: center; padding: 10px; font-size: 20px; font-weight: bold;">
        📥 Download Station - {{ states('sensor.synology_download_station_active_downloads') }} download(s)
        📤 {{ states('sensor.synology_download_station_active_uploads') }} upload(s)/seeding
      </div>
      <div style="text-align: center; padding: 5px; font-size: 14px; color: #888;">
        📥 {{ states('sensor.synology_download_station_total_download_speed') }} MB/s | 
        📤 {{ states('sensor.synology_download_station_total_upload_speed') }} MB/s
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


### Version 7: Conditional Card

Displays an alert only when downloads are active.

![Alt text](/images%20card/image1.png "a title")


<details >

<summary> ℹ️ Code available</summary>

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
    **{{ states('sensor.synology_download_station_active_uploads') }}** file(s) uploading/seeding
    
    **📥 Download Speed:** {{ states('sensor.synology_download_station_total_download_speed') }} MB/s
    **📤 Upload Speed:** {{ states('sensor.synology_download_station_total_upload_speed') }} MB/s
    
    **Progress:** {{ states('sensor.synology_download_station_download_progress') }}%
  title: Download Station
```

</details>

### version 8 : Carte détail

Displays multiple cards with status, action, summary

Reduced menu:

![Alt text](/images%20card/image10.png "a title")

Expanded menu:

![Alt text](/images%20card/image11.png "a title")

<details >
  
<summary> ℹ️ Code available</summary>

```yaml
type: custom:mod-card
style: |
ha-card {
border-radius: 15px;
background: rgba(30,30,50,0.85);
box-shadow: 0 8px 20px rgba(0,0,0,0.4);
padding: 15px;
color: white;
}
card:
type: vertical-stack
cards:
- type: markdown
content: >
## 🖥️ Synology Download Station

    {% set d =
    states('sensor.synology_download_station_active_downloads')|int %}

    {% set u = states('sensor.synology_download_station_active_uploads')|int
    %}


    {% if d > 0 and u > 0 %}

    📥 **Downloads aktiv:** {{ d }} &nbsp;&nbsp; 📤 **Uploads:** {{ u }}

    {% elif d > 0 %}

    📥 **Downloads aktiv:** {{ d }}

    {% elif u > 0 %}

    📤 **Uploads:** {{ u }}

    {% endif %}


    🕒 **Gesamtfortschritt:** {{
    states('sensor.synology_download_station_download_progress') }} %  

    🌐 **Download Speed:** {{
    states('sensor.synology_download_station_total_download_speed') }}
    MB/s  

    ⬆️ **Upload Speed:** {{
    states('sensor.synology_download_station_total_upload_speed') }} MB/s
- type: markdown
  content: >
    {% set downloads =
    state_attr('sensor.synology_download_station_active_downloads',
    'downloads') or [] %}

    {% if downloads %}

    ### 📥 Aktive Downloads

    {% for d in downloads %}

    <details style="margin-bottom:10px; border-left: 4px solid #00BFFF;
    padding-left:5px;">

    <summary>📄 {{ d.title | default('Unbekannte Datei') }}</summary>

    🆔 ID: `{{ d.id }}` | 🔄 Status: {{ d.status }}<br>

    📊 Fortschritt: {{ d.progress | default('100') }} % | 💾 Gesamt: {{
    (d.size / 1024 / 1024 / 1024)|round(2) if d.size else '?' }} GB | ⬇️
    Geladen: {{ (d.downloaded / 1024 / 1024 / 1024)|round(2) if d.downloaded
    else '?' }} GB<br>

    🚀 Speed: {{ d.speed | default('0') }} MB/s

    </details>

    {% endfor %}

    {% else %}

    _Keine aktiven Downloads_

    {% endif %}
- type: markdown
  content: >
    {% set uploads =
    state_attr('sensor.synology_download_station_active_uploads',
    'downloads') or [] %}

    {% if uploads %}

    ### 📤 Aktive Uploads / Seeding

    {% for u in uploads %}

    <details style="margin-bottom:10px; border-left: 4px solid #32CD32;
    padding-left:5px;">

    <summary>📄 {{ u.title | default('Unbekannte Datei') }}</summary>

    🆔 ID: `{{ u.id }}` | 🔄 Status: {{ u.status }}<br>

    📊 Fortschritt: {{ u.progress | default('100') }} % | 💾 Gesamt: {{
    (u.size / 1024 / 1024 / 1024)|round(2) if u.size else '?' }} GB | ⬆️
    Hochgeladen: {{ (u.downloaded / 1024 / 1024 / 1024)|round(2) if
    u.downloaded else '?' }} GB

    </details>

    {% endfor %}

    {% else %}

    _Keine aktiven Uploads_

    {% endif %}
- type: horizontal-stack
  cards:
    - type: sensor
      entity: sensor.synology_download_station_total_download_speed
      graph: line
      name: ⬇️ Download Speed
      unit: MB/s
    - type: sensor
      entity: sensor.synology_download_station_total_upload_speed
      graph: line
      name: ⬆️ Upload Speed
      unit: MB/s
- type: horizontal-stack
  cards:
    - type: button
      name: ⏸ Pause alle
      icon: mdi:pause
      tap_action:
        action: call-service
        service: synology_download_station.task_control
        data:
          action: pause
          all: true
    - type: button
      name: ▶️ Resume alle
      icon: mdi:play
      tap_action:
        action: call-service
        service: synology_download_station.task_control
        data:
          action: resume
          all: true
    - type: button
      name: 🗑 Löschen alle
      icon: mdi:delete
      tap_action:
        action: call-service
        service: synology_download_station.task_control
        data:
          action: delete
          all: true
- type: entities
  title: ⚙️ Update Status
  entities:
    - entity: update.synology_download_station_update
      name: Version / Update
```

</details>



### Data Refresh
Sensors update every **60 seconds** by default.

### Suggested Automations

**Notification when download completes:**
<details >

<summary> ℹ️ Code available</summary>

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

<summary> ℹ️ Code available</summary>

```yaml
alias: Slow Download Speed Alert
trigger:
  - platform: numeric_state
    entity_id: sensor.synology_download_station_total_download_speed
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



\
**💡 Tip:** Combine multiple cards to create your custom dashboard!

**🇫🇷 Version française :** [LOVELACE_EXAMPLES.md](LOVELACE_EXAMPLES.md)
