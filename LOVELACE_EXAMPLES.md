# Exemples de Cartes Lovelace

Ce document présente différents exemples de cartes pour afficher les données de votre Synology Download Station dans Home Assistant.

**🇬🇧 English version available:** [LOVELACE_EXAMPLES_EN.md](LOVELACE_EXAMPLES_EN.md)

---  


## 📋 Liste détaillée des téléchargements / Detailed Download List

Affiche chaque téléchargement avec toutes ses informations (comme dans l'interface Synology).


### Version 1 : Details telechargement avec collapse
  
![Alt text](/images%20card/image4.png "a title")

![Alt text](/images%20card/image5.png "a title")

![Alt text](/images%20card/image10.png "a title")
<details >

<summary> ℹ️ Code disponible</summary>

```yaml
type: markdown
title: 📋 Détails des téléchargements
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
        <td style="padding: 5px;"><strong>🚀 Vitesse:</strong></td>
        <td style="padding: 5px;">{{ (download.speed / (1024**2)) | round(2) }} MB/s</td>
      </tr>
      <tr>
        <td style="padding: 5px;"><strong>📊 Statut:</strong></td>
        <td style="padding: 5px;">{{ download.status }}</td>
      </tr>
      <tr>
        <td style="padding: 5px;"><strong>💾 Taille:</strong></td>
        <td style="padding: 5px;">{{ (download.size / (1024**3)) | round(2) }} GB</td>
      </tr>
      <tr>
        <td style="padding: 5px;"><strong>⬇️ Téléchargé:</strong></td>
        <td style="padding: 5px;">{{ (download.downloaded / (1024**3)) | round(2) }} GB</td>
      </tr>
      <tr>
        <td style="padding: 5px;"><strong>📈 Progression:</strong></td>
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
    ℹ️ Aucun téléchargement en cours
  </div>

  {% endif %}

```

</details>

### Version 2 : Carte Button-Card interactive 

**⚠️ Nécessite [button-card](https://github.com/custom-cards/button-card) via HACS**

![Alt text](/images%20card/image2.png "a title")


<details >

<summary> ℹ️ Code disponible</summary>

```yaml
type: custom:button-card
entity: sensor.synology_download_station_active_downloads
name: Téléchargements Synology
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
      
      // Fonction pour formater la taille automatiquement en Mo ou Go
      const formatSize = (bytes) => {
        const gb = bytes / (1024 ** 3);
        const mb = bytes / (1024 ** 2);
        if (gb >= 1) {
          return `${gb.toFixed(2)} Go`;
        } else {
          return `${mb.toFixed(2)} Mo`;
        }
      };
      
      // Fonction pour formater la vitesse
      const formatSpeed = (bytesPerSec) => {
        const mbps = bytesPerSec / (1024 ** 2);
        if (mbps >= 1) {
          return `${mbps.toFixed(2)} Mo/s`;
        } else {
          const kbps = bytesPerSec / 1024;
          return `${kbps.toFixed(2)} Ko/s`;
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
            <div style="font-size: 14px;">Aucun téléchargement actif</div>
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
          <!-- Barre de progression en arrière-plan -->
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
          
          <!-- Contenu -->
          <div style="position: relative; z-index: 1;">
            <!-- Titre et progression -->
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
            
            <!-- Informations détaillées -->
            <div style="
              display: grid;
              grid-template-columns: repeat(3, 1fr);
              gap: 8px;
              font-size: 11px;
              color: #ddd;
            ">
              <div>
                <span style="color: #aaa;">⚡ Vitesse:</span><br/>
                <strong style="color: #fff;">${formatSpeed(dl.speed)}</strong>
              </div>
              <div>
                <span style="color: #aaa;">📁 Taille:</span><br/>
                <strong style="color: #fff;">${formatSize(dl.size)}</strong>
              </div>
              <div>
                <span style="color: #aaa;">⬇️ Téléchargé:</span><br/>
                <strong style="color: #fff;">${formatSize(dl.downloaded)}</strong>
              </div>
            </div>
            
            <!-- Barre de progression visuelle -->
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


### Version 3 : Carte Button-Card interactive 

![Alt text](/images%20card/image3.png "a title")


<details >

<summary> ℹ️ Code disponible</summary>

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
        return '<div style="padding: 10px; text-align: center; color: #888;">Aucun téléchargement actif</div>';
      }

      return downloads.map(dl => {
        const percent = (typeof dl.progress === 'number' ? dl.progress : 0);
        const percentStr = percent.toFixed(1);
        const pctClamp = Math.min(Math.max(percent, 0), 100);

        const speed = (dl.speed / 1048576).toFixed(2);

        // Calcul taille dynamique
        let sizeStr = '';
        if (dl.size >= 1073741824) { // 1 Go = 1024*1024*1024 = 1073741824 octets
          sizeStr = (dl.size / 1073741824).toFixed(2) + ' Go';
        } else {
          sizeStr = (dl.size / 1048576).toFixed(0) + ' Mo';
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
            <span>⚡ ${speed} Mo/s</span>
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

### Version 4 : Carte Button-Card interactive 

![Alt text](/images%20card/image6.png "a title")


<details >

<summary> ℹ️ Code disponible</summary>

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
            <div>Aucun téléchargement</div>
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
                      <div style="color: rgba(255,255,255,0.5); margin-bottom: 2px;">Vitesse</div>
                      <div style="color: #4CAF50; font-weight: bold;">${speed} Mo/s</div>
                    </div>
                    <div>
                      <div style="color: rgba(255,255,255,0.5); margin-bottom: 2px;">Taille</div>
                      <div style="color: #2196F3; font-weight: bold;">${size} Go</div>
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

### Version 5 : Carte Button-Card interactive 

![Alt text](/images%20card/image8.png "a title")

![Alt text](/images%20card/image9.png "a title")

<details >

<summary> ℹ️ Code disponible</summary>

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
                ${states['sensor.synology_download_station_active_downloads'].state} téléchargement(s) actif(s)
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
            <div style="font-size: 16px;">Tous les téléchargements sont terminés</div>
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
                    <span>⚡ ${speedMb} Mo/s</span>
                    <span>📦 ${downloadedGb} / ${sizeGb} Go</span>
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


### Version 6 : markdown  / Verticales card 

**⚠️ Nécessite [bar-card](https://github.com/custom-cards/bar-card) via HACS**


![Alt text](/images%20card/image7.png "a title")

<details >

<summary> ℹ️ Code disponible</summary>

```yaml
type: vertical-stack
cards:
  # En-tête
  - type: markdown
    content: |
      <div style="text-align: center; padding: 10px; font-size: 20px; font-weight: bold;">
        📥 Download Station - {{ states('sensor.synology_download_station_active_downloads') }} téléchargement(s)
        📤 {{ states('sensor.synology_download_station_active_uploads') }} upload(s)/seeding
      </div>
      <div style="text-align: center; padding: 5px; font-size: 14px; color: #888;">
        📥 {{ states('sensor.synology_download_station_total_download_speed') }} MB/s | 
        📤 {{ states('sensor.synology_download_station_total_upload_speed') }} MB/s
      </div>
  
  # Liste avec barres
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
          <span>⚡ {{ (download.speed / (1024**2)) | round(2) }} Mo/s</span>
          <span>📦 {{ (download.size / (1024**3)) | round(2) }} Go</span>
        </div>
      </div>
        {% endfor %}
      {% endif %}
```

</details>


### Version 7 : Carte conditionnelle

Affiche une alerte uniquement si des téléchargements sont actifs.

![Alt text](/images%20card/image1.png "a title")


<details >

<summary> ℹ️ Code disponible</summary>

```yaml
type: conditional
conditions:
  - entity: sensor.synology_download_station_active_downloads
    state_not: "0"
card:
  type: markdown
  content: |
    ## 🚀 Téléchargement en cours !
    
    **{{ states('sensor.synology_download_station_active_downloads') }}** fichier(s) en téléchargement
    **{{ states('sensor.synology_download_station_active_uploads') }}** fichier(s) en upload/seeding
    
    **📥 Vitesse Download:** {{ states('sensor.synology_download_station_total_download_speed') }} MB/s
    **📤 Vitesse Upload:** {{ states('sensor.synology_download_station_total_upload_speed') }} MB/s
    
    **Progression:** {{ states('sensor.synology_download_station_download_progress') }}%
  title: Download Station
```

</details>




### Actualisation des données
Les capteurs se mettent à jour toutes les **60 secondes** par défaut.

### Automatisations suggérées

**Notification quand un téléchargement est terminé:**
<details >

<summary> ℹ️ Code disponible</summary>

```yaml
alias: Notification téléchargement terminé
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
      message: "Tous les téléchargements sont terminés !"
```
</details>



**Alerte vitesse lente:**

<details >

<summary> ℹ️ Code disponible</summary>

```yaml
alias: Alerte vitesse de téléchargement lente
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
      message: "La vitesse de téléchargement est anormalement basse"
```

</details>



Vous pouvez personnaliser l'apparence de n'importe quelle carte avec [card-mod](https://github.com/thomasloven/lovelace-card-mod).

**Exemple:**

<details >

<summary> ℹ️ Code disponible</summary>

```yaml
type: entities
title: Download Station
entities:
  - entity: sensor.synology_download_station_active_downloads
  - entity: sensor.synology_download_station_active_uploads
  - entity: sensor.synology_download_station_total_download_speed
  - entity: sensor.synology_download_station_total_upload_speed
card_mod:
  style: |
    ha-card {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      border-radius: 15px;
    }
```

</details>

## 8. Carte de vitesses combinées (Download + Upload)

### 8.1 Carte simple avec vitesses côte à côte

```yaml
type: horizontal-stack
cards:
  - type: gauge
    entity: sensor.synology_download_station_total_download_speed
    name: Vitesse Download
    min: 0
    max: 50
    severity:
      green: 0
      yellow: 20
      red: 40
    needle: true
  - type: gauge
    entity: sensor.synology_download_station_total_upload_speed
    name: Vitesse Upload
    min: 0
    max: 20
    severity:
      green: 0
      yellow: 10
      red: 15
    needle: true
```

### 8.2 Carte personnalisée avec graphique des vitesses

```yaml
type: custom:apexcharts-card
header:
  show: true
  title: "Vitesses Download/Upload"
  show_states: true
  colorize_states: true
graph_span: 24h
span:
  start: day
series:
  - entity: sensor.synology_download_station_total_download_speed
    name: "Download"
    color: "#2196F3"
    stroke_width: 2
    type: area
    opacity: 0.3
    group_by:
      func: avg
      duration: 5min
  - entity: sensor.synology_download_station_total_upload_speed
    name: "Upload"
    color: "#4CAF50"
    stroke_width: 2
    type: area
    opacity: 0.3
    group_by:
      func: avg
      duration: 5min
yaxis:
  - id: speed
    apex_config:
      tickAmount: 4
```

### 8.3 Carte Mushroom avec vitesses

```yaml
type: custom:mushroom-entity-card
entity: sensor.synology_download_station_total_download_speed
name: "Synology Download Station"
secondary_info: |
  📥 {{ states('sensor.synology_download_station_total_download_speed') }} MB/s
  📤 {{ states('sensor.synology_download_station_total_upload_speed') }} MB/s
  📊 {{ states('sensor.synology_download_station_active_downloads') }} actifs
  🌱 {{ states('sensor.synology_download_station_active_uploads') }} seeds
icon: mdi:download-network
icon_color: blue
```

### 8.4 Carte de statistiques complètes

```yaml
type: custom:button-card
entity: sensor.synology_download_station_active_downloads
name: "Synology Download Station"
show_name: false
show_state: false
show_icon: true
icon: mdi:download-network
styles:
  card:
    - height: auto
    - padding: 15px
  name:
    - font-size: 18px
    - font-weight: bold
    - color: white
custom_fields:
  stats: |
    [[[
      const downloadSpeed = states['sensor.synology_download_station_total_download_speed'].state;
      const uploadSpeed = states['sensor.synology_download_station_total_upload_speed'].state;
      const activeDownloads = states['sensor.synology_download_station_active_downloads'].state;
      const activeUploads = states['sensor.synology_download_station_active_uploads'].state;
      
      return `
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 10px;">
          <div style="background: linear-gradient(135deg, #2196F3, #1976D2); padding: 10px; border-radius: 8px; text-align: center;">
            <div style="font-size: 12px; opacity: 0.8;">📥 Download</div>
            <div style="font-size: 16px; font-weight: bold;">${downloadSpeed} MB/s</div>
          </div>
          <div style="background: linear-gradient(135deg, #4CAF50, #388E3C); padding: 10px; border-radius: 8px; text-align: center;">
            <div style="font-size: 12px; opacity: 0.8;">📤 Upload</div>
            <div style="font-size: 16px; font-weight: bold;">${uploadSpeed} MB/s</div>
          </div>
          <div style="background: linear-gradient(135deg, #FF9800, #F57C00); padding: 10px; border-radius: 8px; text-align: center;">
            <div style="font-size: 12px; opacity: 0.8;">⬇️ Actifs</div>
            <div style="font-size: 16px; font-weight: bold;">${activeDownloads}</div>
          </div>
          <div style="background: linear-gradient(135deg, #9C27B0, #7B1FA2); padding: 10px; border-radius: 8px; text-align: center;">
            <div style="font-size: 12px; opacity: 0.8;">🌱 Seeds</div>
            <div style="font-size: 16px; font-weight: bold;">${activeUploads}</div>
          </div>
        </div>
      `;
    ]]]
layout: vertical
```

</details>

\
**💡 Astuce:** Combinez plusieurs cartes pour créer votre tableau de bord personnalisé !
