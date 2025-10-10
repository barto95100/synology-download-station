# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

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
