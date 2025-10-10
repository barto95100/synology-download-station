# Guide d'installation - Synology Download Station pour Home Assistant

## 📋 Prérequis

- Home Assistant installé et fonctionnel
- Synology NAS avec Download Station installé
- Accès au répertoire de configuration de Home Assistant

## 🚀 Installation rapide

### Option 1 : Script d'installation automatique

```bash
# Rendez le script exécutable (si ce n'est pas déjà fait)
chmod +x install.sh

# Exécutez le script
./install.sh

# Ou spécifiez le chemin de votre config Home Assistant
./install.sh /chemin/vers/config
```

### Option 2 : Installation manuelle

1. **Accédez au répertoire de configuration de Home Assistant**
   
   Le répertoire se trouve généralement à :
   - Home Assistant OS / Supervised : `/config`
   - Home Assistant Core : `~/.homeassistant`
   - Docker : Le volume monté (souvent `/config`)

2. **Créez le dossier custom_components (s'il n'existe pas)**
   
   ```bash
   mkdir -p /config/custom_components
   ```

3. **Copiez l'intégration**
   
   ```bash
   cp -r synology_download_station /config/custom_components/
   ```

4. **Vérifiez la structure**
   
   Votre structure devrait ressembler à :
   ```
   /config/
   ├── blueprints/
   ├── custom_components/
   │   └── synology_download_station/
   │       ├── __init__.py
   │       ├── manifest.json
   │       ├── const.py
   │       ├── sensor.py
   │       ├── config_flow.py
   │       ├── strings.json
   │       └── translations/
   │           ├── en.json
   │           └── fr.json
   ├── configuration.yaml
   └── ...
   ```

## ⚙️ Configuration

1. **Redémarrez Home Assistant**
   - Allez dans **Paramètres** → **Système** → **Redémarrer**

2. **Ajoutez l'intégration**
   - Allez dans **Paramètres** → **Appareils et services**
   - Cliquez sur le bouton **+ AJOUTER UNE INTÉGRATION** en bas à droite
   - Recherchez "**Synology Download Station**"
   - Cliquez dessus

3. **Remplissez le formulaire de configuration**
   
   | Champ | Valeur | Exemple |
   |-------|--------|---------|
   | **Hôte** | Adresse IP de votre NAS | `10.150.150.182` |
   | **Port** | Port de l'API | `5000` (HTTP) ou `5001` (HTTPS) |
   | **SSL** | Utiliser HTTPS | ☐ Non (pour HTTP) |
   | **Vérifier SSL** | Vérifier le certificat | ☐ Non (si certificat auto-signé) |
   | **Nom d'utilisateur** | Votre compte Synology | `multimedia` |
   | **Mot de passe** | Votre mot de passe | `********` |

4. **Validez**
   - Cliquez sur **SOUMETTRE**
   - L'intégration devrait se connecter et créer les capteurs

## 📊 Vérification

Une fois l'intégration configurée, vous devriez voir 6 nouveaux capteurs :

- `sensor.synology_download_station_active_downloads` - Téléchargements actifs
- `sensor.synology_download_station_active_uploads` - Téléversements actifs
- `sensor.synology_download_station_total_speed` - Vitesse totale (MB/s)
- `sensor.synology_download_station_total_size` - Taille totale (GB)
- `sensor.synology_download_station_total_downloaded` - Téléchargé (GB)
- `sensor.synology_download_station_download_progress` - Progression (%)

## 🔍 Dépannage

### L'intégration n'apparaît pas dans la liste

1. Vérifiez que les fichiers sont bien dans `/config/custom_components/synology_download_station/`
2. Redémarrez Home Assistant
3. Videz le cache de votre navigateur (Ctrl+F5)

### Erreur "cannot_connect"

1. Vérifiez que votre NAS est accessible depuis Home Assistant :
   ```bash
   ping 10.150.150.182
   ```
2. Vérifiez que le port est correct (5000 pour HTTP, 5001 pour HTTPS)
3. Testez la connexion avec curl :
   ```bash
   curl -k "http://10.150.150.182:5000/webapi/auth.cgi?api=SYNO.API.Auth&version=3&method=login&account=multimedia&passwd=VOTRE_MOT_DE_PASSE&session=DownloadStation&format=cookie"
   ```

### Erreur "invalid_auth"

1. Vérifiez votre nom d'utilisateur et mot de passe
2. Assurez-vous que le compte a les droits d'accès à Download Station
3. Testez la connexion manuellement avec curl (voir ci-dessus)

### Les capteurs ne se mettent pas à jour

1. Consultez les logs : **Paramètres** → **Système** → **Journaux**
2. Activez les logs de débogage en ajoutant dans `configuration.yaml` :
   ```yaml
   logger:
     default: info
     logs:
       custom_components.synology_download_station: debug
   ```
3. Redémarrez Home Assistant et consultez les logs

## 📱 Exemples d'utilisation

### Carte simple

```yaml
type: entities
title: Téléchargements Synology
entities:
  - entity: sensor.synology_download_station_active_downloads
    name: En cours
  - entity: sensor.synology_download_station_total_speed
    name: Vitesse
  - entity: sensor.synology_download_station_download_progress
    name: Progression
```

### Notification de fin de téléchargement

```yaml
automation:
  - alias: "Notification téléchargement terminé"
    trigger:
      - platform: state
        entity_id: sensor.synology_download_station_active_downloads
        from: "1"
        to: "0"
    condition:
      - condition: state
        entity_id: sensor.synology_download_station_download_progress
        state: "100"
    action:
      - service: notify.mobile_app_votre_telephone
        data:
          title: "✅ Téléchargement terminé"
          message: "Tous vos téléchargements sont terminés sur le NAS !"
```

## 🆘 Support

Si vous rencontrez des problèmes :

1. Consultez les logs de Home Assistant
2. Vérifiez que Download Station fonctionne sur votre NAS
3. Testez la connexion API manuellement avec curl
4. Ouvrez une issue sur GitHub avec les logs

## 📝 Notes

- L'intégration interroge l'API toutes les 30 secondes
- Les mots de passe sont stockés de manière sécurisée dans Home Assistant
- L'intégration supporte SSL/HTTPS avec certificats auto-signés
- Compatible avec Home Assistant 2023.1.0 et supérieur
