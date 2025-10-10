# 📚 Exemples d'utilisation avancés

## 🎨 Cartes Lovelace

### Carte simple avec icônes
```yaml
type: entities
title: 📥 Synology Downloads
show_header_toggle: false
entities:
  - entity: sensor.synology_download_station_active_downloads
    name: Téléchargements actifs
    icon: mdi:download-circle
  - entity: sensor.synology_download_station_active_uploads
    name: Partages actifs
    icon: mdi:upload-circle
  - entity: sensor.synology_download_station_total_speed
    name: Vitesse
    icon: mdi:speedometer
  - entity: sensor.synology_download_station_download_progress
    name: Progression
    icon: mdi:progress-download
```

### Carte avec barre de progression
```yaml
type: vertical-stack
cards:
  - type: entities
    title: 📥 Téléchargements Synology
    entities:
      - entity: sensor.synology_download_station_active_downloads
        name: En cours
      - entity: sensor.synology_download_station_total_speed
        name: Vitesse
  - type: gauge
    entity: sensor.synology_download_station_download_progress
    name: Progression globale
    min: 0
    max: 100
    severity:
      green: 90
      yellow: 50
      red: 0
```

### Carte avec graphique
```yaml
type: vertical-stack
cards:
  - type: entities
    title: 📊 Statistiques
    entities:
      - sensor.synology_download_station_active_downloads
      - sensor.synology_download_station_total_speed
      - sensor.synology_download_station_total_size
  - type: history-graph
    title: Vitesse de téléchargement
    hours_to_show: 24
    entities:
      - sensor.synology_download_station_total_speed
```

### Carte conditionnelle (affiche seulement si téléchargements actifs)
```yaml
type: conditional
conditions:
  - entity: sensor.synology_download_station_active_downloads
    state_not: "0"
card:
  type: entities
  title: 📥 Téléchargements en cours
  entities:
    - sensor.synology_download_station_active_downloads
    - sensor.synology_download_station_total_speed
    - sensor.synology_download_station_download_progress
```

### Carte Markdown personnalisée
```yaml
type: markdown
content: |
  ## 📥 Synology Download Station
  
  **Téléchargements actifs:** {{ states('sensor.synology_download_station_active_downloads') }}
  
  **Vitesse:** {{ states('sensor.synology_download_station_total_speed') }} MB/s
  
  **Progression:** {{ states('sensor.synology_download_station_download_progress') }}%
  
  {% if states('sensor.synology_download_station_active_downloads')|int > 0 %}
  🟢 Téléchargement en cours...
  {% else %}
  ⚪ Aucun téléchargement
  {% endif %}
```

---

## 🤖 Automations

### Notification quand un téléchargement commence
```yaml
automation:
  - alias: "Notification nouveau téléchargement"
    trigger:
      - platform: state
        entity_id: sensor.synology_download_station_active_downloads
        from: "0"
    action:
      - service: notify.mobile_app
        data:
          title: "📥 Nouveau téléchargement"
          message: "Un téléchargement a démarré sur le NAS"
```

### Notification quand tous les téléchargements sont terminés
```yaml
automation:
  - alias: "Notification téléchargements terminés"
    trigger:
      - platform: state
        entity_id: sensor.synology_download_station_active_downloads
        to: "0"
        for:
          seconds: 30
    condition:
      - condition: state
        entity_id: sensor.synology_download_station_download_progress
        state: "100"
    action:
      - service: notify.mobile_app
        data:
          title: "✅ Téléchargements terminés"
          message: "Tous vos téléchargements sont terminés sur le NAS !"
          data:
            actions:
              - action: "OPEN_NAS"
                title: "Ouvrir le NAS"
```

### Notification avec détails de vitesse
```yaml
automation:
  - alias: "Notification vitesse élevée"
    trigger:
      - platform: numeric_state
        entity_id: sensor.synology_download_station_total_speed
        above: 10
    action:
      - service: notify.mobile_app
        data:
          title: "⚡ Vitesse élevée"
          message: >
            Téléchargement à {{ states('sensor.synology_download_station_total_speed') }} MB/s
            ({{ states('sensor.synology_download_station_active_downloads') }} fichiers)
```

### Allumer une LED quand téléchargement actif
```yaml
automation:
  - alias: "LED téléchargement actif"
    trigger:
      - platform: state
        entity_id: sensor.synology_download_station_active_downloads
    action:
      - choose:
          - conditions:
              - condition: numeric_state
                entity_id: sensor.synology_download_station_active_downloads
                above: 0
            sequence:
              - service: light.turn_on
                target:
                  entity_id: light.led_bureau
                data:
                  color_name: blue
                  brightness: 128
        default:
          - service: light.turn_off
            target:
              entity_id: light.led_bureau
```

### Pause des téléchargements la nuit (avec script externe)
```yaml
automation:
  - alias: "Pause téléchargements la nuit"
    trigger:
      - platform: time
        at: "23:00:00"
    condition:
      - condition: numeric_state
        entity_id: sensor.synology_download_station_active_downloads
        above: 0
    action:
      - service: notify.mobile_app
        data:
          title: "🌙 Pause des téléchargements"
          message: "Les téléchargements seront mis en pause à 23h"
```

### Notification quotidienne des statistiques
```yaml
automation:
  - alias: "Statistiques quotidiennes"
    trigger:
      - platform: time
        at: "20:00:00"
    condition:
      - condition: numeric_state
        entity_id: sensor.synology_download_station_total_downloaded
        above: 0
    action:
      - service: notify.mobile_app
        data:
          title: "📊 Statistiques du jour"
          message: >
            Téléchargé aujourd'hui: {{ states('sensor.synology_download_station_total_downloaded') }} GB
            Vitesse moyenne: {{ states('sensor.synology_download_station_total_speed') }} MB/s
```

---

## 📊 Templates et sensors personnalisés

### Sensor pour le temps restant estimé
```yaml
template:
  - sensor:
      - name: "Synology Download ETA"
        unit_of_measurement: "min"
        state: >
          {% set speed = states('sensor.synology_download_station_total_speed')|float %}
          {% set remaining = states('sensor.synology_download_station_total_size')|float - states('sensor.synology_download_station_total_downloaded')|float %}
          {% if speed > 0 %}
            {{ ((remaining * 1024) / speed / 60)|round(0) }}
          {% else %}
            0
          {% endif %}
        icon: mdi:timer-sand
```

### Sensor pour le statut textuel
```yaml
template:
  - sensor:
      - name: "Synology Download Status"
        state: >
          {% set active = states('sensor.synology_download_station_active_downloads')|int %}
          {% if active > 0 %}
            Téléchargement en cours ({{ active }} fichier{{ 's' if active > 1 else '' }})
          {% else %}
            Aucun téléchargement
          {% endif %}
        icon: >
          {% if states('sensor.synology_download_station_active_downloads')|int > 0 %}
            mdi:download
          {% else %}
            mdi:download-off
          {% endif %}
```

### Binary sensor pour téléchargement actif
```yaml
template:
  - binary_sensor:
      - name: "Synology Downloading"
        state: >
          {{ states('sensor.synology_download_station_active_downloads')|int > 0 }}
        device_class: running
```

---

## 🎯 Scripts

### Script pour afficher les détails
```yaml
script:
  show_download_details:
    alias: "Afficher détails téléchargements"
    sequence:
      - service: persistent_notification.create
        data:
          title: "📥 Détails des téléchargements"
          message: >
            **Téléchargements actifs:** {{ states('sensor.synology_download_station_active_downloads') }}
            
            **Vitesse:** {{ states('sensor.synology_download_station_total_speed') }} MB/s
            
            **Taille totale:** {{ states('sensor.synology_download_station_total_size') }} GB
            
            **Téléchargé:** {{ states('sensor.synology_download_station_total_downloaded') }} GB
            
            **Progression:** {{ states('sensor.synology_download_station_download_progress') }}%
```

---

## 📱 Notifications avancées

### Notification avec image et actions
```yaml
automation:
  - alias: "Notification complète téléchargement"
    trigger:
      - platform: state
        entity_id: sensor.synology_download_station_download_progress
        to: "100"
    action:
      - service: notify.mobile_app
        data:
          title: "✅ Téléchargement terminé"
          message: "{{ states('sensor.synology_download_station_total_size') }} GB téléchargés"
          data:
            image: "/local/synology_logo.png"
            actions:
              - action: "OPEN_DOWNLOADS"
                title: "Voir les fichiers"
              - action: "DISMISS"
                title: "OK"
            tag: "download_complete"
            color: "#00ff00"
```

---

## 🎨 Thème personnalisé

### Couleurs conditionnelles
```yaml
type: entities
title: 📥 Downloads
entities:
  - entity: sensor.synology_download_station_total_speed
    name: Vitesse
    style: |
      :host {
        {% if states('sensor.synology_download_station_total_speed')|float > 10 %}
          --paper-item-icon-color: green;
        {% elif states('sensor.synology_download_station_total_speed')|float > 5 %}
          --paper-item-icon-color: orange;
        {% else %}
          --paper-item-icon-color: red;
        {% endif %}
      }
```

---

## 💡 Conseils d'utilisation

1. **Surveillance continue** : Utilisez les graphiques d'historique pour suivre les tendances
2. **Notifications intelligentes** : Ajoutez des conditions pour éviter les notifications inutiles
3. **Automatisation** : Créez des scénarios basés sur l'état des téléchargements
4. **Intégration** : Combinez avec d'autres intégrations (Plex, Sonarr, Radarr, etc.)
5. **Dashboard dédié** : Créez un tableau de bord spécifique pour vos téléchargements

---

## 🔗 Intégrations complémentaires

Ces intégrations fonctionnent bien avec Synology Download Station :

- **Plex** : Notification quand un média est téléchargé
- **Sonarr/Radarr** : Automatisation des téléchargements
- **Telegram/Discord** : Notifications sur mobile
- **Node-RED** : Automatisations complexes
- **InfluxDB/Grafana** : Statistiques avancées
