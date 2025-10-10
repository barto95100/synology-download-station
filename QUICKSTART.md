# 🚀 Démarrage Rapide

## Installation en 3 étapes

### 1️⃣ Copier l'intégration

```bash
# Copiez le dossier dans custom_components
cp -r synology_download_station /config/custom_components/
```

Ou utilisez le script d'installation :
```bash
./install.sh
```

### 2️⃣ Redémarrer Home Assistant

Allez dans **Paramètres** → **Système** → **Redémarrer**

### 3️⃣ Configurer l'intégration

1. **Paramètres** → **Appareils et services**
2. Cliquez sur **+ AJOUTER UNE INTÉGRATION**
3. Recherchez "**Synology Download Station**"
4. Remplissez le formulaire :
   - **Hôte** : `10.150.150.182`
   - **Port** : `5000`
   - **SSL** : Non
   - **Vérifier SSL** : Non
   - **Nom d'utilisateur** : `multimedia`
   - **Mot de passe** : votre mot de passe

## ✅ C'est fait !

Vous devriez maintenant voir 6 nouveaux capteurs dans Home Assistant :

- 📥 Téléchargements actifs
- 📤 Téléversements actifs
- ⚡ Vitesse totale
- 💾 Taille totale
- ✔️ Données téléchargées
- 📊 Progression

## 🎨 Ajouter une carte Lovelace

Copiez-collez ce code dans une nouvelle carte :

```yaml
type: entities
title: 📥 Synology Downloads
entities:
  - entity: sensor.synology_download_station_active_downloads
    name: En cours
    icon: mdi:download
  - entity: sensor.synology_download_station_total_speed
    name: Vitesse
    icon: mdi:speedometer
  - entity: sensor.synology_download_station_download_progress
    name: Progression
    icon: mdi:progress-download
```

## 🔔 Ajouter une notification

Créez une automation pour être notifié quand un téléchargement est terminé :

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
          title: "✅ Téléchargement terminé"
          message: "Tous vos téléchargements sont terminés !"
```

## ❓ Problèmes ?

- **L'intégration n'apparaît pas** → Redémarrez HA et videz le cache du navigateur
- **Erreur de connexion** → Vérifiez l'IP, le port et les identifiants
- **Erreur d'authentification** → Vérifiez votre nom d'utilisateur et mot de passe

Pour plus de détails, consultez [INSTALLATION_FR.md](INSTALLATION_FR.md)
