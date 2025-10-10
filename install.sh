#!/bin/bash

# Script d'installation pour Synology Download Station Integration
# Usage: ./install.sh [chemin_vers_config_home_assistant]

# Couleurs pour l'affichage
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Installation de Synology Download Station Integration ===${NC}"

# Déterminer le chemin de configuration Home Assistant
if [ -n "$1" ]; then
    CONFIG_PATH="$1"
else
    # Chemins par défaut selon le système
    if [ -d "/config" ]; then
        CONFIG_PATH="/config"
    elif [ -d "$HOME/.homeassistant" ]; then
        CONFIG_PATH="$HOME/.homeassistant"
    else
        echo -e "${RED}Erreur: Impossible de trouver le répertoire de configuration Home Assistant${NC}"
        echo "Usage: $0 [chemin_vers_config_home_assistant]"
        exit 1
    fi
fi

echo -e "${YELLOW}Répertoire de configuration: ${CONFIG_PATH}${NC}"

# Vérifier que le répertoire existe
if [ ! -d "$CONFIG_PATH" ]; then
    echo -e "${RED}Erreur: Le répertoire ${CONFIG_PATH} n'existe pas${NC}"
    exit 1
fi

# Créer le répertoire custom_components s'il n'existe pas
CUSTOM_COMPONENTS_PATH="${CONFIG_PATH}/custom_components"
if [ ! -d "$CUSTOM_COMPONENTS_PATH" ]; then
    echo -e "${YELLOW}Création du répertoire custom_components...${NC}"
    mkdir -p "$CUSTOM_COMPONENTS_PATH"
fi

# Créer le répertoire de l'intégration
INTEGRATION_PATH="${CUSTOM_COMPONENTS_PATH}/synology_download_station"
if [ -d "$INTEGRATION_PATH" ]; then
    echo -e "${YELLOW}L'intégration existe déjà. Mise à jour...${NC}"
    rm -rf "$INTEGRATION_PATH"
fi

mkdir -p "$INTEGRATION_PATH"

# Copier les fichiers
echo -e "${YELLOW}Copie des fichiers...${NC}"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cp "$SCRIPT_DIR/__init__.py" "$INTEGRATION_PATH/"
cp "$SCRIPT_DIR/manifest.json" "$INTEGRATION_PATH/"
cp "$SCRIPT_DIR/const.py" "$INTEGRATION_PATH/"
cp "$SCRIPT_DIR/sensor.py" "$INTEGRATION_PATH/"
cp "$SCRIPT_DIR/config_flow.py" "$INTEGRATION_PATH/"
cp "$SCRIPT_DIR/strings.json" "$INTEGRATION_PATH/"

# Copier les traductions
mkdir -p "$INTEGRATION_PATH/translations"
cp "$SCRIPT_DIR/translations/"*.json "$INTEGRATION_PATH/translations/"

# Copier les icônes
mkdir -p "$INTEGRATION_PATH/icons"
cp "$SCRIPT_DIR/icons/"* "$INTEGRATION_PATH/icons/"

echo -e "${GREEN}✓ Installation terminée avec succès !${NC}"
echo ""
echo -e "${YELLOW}Prochaines étapes :${NC}"
echo "1. Redémarrez Home Assistant"
echo "2. Allez dans Paramètres → Appareils et services"
echo "3. Cliquez sur '+ Ajouter une intégration'"
echo "4. Recherchez 'Synology Download Station'"
echo "5. Suivez les instructions de configuration"
echo ""
echo -e "${GREEN}Bonne utilisation !${NC}"
