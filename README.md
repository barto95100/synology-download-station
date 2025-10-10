# Synology Download Station for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub Release](https://img.shields.io/github/v/release/VOTRE-USERNAME-GITHUB/synology-download-station)](https://github.com/VOTRE-USERNAME-GITHUB/synology-download-station/releases)
[![License](https://img.shields.io/github/license/VOTRE-USERNAME-GITHUB/synology-download-station)](LICENSE)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/VOTRE-USERNAME-GITHUB/synology-download-station/graphs/commit-activity)

> **Intégration Home Assistant pour surveiller Synology Download Station en temps réel.**

Monitor and track your Synology Download Station downloads directly from Home Assistant with real-time sensors and detailed statistics.

**Version française ci-dessous** | *French version below*

## Fonctionnalités

- 📊 **Capteurs en temps réel** :
  - Nombre de téléchargements actifs
  - Nombre de téléversements actifs (seeding)
  - Vitesse totale de téléchargement
  - Taille totale des téléchargements
  - Données téléchargées
  - Progression globale des téléchargements

- 🔄 **Mise à jour automatique** toutes les 30 secondes
- 🔐 **Authentification sécurisée** avec gestion des sessions
- 🌐 **Support SSL/HTTPS**
- 📝 **Détails des téléchargements** dans les attributs des capteurs

## Installation

### Méthode 1 : Installation manuelle

1. Copiez le dossier `synology_download_station` dans le répertoire `custom_components` de votre installation Home Assistant :
   ```
   /config/custom_components/synology_download_station/
   ```

2. Redémarrez Home Assistant

3. Ajoutez l'intégration via l'interface utilisateur :
   - Allez dans **Paramètres** → **Appareils et services**
   - Cliquez sur **+ Ajouter une intégration**
   - Recherchez "Synology Download Station"
   - Suivez les instructions de configuration

### Méthode 2 : Via HACS (à venir)

Cette intégration sera bientôt disponible via HACS.

## Configuration

Lors de l'ajout de l'intégration, vous devrez fournir :

- **Hôte** : Adresse IP ou nom d'hôte de votre NAS Synology (ex: `10.150.150.182`)
- **Port** : Port de l'API (par défaut `5000` pour HTTP, `5001` pour HTTPS)
- **SSL** : Cochez si vous utilisez HTTPS
- **Vérifier SSL** : Décochez si vous utilisez un certificat auto-signé
- **Nom d'utilisateur** : Votre nom d'utilisateur Synology
- **Mot de passe** : Votre mot de passe Synology

### Exemple de configuration

```
Hôte: 10.150.150.182
Port: 5000
SSL: Non
Vérifier SSL: Non
Nom d'utilisateur: multimedia
Mot de passe: votre_mot_de_passe
```

## Capteurs disponibles

Une fois configurée, l'intégration créera les capteurs suivants :

| Capteur | Description | Unité |
|---------|-------------|-------|
| `sensor.synology_download_station_active_downloads` | Nombre de téléchargements actifs | - |
| `sensor.synology_download_station_active_uploads` | Nombre de téléversements actifs | - |
| `sensor.synology_download_station_total_speed` | Vitesse totale de téléchargement | MB/s |
| `sensor.synology_download_station_total_size` | Taille totale des téléchargements | GB |
| `sensor.synology_download_station_total_downloaded` | Données téléchargées | GB |
| `sensor.synology_download_station_download_progress` | Progression globale | % |

## Exemples d'utilisation

### Carte Lovelace

```yaml
type: entities
title: Synology Download Station
entities:
  - entity: sensor.synology_download_station_active_downloads
    name: Téléchargements actifs
  - entity: sensor.synology_download_station_total_speed
    name: Vitesse
  - entity: sensor.synology_download_station_download_progress
    name: Progression
```

### Automation - Notification de téléchargement terminé

```yaml
automation:
  - alias: "Notification téléchargement terminé"
    trigger:
      - platform: state
        entity_id: sensor.synology_download_station_download_progress
        to: "100"
    action:
      - service: notify.mobile_app
        data:
          title: "Téléchargement terminé"
          message: "Tous vos téléchargements sont terminés !"
```

## Dépannage

### L'intégration ne se connecte pas

1. Vérifiez que votre NAS Synology est accessible depuis Home Assistant
2. Vérifiez les identifiants (nom d'utilisateur et mot de passe)
3. Vérifiez que Download Station est installé et démarré sur votre NAS
4. Si vous utilisez SSL, essayez de décocher "Vérifier SSL"

### Les capteurs ne se mettent pas à jour

1. Vérifiez les logs de Home Assistant pour voir les erreurs
2. Redémarrez l'intégration depuis **Paramètres** → **Appareils et services**

### Activer les logs de débogage

Ajoutez ceci dans votre `configuration.yaml` :

```yaml
logger:
  default: info
  logs:
    custom_components.synology_download_station: debug
```

## Support

Pour signaler un bug ou demander une fonctionnalité, veuillez ouvrir une issue sur GitHub.

## Licence

MIT License

## Crédits

Développé pour Home Assistant avec ❤️
