# 🎉 COMMENCEZ ICI !

Bienvenue dans l'intégration **Synology Download Station** pour Home Assistant !

---

## 🚀 Installation en 3 étapes

### Étape 1 : Installer l'intégration

**Option A - Script automatique (recommandé)**
```bash
cd "/Users/l.ramos/Downloads/Integration Home assistant/Synology Download Station"
./install.sh
```

**Option B - Installation manuelle**
```bash
# Copiez le dossier dans custom_components de Home Assistant
cp -r "synology_download_station" /config/custom_components/
```

### Étape 2 : Redémarrer Home Assistant

Allez dans **Paramètres** → **Système** → **Redémarrer**

### Étape 3 : Configurer

1. **Paramètres** → **Appareils et services**
2. Cliquez sur **+ AJOUTER UNE INTÉGRATION**
3. Recherchez "**Synology Download Station**"
4. Remplissez :
   - **Hôte** : `10.150.150.182`
   - **Port** : `5000`
   - **SSL** : ☐ Non
   - **Vérifier SSL** : ☐ Non
   - **Nom d'utilisateur** : `multimedia`
   - **Mot de passe** : [votre mot de passe]

---

## 📚 Documentation disponible

| Fichier | Description | Quand l'utiliser |
|---------|-------------|------------------|
| **QUICKSTART.md** | Démarrage rapide | Pour commencer rapidement |
| **INSTALLATION_FR.md** | Guide détaillé | Si vous avez des problèmes |
| **README.md** | Documentation complète | Pour tout comprendre |
| **EXAMPLES.md** | Exemples avancés | Pour aller plus loin |
| **SUMMARY.md** | Résumé complet | Vue d'ensemble |
| **PROJECT_INFO.md** | Infos techniques | Pour les développeurs |

---

## ✅ Vérification rapide

Après l'installation, vérifiez que :

- [ ] Le dossier est dans `/config/custom_components/synology_download_station/`
- [ ] Home Assistant a été redémarré
- [ ] L'intégration apparaît dans la liste
- [ ] Vous pouvez configurer via l'interface (pas de YAML requis)
- [ ] 6 capteurs sont créés après la configuration

---

## 🎯 Prochaines étapes

### 1. Testez la connexion
Vérifiez que les capteurs se mettent à jour :
- `sensor.synology_download_station_active_downloads`
- `sensor.synology_download_station_total_speed`
- `sensor.synology_download_station_download_progress`

### 2. Créez une carte Lovelace
Copiez ce code dans une nouvelle carte :

```yaml
type: entities
title: 📥 Téléchargements
entities:
  - sensor.synology_download_station_active_downloads
  - sensor.synology_download_station_total_speed
  - sensor.synology_download_station_download_progress
```

### 3. Ajoutez une notification
Créez une automation pour être notifié :

```yaml
automation:
  - alias: "Téléchargement terminé"
    trigger:
      platform: state
      entity_id: sensor.synology_download_station_download_progress
      to: "100"
    action:
      service: notify.mobile_app
      data:
        title: "✅ Téléchargement terminé"
        message: "Tous vos téléchargements sont terminés !"
```

---

## 🆘 Besoin d'aide ?

### Problème courant #1 : L'intégration n'apparaît pas
**Solution** :
1. Vérifiez que les fichiers sont dans le bon dossier
2. Redémarrez Home Assistant
3. Videz le cache du navigateur (Ctrl+F5)

### Problème courant #2 : Erreur de connexion
**Solution** :
```bash
# Testez manuellement la connexion
curl -k "http://10.150.150.182:5000/webapi/auth.cgi?api=SYNO.API.Auth&version=3&method=login&account=multimedia&passwd=VOTRE_MOT_DE_PASSE&session=DownloadStation&format=cookie"
```

### Problème courant #3 : Erreur d'authentification
**Solution** :
- Vérifiez votre nom d'utilisateur et mot de passe
- Assurez-vous que le compte a accès à Download Station

---

## 📊 Capteurs créés

Une fois configurée, vous aurez accès à :

| Capteur | Description |
|---------|-------------|
| `active_downloads` | Nombre de téléchargements en cours |
| `active_uploads` | Nombre de torrents en seed |
| `total_speed` | Vitesse de téléchargement (MB/s) |
| `total_size` | Taille totale (GB) |
| `total_downloaded` | Données téléchargées (GB) |
| `download_progress` | Progression globale (%) |

---

## 🎨 Exemples rapides

### Carte avec jauge
```yaml
type: gauge
entity: sensor.synology_download_station_download_progress
name: Progression
min: 0
max: 100
```

### Notification intelligente
```yaml
automation:
  - alias: "Nouveau téléchargement"
    trigger:
      platform: state
      entity_id: sensor.synology_download_station_active_downloads
      from: "0"
    action:
      service: notify.mobile_app
      data:
        title: "📥 Nouveau téléchargement"
        message: "Un téléchargement a démarré"
```

---

## 🔧 Outils disponibles

### Script de validation
Vérifiez que tout est en ordre :
```bash
./validate.sh
```

### Script d'installation
Installation automatique :
```bash
./install.sh [chemin_config_optionnel]
```

---

## 💡 Conseils

1. **Mise à jour** : Les capteurs se mettent à jour toutes les 30 secondes
2. **Logs** : Consultez les logs HA en cas de problème
3. **Exemples** : Voir `EXAMPLES.md` pour des cas d'usage avancés
4. **Support** : La documentation complète est dans `README.md`

---

## 🎉 C'est parti !

Vous êtes maintenant prêt à utiliser l'intégration Synology Download Station !

**Questions fréquentes** : Voir `INSTALLATION_FR.md`  
**Exemples avancés** : Voir `EXAMPLES.md`  
**Infos techniques** : Voir `PROJECT_INFO.md`

---

**Bon téléchargement ! 📥**
