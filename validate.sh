#!/bin/bash

# Script de validation de l'intégration Synology Download Station
# Vérifie que tous les fichiers nécessaires sont présents

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}=== Validation de l'intégration Synology Download Station ===${NC}\n"

ERRORS=0
WARNINGS=0

# Fonction pour vérifier l'existence d'un fichier
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1"
        return 0
    else
        echo -e "${RED}✗${NC} $1 ${RED}(MANQUANT)${NC}"
        ((ERRORS++))
        return 1
    fi
}

# Fonction pour vérifier l'existence d'un dossier
check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $1/"
        return 0
    else
        echo -e "${RED}✗${NC} $1/ ${RED}(MANQUANT)${NC}"
        ((ERRORS++))
        return 1
    fi
}

echo "📁 Vérification de la structure des fichiers..."
echo ""

# Fichiers Python essentiels
echo "Fichiers Python :"
check_file "__init__.py"
check_file "config_flow.py"
check_file "const.py"
check_file "sensor.py"
echo ""

# Fichiers de configuration
echo "Fichiers de configuration :"
check_file "manifest.json"
check_file "strings.json"
echo ""

# Documentation
echo "Documentation :"
check_file "README.md"
check_file "INSTALLATION_FR.md"
check_file "QUICKSTART.md"
check_file "CHANGELOG.md"
check_file "LICENSE"
check_file "info.md"
echo ""

# Traductions
echo "Traductions :"
check_dir "translations"
check_file "translations/en.json"
check_file "translations/fr.json"
echo ""

# Fichiers optionnels
echo "Fichiers optionnels :"
check_file "hacs.json"
check_file "install.sh"
check_file ".gitignore"
echo ""

# Vérification du contenu de manifest.json
echo "Vérification du manifest.json :"
if [ -f "manifest.json" ]; then
    if grep -q '"domain": "synology_download_station"' manifest.json; then
        echo -e "${GREEN}✓${NC} Domain correct"
    else
        echo -e "${RED}✗${NC} Domain incorrect"
        ((ERRORS++))
    fi
    
    if grep -q '"version"' manifest.json; then
        echo -e "${GREEN}✓${NC} Version présente"
    else
        echo -e "${YELLOW}⚠${NC} Version manquante"
        ((WARNINGS++))
    fi
    
    if grep -q '"iot_class"' manifest.json; then
        echo -e "${GREEN}✓${NC} IoT class présente"
    else
        echo -e "${YELLOW}⚠${NC} IoT class manquante"
        ((WARNINGS++))
    fi
fi
echo ""

# Vérification des imports Python
echo "Vérification des imports Python :"
if grep -q "from homeassistant.config_entries import ConfigEntry" __init__.py; then
    echo -e "${GREEN}✓${NC} Imports corrects dans __init__.py"
else
    echo -e "${RED}✗${NC} Imports manquants dans __init__.py"
    ((ERRORS++))
fi

if grep -q "class ConfigFlow" config_flow.py; then
    echo -e "${GREEN}✓${NC} ConfigFlow présent"
else
    echo -e "${RED}✗${NC} ConfigFlow manquant"
    ((ERRORS++))
fi

if grep -q "class.*Sensor" sensor.py; then
    echo -e "${GREEN}✓${NC} Sensor class présente"
else
    echo -e "${RED}✗${NC} Sensor class manquante"
    ((ERRORS++))
fi
echo ""

# Résumé
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✓ Validation réussie !${NC}"
    echo -e "L'intégration est prête à être installée dans Home Assistant."
    if [ $WARNINGS -gt 0 ]; then
        echo -e "${YELLOW}⚠ $WARNINGS avertissement(s)${NC}"
    fi
    exit 0
else
    echo -e "${RED}✗ Validation échouée avec $ERRORS erreur(s)${NC}"
    if [ $WARNINGS -gt 0 ]; then
        echo -e "${YELLOW}⚠ $WARNINGS avertissement(s)${NC}"
    fi
    exit 1
fi
