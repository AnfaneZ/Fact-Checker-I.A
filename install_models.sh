#!/bin/bash

echo "🚀 Installation du Fact Checker IA"

# Vérifier Ollama
if ! command -v ollama &> /dev/null
then
    echo "❌ Ollama n'est pas installé"
    echo "👉 Installe-le ici : https://ollama.com"
    exit 1
fi

echo "✅ Ollama détecté"

# Télécharger les modèles
echo "📥 Téléchargement des modèles IA..."
ollama pull llama3.1
ollama pull mistral

# Aller dans le backend
cd backend || exit

# Créer le venv si absent
if [ ! -d "venv" ]; then
    echo "📦 Création de l'environnement virtuel"
    python3 -m venv venv
fi

# Activer le venv
source venv/bin/activate

# Installer les dépendances
echo "📦 Installation des dépendances Python"
pip install --upgrade pip
pip install -r ../requirements.txt

# Lancer le backend
echo "🚀 Lancement du serveur"
uvicorn main:app --reload
