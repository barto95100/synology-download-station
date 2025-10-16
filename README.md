# Synology Download Station for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub Release](https://img.shields.io/github/v/release/barto95100/synology-download-station)](https://github.com/barto95100/synology-download-station/releases)
[![License](https://img.shields.io/github/license/barto95100/synology-download-station)](LICENSE)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/barto95100/synology-download-station/graphs/commit-activity)

Intégration Home Assistant pour surveiller et contrôler Synology Download Station en temps réel.

> 🇬🇧 [English version / Version anglaise](README_EN.md)

---

## ✨ Fonctionnalités

- 📊 **Capteurs en temps réel** :
  - Nombre de téléchargements actifs
  - Nombre de téléversements actifs (seeding)
  - Vitesse totale de téléchargement
  - Taille totale des téléchargements
  - Données téléchargées
  - Progression globale des téléchargements

- 🔄 **Mise à jour automatique** toutes les 60 secondes
- 🔐 **Authentification sécurisée** avec gestion des sessions
- 🌐 **Support SSL/HTTPS**
- 📝 **Détails des téléchargements** dans les attributs des capteurs
- 🎮 **Service de contrôle** pour mettre en pause, reprendre ou supprimer les tâches

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

### Méthode 2 : Via HACS (recommandé)

#### Option A : Installation depuis HACS (dépôt personnalisé)

En attendant l'approbation officielle dans HACS, vous pouvez installer l'intégration comme dépôt personnalisé :

1. Ouvrez HACS dans Home Assistant
2. Cliquez sur les **⋮** (trois points en haut à droite)
3. Sélectionnez **Dépôts personnalisés**
4. Ajoutez l'URL du dépôt :
   ```
   https://github.com/barto95100/synology-download-station
   ```
5. Sélectionnez la catégorie : **Integration**
6. Cliquez sur **Ajouter**
7. Recherchez "Synology Download Station" dans HACS
8. Cliquez sur **Télécharger**
9. Redémarrez Home Assistant
10. Ajoutez l'intégration via **Paramètres** → **Appareils et services** → **+ Ajouter une intégration**

#### Option B : Depuis le store HACS par défaut

L'intégration est en cours de soumission au store HACS par défaut. Une fois approuvée, elle sera directement disponible dans HACS sans configuration supplémentaire.

## Configuration

Lors de l'ajout de l'intégration, vous devrez fournir :

- **Hôte** : Adresse IP ou nom d'hôte de votre NAS Synology (ex: `192.168.1.10`)
- **Port** : Port de l'API (par défaut `5000` pour HTTP, `5001` pour HTTPS)
- **SSL** : Cochez si vous utilisez HTTPS
- **Vérifier SSL** : Décochez si vous utilisez un certificat auto-signé
- **Nom d'utilisateur** : Votre nom d'utilisateur Synology
- **Mot de passe** : Votre mot de passe Synology

### Exemple de configuration

```
Hôte: 192.168.1.10
Port: 5000
SSL: Non
Vérifier SSL: Non
Nom d'utilisateur: votre_utilisateur
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

## Services disponibles

L'intégration fournit un service pour contrôler les tâches de téléchargement :

### `synology_download_station.task_control`

Ce service permet de mettre en pause, reprendre ou supprimer des tâches de téléchargement.

#### Paramètres

| Paramètre | Type | Requis | Description |
|-----------|------|--------|-------------|
| `action` | string | Oui | Action à effectuer : `pause`, `resume`, ou `delete` |
| `ids` | number/string/list | Non* | ID(s) de la/des tâche(s) à contrôler |
| `all` | boolean | Non | Si `true`, applique l'action à toutes les tâches |

*`ids` est requis sauf si `all=true`

#### Formats d'ID acceptés

Le service accepte plusieurs formats pour les IDs :

- **Nombre simple** : `2623`
- **String simple** : `"2623"`
- **Liste de nombres** : `[2623, 2624, 2625]`
- **Liste de strings** : `["2623", "2624", "2625"]`
- **Format complet** : `"dbid_2623"`

#### Exemples d'utilisation

**Mettre en pause une tâche spécifique :**
```yaml
service: synology_download_station.task_control
data:
  action: pause
  ids: 2623
```

**Reprendre plusieurs tâches :**
```yaml
service: synology_download_station.task_control
data:
  action: resume
  ids: [2623, 2624, 2625]
```

**Supprimer toutes les tâches :**
```yaml
service: synology_download_station.task_control
data:
  action: delete
  all: true
```

**Mettre en pause toutes les tâches :**
```yaml
service: synology_download_station.task_control
data:
  action: pause
  all: true
```

#### Trouver les IDs des tâches

Les IDs des tâches sont disponibles dans les attributs des capteurs :

1. Allez dans **Paramètres** → **Entités**
2. Recherchez `sensor.synology_download_station_active_downloads`
3. Cliquez sur le capteur
4. Dans l'attribut `downloads`, vous verrez la liste des tâches avec leurs IDs

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

**📖 Pour plus d'exemples de cartes (jauges, graphiques, cartes personnalisées, etc.), consultez le fichier [LOVELACE_EXAMPLES.md](LOVELACE_EXAMPLES.md) !**

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

Développé pour Home Assistant avec ❤️ par HACF
(Home Assistant Communauté Francophone)
* site: https://hacf.fr
* forum: https://forum.hacf.fr