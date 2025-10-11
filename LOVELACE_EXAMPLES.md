# Exemples de Cartes Lovelace / Lovelace Card Examples

Ce document présente différents exemples de cartes pour afficher les données de votre Synology Download Station dans Home Assistant.

*This document provides various card examples to display your Synology Download Station data in Home Assistant.*

---

## 📊 Vue d'ensemble simple / Simple Overview

Une carte simple affichant tous les capteurs principaux.

*A simple card displaying all main sensors.*

```yaml
type: entities
title: Synology Download Station
entities:
  - entity: sensor.synology_download_station_active_downloads
    name: Téléchargements actifs
    icon: mdi:download
  - entity: sensor.synology_download_station_total_speed
    name: Vitesse totale
    icon: mdi:speedometer
  - entity: sensor.synology_download_station_download_progress
    name: Progression
    icon: mdi:progress-download
  - entity: sensor.synology_download_station_total_downloaded
    name: Total téléchargé
    icon: mdi:download-network
  - entity: sensor.synology_download_station_total_size
    name: Taille totale
    icon: mdi:harddisk
```

---

## 🎯 Vue compacte avec icônes / Compact View with Icons

Affichage compact avec grandes icônes, parfait pour un tableau de bord.

*Compact display with large icons, perfect for a dashboard.*

```yaml
type: glance
title: Download Station
entities:
  - entity: sensor.synology_download_station_active_downloads
    name: Actifs
  - entity: sensor.synology_download_station_total_speed
    name: Vitesse
  - entity: sensor.synology_download_station_download_progress
    name: Progression
  - entity: sensor.synology_download_station_total_downloaded
    name: Téléchargé
show_name: true
show_icon: true
show_state: true
```

---

## 📈 Jauge de progression / Progress Gauge

Affiche la progression des téléchargements sous forme de jauge circulaire.

*Displays download progress as a circular gauge.*

```yaml
type: gauge
entity: sensor.synology_download_station_download_progress
name: Progression des téléchargements
min: 0
max: 100
severity:
  green: 80
  yellow: 50
  red: 0
needle: true
```

---

## 🚀 Carte de statistiques / Statistics Card

Cartes modernes avec graphique intégré (nécessite `statistic` configuré sur les capteurs).

*Modern cards with integrated graphs (requires `statistic` configured on sensors).*

```yaml
type: statistic
entity: sensor.synology_download_station_total_speed
period:
  calendar:
    period: hour
stat_type: mean
name: Vitesse moyenne
```

---

## 📋 Liste détaillée des téléchargements / Detailed Download List

Affiche chaque téléchargement avec toutes ses informations (comme dans l'interface Synology).

*Displays each download with all its information (like in the Synology interface).*

### Version 1 : Liste compacte avec barres de progression

```yaml
type: markdown
title: 📥 Téléchargements actifs
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
  *Aucun téléchargement en cours*
  </div>
  {% endif %}
```

---

### Version 2 : Style tableau détaillé

```yaml
type: markdown
title: 📥 Téléchargements en cours
content: |
  {% set downloads = state_attr('sensor.synology_download_station_active_downloads', 'downloads') %}
  {% if downloads and downloads|length > 0 %}
  | Fichier | Vitesse | Statut | Taille | Téléchargé | Progression |
  |---------|---------|--------|--------|------------|-------------|
    {% for download in downloads %}
  | {{ download.title[:30] }}... | {{ (download.speed / (1024**2)) | round(2) }} MB/s | {{ download.status }} | {{ (download.size / (1024**3)) | round(2) }} GB | {{ (download.downloaded / (1024**3)) | round(2) }} GB | {{ download.progress | round(1) }}% |
    {% endfor %}
  {% else %}
  *Aucun téléchargement en cours*
  {% endif %}
```

---

### Version 3 : Cartes individuelles avec custom:bar-card

**⚠️ Nécessite [bar-card](https://github.com/custom-cards/bar-card) via HACS**

```yaml
type: markdown
title: Téléchargements
content: |
  {% set downloads = state_attr('sensor.synology_download_station_active_downloads', 'downloads') %}
  {% if downloads and downloads|length > 0 %}
    {% for download in downloads %}
  ---
  ### 📥 {{ download.title }}
  
  | Info | Valeur |
  |------|--------|
  | **Vitesse** | {{ (download.speed / (1024**2)) | round(2) }} MB/s |
  | **Statut** | {{ download.status }} |
  | **Taille** | {{ (download.size / (1024**3)) | round(2) }} GB |
  | **Téléchargé** | {{ (download.downloaded / (1024**3)) | round(2) }} GB |
  | **Progression** | {{ download.progress | round(1) }}% |
  
    {% endfor %}
  {% else %}
  *Aucun téléchargement en cours*
  {% endif %}
```

---

### Version 4 : Dashboard complet avec graphique intégré

```yaml
type: vertical-stack
cards:
  # Résumé global
  - type: glance
    entities:
      - entity: sensor.synology_download_station_active_downloads
        name: Téléchargements
      - entity: sensor.synology_download_station_total_speed
        name: Vitesse totale
    
  # Liste des téléchargements
  - type: markdown
    title: 📋 Détails des téléchargements
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

---

### Version 5 : Style moderne avec icônes et couleurs

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
        <div style="color: #aaa; font-size: 12px;">VITESSE</div>
        <div style="color: #fff; font-size: 18px; font-weight: bold;">{{ (download.speed / (1024**2)) | round(2) }} <span style="font-size: 12px;">MB/s</span></div>
      </div>
      <div>
        <div style="color: #aaa; font-size: 12px;">TÉLÉCHARGÉ</div>
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
    <div style="font-size: 18px;">Aucun téléchargement en cours</div>
  </div>
  {% endif %}
```

---

### Version 6 : Carte Button-Card interactive (pleine largeur)

**⚠️ Nécessite [button-card](https://github.com/custom-cards/button-card) via HACS**

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

---

### Version 7 : Mushroom Cards (Style moderne)

**⚠️ Nécessite [mushroom](https://github.com/piitaya/lovelace-mushroom) via HACS**

```yaml
type: vertical-stack
cards:
  # En-tête avec chip
  - type: custom:mushroom-title-card
    title: 📥 Download Station
    subtitle: Synology NAS
  
  # Statistiques globales
  - type: horizontal-stack
    cards:
      - type: custom:mushroom-entity-card
        entity: sensor.synology_download_station_active_downloads
        name: Actifs
        icon: mdi:download
        icon_color: blue
        layout: vertical
      - type: custom:mushroom-entity-card
        entity: sensor.synology_download_station_total_speed
        name: Vitesse
        icon: mdi:speedometer
        icon_color: green
        layout: vertical
      - type: custom:mushroom-entity-card
        entity: sensor.synology_download_station_download_progress
        name: Progression
        icon: mdi:progress-download
        icon_color: orange
        layout: vertical
  
  # Liste des téléchargements
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
              <span>⚡ {{ (download.speed / (1024**2)) | round(2) }} Mo/s</span>
              <span>📦 {{ (download.size / (1024**3)) | round(2) }} Go</span>
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
        <div style="color: var(--secondary-text-color);">Aucun téléchargement</div>
      </ha-card>
      {% endif %}
```

---

### Version 8 : Auto-Entities avec cartes dynamiques

**⚠️ Nécessite [auto-entities](https://github.com/thomasloven/lovelace-auto-entities) et [card-mod](https://github.com/thomasloven/lovelace-card-mod) via HACS**

```yaml
type: vertical-stack
cards:
  # Résumé
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
          name: Téléchargements
        - entity: sensor.synology_download_station_total_speed
          name: Vitesse
        - entity: sensor.synology_download_station_download_progress
          name: Progression
  
  # Auto-génération des capteurs liés
  - type: custom:auto-entities
    filter:
      include:
        - entity_id: sensor.synology_download_station_*
    card:
      type: entities
      title: Tous les capteurs
```

---

### Version 9 : Style Media Player (Élégant)

**⚠️ Nécessite [button-card](https://github.com/custom-cards/button-card) via HACS**

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
                ${states['sensor.synology_download_station_active_downloads'].state} téléchargement(s) actif(s)
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
            <div style="font-size: 16px;">Tous les téléchargements sont terminés</div>
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
    ]]]
```

---

### Version 10 : Compact Grid Style (Grille compacte)

**⚠️ Nécessite [button-card](https://github.com/custom-cards/button-card) via HACS**

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

---

### Version 11 : Swipe Card (Navigation horizontale)

**⚠️ Nécessite [swipe-card](https://github.com/bramkragten/swipe-card) via HACS**

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
              <div style="font-size: 12px; opacity: 0.8;">Vitesse</div>
              <div style="font-size: 18px; font-weight: bold;">{{ (download.speed / (1024**2)) | round(2) }}</div>
              <div style="font-size: 10px; opacity: 0.8;">Mo/s</div>
            </div>
            <div>
              <div style="font-size: 12px; opacity: 0.8;">Taille</div>
              <div style="font-size: 18px; font-weight: bold;">{{ (download.size / (1024**3)) | round(2) }}</div>
              <div style="font-size: 10px; opacity: 0.8;">Go</div>
            </div>
          </div>
        </div>
      </ha-card>
        {% endfor %}
      {% else %}
      <ha-card style="width: 300px; text-align: center; padding: 40px;">
        <div style="font-size: 60px; margin-bottom: 10px;">✓</div>
        <div>Aucun téléchargement</div>
      </ha-card>
      {% endif %}
```

---

### Version 12 : Bar Card (Barres horizontales)

**⚠️ Nécessite [bar-card](https://github.com/custom-cards/bar-card) via HACS**

```yaml
type: vertical-stack
cards:
  # En-tête
  - type: markdown
    content: |
      <div style="text-align: center; padding: 10px; font-size: 20px; font-weight: bold;">
        📥 Download Station - {{ states('sensor.synology_download_station_active_downloads') }} téléchargement(s)
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

---

## 🎨 Dashboard complet / Complete Dashboard

Une vue complète combinant plusieurs cartes pour un aperçu complet.

*A complete view combining multiple cards for a full overview.*

```yaml
type: vertical-stack
cards:
  # En-tête avec statistiques principales
  - type: glance
    title: Download Station - Vue d'ensemble
    entities:
      - entity: sensor.synology_download_station_active_downloads
        name: Actifs
      - entity: sensor.synology_download_station_active_uploads
        name: Seeds
      - entity: sensor.synology_download_station_total_speed
        name: Vitesse
    show_name: true
    show_icon: true
    show_state: true

  # Barre de progression
  - type: custom:bar-card
    entity: sensor.synology_download_station_download_progress
    name: Progression globale
    icon: mdi:progress-download
    positions:
      icon: inside
      indicator: inside
      name: inside
    height: 50px
    color: '#4CAF50'

  # Détails des téléchargements
  - type: markdown
    title: 📥 Téléchargements actifs
    content: |
      {% set downloads = state_attr('sensor.synology_download_station_active_downloads', 'downloads') %}
      {% if downloads and downloads|length > 0 %}
        {% for download in downloads %}
      **{{ download.title }}**
      `{{ download.progress | round(1) }}%` • {{ (download.speed / (1024**2)) | round(2) }} MB/s
      ---
        {% endfor %}
      {% else %}
      *Aucun téléchargement en cours*
      {% endif %}

  # Informations détaillées
  - type: entities
    title: Détails
    entities:
      - entity: sensor.synology_download_station_total_downloaded
        name: Total téléchargé
        icon: mdi:download-network
      - entity: sensor.synology_download_station_total_size
        name: Taille totale
        icon: mdi:harddisk
      - type: divider
      - entity: sensor.synology_download_station_active_uploads
        name: Fichiers en seed
        icon: mdi:upload
```

---

## 🔥 Mini Graph Card (Carte personnalisée)

Affiche un graphique de la vitesse de téléchargement dans le temps.

*Displays a graph of download speed over time.*

**⚠️ Nécessite l'installation de [mini-graph-card](https://github.com/kalkih/mini-graph-card) via HACS**

*⚠️ Requires [mini-graph-card](https://github.com/kalkih/mini-graph-card) installation via HACS*

```yaml
type: custom:mini-graph-card
name: Vitesse de téléchargement
icon: mdi:speedometer
entities:
  - entity: sensor.synology_download_station_total_speed
    name: Vitesse
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

---

## 📊 ApexCharts (Carte personnalisée avancée)

Graphique avancé avec plusieurs métriques.

*Advanced chart with multiple metrics.*

**⚠️ Nécessite l'installation de [apexcharts-card](https://github.com/RomRider/apexcharts-card) via HACS**

*⚠️ Requires [apexcharts-card](https://github.com/RomRider/apexcharts-card) installation via HACS*

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
    name: Vitesse
    color: '#2196F3'
    stroke_width: 2
    type: area
    opacity: 0.3
    yaxis_id: speed
    group_by:
      func: avg
      duration: 5min
  - entity: sensor.synology_download_station_download_progress
    name: Progression
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

---

## 🎯 Carte conditionnelle / Conditional Card

Affiche une alerte uniquement si des téléchargements sont actifs.

*Displays an alert only when downloads are active.*

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
    
    **Vitesse actuelle:** {{ states('sensor.synology_download_station_total_speed') }} MB/s
    
    **Progression:** {{ states('sensor.synology_download_station_download_progress') }}%
  title: Download Station
```

---

## 🔔 Carte de notification / Notification Card

Affiche une bannière en haut de l'écran quand un téléchargement est terminé.

*Displays a banner at the top of the screen when a download is complete.*

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
    ✅ **Tous les téléchargements sont terminés !**
    
    Total téléchargé: {{ states('sensor.synology_download_station_total_downloaded') }} GB
  card_mod:
    style: |
      ha-card {
        background-color: #4CAF50;
        color: white;
        text-align: center;
      }
```

---

## 💡 Conseils d'utilisation / Usage Tips

### Actualisation des données / Data Refresh
Les capteurs se mettent à jour toutes les **60 secondes** par défaut.

*Sensors update every **60 seconds** by default.*

### Automatisations suggérées / Suggested Automations

**Notification quand un téléchargement est terminé:**
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

**Alerte vitesse lente:**
```yaml
alias: Alerte vitesse de téléchargement lente
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
      message: "La vitesse de téléchargement est anormalement basse"
```

---

## 🎨 Personnalisation avec Card-mod

Vous pouvez personnaliser l'apparence de n'importe quelle carte avec [card-mod](https://github.com/thomasloven/lovelace-card-mod).

*You can customize the appearance of any card with [card-mod](https://github.com/thomasloven/lovelace-card-mod).*

**Exemple:**
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

---

**💡 Astuce:** Combinez plusieurs cartes pour créer votre tableau de bord personnalisé !

**💡 Tip:** Combine multiple cards to create your custom dashboard!

