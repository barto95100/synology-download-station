# 📁 Structure GitHub/HACS Recommandée

## ✅ Fichiers à GARDER sur GitHub

### 📄 Documentation essentielle

```
✓ README.md                 - Description principale (✅ amélioré)
✓ CHANGELOG.md              - Historique des versions
✓ CONTRIBUTING.md           - Guide contributeurs (✅ créé)
✓ LICENSE                   - Licence MIT
✓ .gitignore                - Fichiers à ignorer (✅ créé)
```

### 🔧 Fichiers d'intégration

```
✓ __init__.py               - Code principal
✓ sensor.py                 - Sensors
✓ const.py                  - Constantes
✓ config_flow.py            - Configuration UI
✓ strings.json              - Traductions UI
✓ manifest.json             - Métadonnées
```

### 🌐 Traductions

```
✓ translations/
  ✓ en.json                 - Anglais
  ✓ fr.json                 - Français
```

### 🎨 Ressources

```
✓ icons/
  ✓ icon.svg                - Icône de l'intégration
```

### 📦 HACS

```
✓ hacs.json                 - Configuration HACS
✓ info.md                   - Info affichée dans HACS
```

---

## ❌ Fichiers à EXCLURE (déjà dans .gitignore)

### 🛠️ Scripts de développement

```
✗ dev-start.sh              - Script Python dev
✗ docker-dev.sh             - Script Docker dev
✗ clean-all.sh              - Script nettoyage
✗ Makefile                  - Commandes dev
✗ docker-compose.dev.yml    - Config Docker dev
```

### 📚 Documentation dev locale

```
✗ DEV_SETUP.md              - À mettre dans Wiki GitHub
✗ QUICKSTART_MACOS.md       - À mettre dans Wiki GitHub
✗ DOCKER_VS_PYTHON.md       - À mettre dans Wiki GitHub
✗ LISEZMOI.md               - Redondant avec README
✗ START_HERE.txt            - Dev local uniquement
```

### 📁 Dossiers dev

```
✗ ha-dev-config/            - Config dev Docker
✗ ha-dev-db/                - DB dev
✗ __pycache__/              - Cache Python
✗ .vscode/                  - Config IDE
```

---

## 🎯 Structure finale sur GitHub

```
synology-download-station/
├── 📄 README.md                    ⭐ Description principale
├── 📄 CHANGELOG.md                 ⭐ Historique versions
├── 📄 CONTRIBUTING.md              ⭐ Guide contributeurs
├── 📄 LICENSE                      ⭐ Licence
├── 📄 .gitignore                   ⭐ Fichiers ignorés
│
├── 📦 HACS
│   ├── hacs.json                   ⭐ Config HACS
│   └── info.md                     ⭐ Info HACS
│
├── 🔧 Integration Files
│   ├── __init__.py                 ⭐ Code principal
│   ├── sensor.py                   ⭐ Sensors
│   ├── const.py                    ⭐ Constantes
│   ├── config_flow.py              ⭐ Config UI
│   ├── strings.json                ⭐ Traductions UI
│   └── manifest.json               ⭐ Métadonnées
│
├── 🌐 Translations
│   └── translations/
│       ├── en.json                 ⭐ Anglais
│       └── fr.json                 ⭐ Français
│
├── 🎨 Icons
│   └── icons/
│       └── icon.svg                ⭐ Icône
│
└── 📚 (Optionnel)
    ├── .github/                    - Workflows CI/CD
    │   └── workflows/
    │       └── validate.yaml       - Validation auto
    └── docs/                       - Documentation extra
        └── development.md          - Guide dev
```

---

## 📝 Fichiers à CRÉER avant publication

### 1. .github/workflows/validate.yaml (optionnel)

Validation automatique des PR :

```yaml
name: Validate

on:
  pull_request:
  push:
    branches:
      - main

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install pylint mypy
      - name: Lint with pylint
        run: pylint *.py
      - name: Type check with mypy
        run: mypy *.py
```

---

## 🚀 Checklist avant publication sur GitHub

### Étape 1 : Nettoyage

```bash
# Supprimer les fichiers de dev (déjà dans .gitignore)
rm -rf ha-dev-config/ ha-dev-db/
rm -f dev-start.sh docker-dev.sh clean-all.sh
rm -f START_HERE.txt LISEZMOI.md
```

### Étape 2 : Vérification des fichiers

```bash
# Vérifier ce qui sera commité
git status

# Devrait montrer uniquement les fichiers essentiels
```

### Étape 3 : Mise à jour des URLs

Dans **README.md**, remplacer :
```markdown
votre-username
```
Par votre vrai nom d'utilisateur GitHub.

### Étape 4 : Vérifier manifest.json

```json
{
  "domain": "synology_download_station",
  "name": "Synology Download Station",
  "documentation": "https://github.com/VOTRE-USERNAME/synology-download-station",
  "issue_tracker": "https://github.com/VOTRE-USERNAME/synology-download-station/issues",
  "codeowners": ["@VOTRE-USERNAME"],
  "version": "1.0.0"
}
```

### Étape 5 : Vérifier hacs.json

```json
{
  "name": "Synology Download Station",
  "render_readme": true,
  "domains": ["sensor"]
}
```

---

## 📦 Checklist HACS

Pour être accepté dans HACS, vérifier :

- [ ] Repository public sur GitHub
- [ ] README.md complet avec badges
- [ ] CHANGELOG.md présent
- [ ] LICENSE présent (MIT recommandé)
- [ ] hacs.json présent et valide
- [ ] info.md présent
- [ ] manifest.json avec toutes les infos
- [ ] Code suit les standards Home Assistant
- [ ] Au moins 1 release/tag (ex: v1.0.0)
- [ ] Documentation claire d'installation
- [ ] Exemples de configuration

---

## 🎨 Améliorer la présentation

### Ajouter des screenshots

Créer un dossier `docs/images/` avec :
- Screenshot de la configuration
- Screenshot des sensors dans HA
- Screenshot d'une carte Lovelace

Puis les ajouter dans le README :

```markdown
## Screenshots

### Configuration
![Configuration](docs/images/config.png)

### Sensors
![Sensors](docs/images/sensors.png)

### Lovelace Card
![Card](docs/images/card.png)
```

---

## ⚡ Prochaines étapes

1. **Nettoyer le repo** : 
   ```bash
   git rm DEV_SETUP.md QUICKSTART_MACOS.md DOCKER_VS_PYTHON.md
   git commit -m "chore: remove dev documentation from repo"
   ```

2. **Créer un Wiki GitHub** pour la documentation dev

3. **Créer la première release** :
   ```bash
   git tag -a v1.0.0 -m "First release"
   git push origin v1.0.0
   ```

4. **Soumettre à HACS** via : https://github.com/hacs/default

---

## 💡 Conseils

### Repository Name
Utilisez : `synology-download-station` (kebab-case)

### Branch principale
Utilisez `main` (pas `master`)

### Versioning
Suivez [Semantic Versioning](https://semver.org/) :
- v1.0.0 : Première version stable
- v1.0.1 : Bug fix
- v1.1.0 : Nouvelle fonctionnalité
- v2.0.0 : Breaking change

### Tags obligatoires pour releases
Chaque version doit avoir un tag Git pour HACS.

---

## ✅ Résumé

**GARDER sur GitHub (13 fichiers) :**
1. README.md
2. CHANGELOG.md
3. CONTRIBUTING.md
4. LICENSE
5. .gitignore
6. __init__.py
7. sensor.py
8. const.py
9. config_flow.py
10. strings.json
11. manifest.json
12. hacs.json
13. info.md
+ translations/ + icons/

**EXCLURE (dans .gitignore) :**
- Tous les fichiers de dev local
- Scripts shell
- Docker compose dev
- Documentation dev spécifique

**OPTIONNEL mais recommandé :**
- GitHub Actions (CI/CD)
- Screenshots
- Wiki pour documentation dev avancée

---

**Votre intégration est maintenant prête pour GitHub et HACS ! 🎉**

