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

## 📥 Détails des téléchargements actifs / Active Downloads Details

Affiche la liste complète des téléchargements en cours avec leurs détails.

*Displays the full list of ongoing downloads with their details.*

```yaml
type: markdown
title: Téléchargements en cours
content: |
  {% set downloads = state_attr('sensor.synology_download_station_active_downloads', 'downloads') %}
  {% if downloads and downloads|length > 0 %}
    {% for download in downloads %}
  ### 📥 {{ download.title }}
  - **Progression:** {{ download.progress | round(1) }}%
  - **Téléchargé:** {{ (download.downloaded / (1024**3)) | round(2) }} GB / {{ (download.size / (1024**3)) | round(2) }} GB
  - **Vitesse:** {{ (download.speed / (1024**2)) | round(2) }} MB/s
  - **Statut:** {{ download.status }}
  ---
    {% endfor %}
  {% else %}
  *Aucun téléchargement en cours*
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

