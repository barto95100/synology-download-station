# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

---

## [1.2.0] - 2025-01-16

### ✨ Ajouté / Added
- **Service `task_control`** : Contrôle des tâches de téléchargement
  - Actions disponibles : `pause`, `resume`, `delete`
  - Support des IDs simples (2623) et complets (dbid_2623)
  - Gestion flexible des formats d'entrée (nombre, string, liste)
  - Possibilité de contrôler toutes les tâches avec `all: true`
- **IDs des tâches dans les attributs** : Les détails des tâches incluent maintenant l'ID pour le contrôle via le service

### 📚 Documentation
- Documentation complète du service `task_control` dans les README (FR et EN)
- Exemples d'utilisation du service avec tous les formats d'IDs supportés

---

## [1.1.0] - 2025-01-14

### ✨ Ajouté / Added
- **Nouveau capteur `total_upload_speed`** : Affiche la vitesse d'upload totale de Download Station en MB/s
- **API Statistiques** : Utilisation de `SYNO.DownloadStation.Statistic` pour obtenir les vitesses globales de download/upload
  - Plus précis que la somme des vitesses individuelles
  - Plus performant (une seule requête API au lieu de calculer sur chaque tâche)
  - Fallback automatique vers le calcul manuel si l'API Statistics n'est pas disponible
- **Service `task_control`** : Contrôle des tâches de téléchargement
  - Actions disponibles : `pause`, `resume`, `delete`
  - Support des IDs simples (2623) et complets (dbid_2623)
  - Gestion flexible des formats d'entrée (nombre, string, liste)
  - Possibilité de contrôler toutes les tâches avec `all: true`
- **IDs des tâches dans les attributs** : Les détails des tâches incluent maintenant l'ID pour le contrôle via le service

### 🔧 Modifié / Changed
- **⚠️ BREAKING CHANGE** : Le capteur `total_speed` est renommé en `total_download_speed` pour plus de cohérence
  - Ancien : `sensor.synology_download_station_total_speed`
  - Nouveau : `sensor.synology_download_station_total_download_speed`
  - **Action requise** : Mettez à jour vos dashboards et automations avec le nouveau nom
- Les logs incluent maintenant les vitesses de download et upload en MB/s pour faciliter le débogage

### 📚 Documentation
- Mise à jour des exemples Lovelace (FR et EN) avec les nouveaux noms de capteurs
- Ajout d'exemples pour le nouveau capteur d'upload
- Documentation complète du service `task_control` dans les README (FR et EN)
- Exemples d'utilisation du service avec tous les formats d'IDs supportés

---

## [1.0.0] - 2025-10-12

### 🎉 Première version publique

#### ✨ Ajouté / Added
- Surveillance des téléchargements actifs
- Surveillance des uploads/seeds actifs
- Capteur de vitesse totale de téléchargement
- Capteur de taille totale des téléchargements
- Capteur de données téléchargées
- Capteur de progression globale
- Support SSL avec option de vérification
- Gestion automatique des sessions (expiration après 8 minutes)
- Interface de configuration via UI (config flow)
- Logs de débogage détaillés
- Documentation bilingue (français/anglais)
- Exemples de cartes Lovelace (7 versions)
- Support des certificats auto-signés

#### 🔧 Technique / Technical
- DataUpdateCoordinator pour la récupération des données
- Intervalle de mise à jour : 60 secondes
- Timeout des requêtes : 60 secondes
- API Synology : SYNO.API.Auth v3 et SYNO.DownloadStation.Task v3
- Compatible Home Assistant 2025.10.0+

#### 📚 Documentation
- README.md (français)
- README_EN.md (anglais)
- LOVELACE_EXAMPLES.md (exemples de cartes FR)
- LOVELACE_EXAMPLES_EN.md (exemples de cartes EN)
- Templates d'issues GitHub (bug, feature request, question)
- Template de Pull Request

---

## Types de changements / Change Types

- `✨ Ajouté / Added` : nouvelles fonctionnalités
- `🔧 Modifié / Changed` : changements dans les fonctionnalités existantes
- `⚠️ Déprécié / Deprecated` : fonctionnalités bientôt supprimées
- `🗑️ Supprimé / Removed` : fonctionnalités supprimées
- `🐛 Corrigé / Fixed` : corrections de bugs
- `🔒 Sécurité / Security` : correctifs de sécurité

---

[1.2.0]: https://github.com/barto95100/synology-download-station/releases/tag/v1.2.0
[1.0.0]: https://github.com/barto95100/synology-download-station/releases/tag/v1.0.0

