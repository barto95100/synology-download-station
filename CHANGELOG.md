# Changelog

All notable changes to this project will be documented in this file.

*Toutes les modifications notables de ce projet seront documentées dans ce fichier.*

---

## [1.0.0] - 2025-10-11

### Added / Ajouté
- ✨ Initial stable release / Première version stable
- 📊 6 real-time sensors for monitoring downloads / 6 capteurs temps réel pour surveiller les téléchargements
- 🔐 Secure authentication with session management / Authentification sécurisée avec gestion des sessions
- 🌐 SSL/HTTPS support / Support SSL/HTTPS
- 🔄 Automatic updates every 60 seconds / Mises à jour automatiques toutes les 60 secondes
- 📝 Detailed download information in sensor attributes / Informations détaillées dans les attributs
- 🌍 English and French translations / Traductions anglais et français

### Changed / Modifié
- ⏱️ Increased timeout from 10s to 60s for slow NAS / Timeout augmenté de 10s à 60s pour les NAS lents
- 🔄 Update interval changed from 30s to 60s / Intervalle de mise à jour passé de 30s à 60s
- 🚀 Optimized API requests (removed tracker data) / Requêtes API optimisées (données tracker retirées)

### Fixed / Corrigé
- 🐛 Session expiration handling / Gestion de l'expiration de session
- 🐛 Timeout errors on busy NAS / Erreurs timeout sur NAS occupé
- 🐛 JSON parsing with text/plain content-type / Parsing JSON avec content-type text/plain

---

## [0.1.0] - 2025-10-09

### Ajouté
- Intégration initiale pour Synology Download Station
- Support de l'authentification API Synology
- 6 capteurs pour surveiller les téléchargements :
  - Téléchargements actifs
  - Téléversements actifs (seeding)
  - Vitesse totale de téléchargement
  - Taille totale des téléchargements
  - Données téléchargées
  - Progression globale des téléchargements
- Configuration via l'interface utilisateur de Home Assistant
- Support SSL/HTTPS avec option de vérification de certificat
- Traductions en français et anglais
- Script d'installation automatique
- Documentation complète en français et anglais
- Mise à jour automatique toutes les 30 secondes
- Gestion automatique des sessions et reconnexion
- Attributs détaillés pour chaque capteur
- Support des certificats SSL auto-signés

### Fonctionnalités
- Interrogation de l'API Synology Download Station
- Calcul automatique des statistiques globales
- Affichage des détails de chaque téléchargement dans les attributs
- Gestion des erreurs et reconnexion automatique
- Compatible avec Home Assistant 2023.1.0+

### Documentation
- README.md avec guide complet
- INSTALLATION_FR.md avec instructions détaillées en français
- info.md pour l'affichage dans Home Assistant
- Exemples d'utilisation avec Lovelace et automations
