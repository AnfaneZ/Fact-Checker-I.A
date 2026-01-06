Write-Host "🚀 Installation du Fact Checker IA"

# Vérifier Ollama
if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Ollama n'est pas installé"
    Write-Host "👉 Installe-le ici : https://ollama.com"
    exit 1
}

Write-Host "✅ Ollama détecté"

# Télécharger les modèles
Write-Host "📥 Téléchargement des modèles IA..."
ollama pull llama3.1
ollama pull mistral

# Aller dans le backend
Set-Location backend

# Créer le venv si absent
if (-not (Test-Path "venv")) {
    Write-Host "📦 Création de l'environnement virtuel"
    python -m venv venv
}

# Activer le venv
Write-Host "⚙️ Activation de l'environnement virtuel"
.\venv\Scripts\Activate.ps1

# Installer les dépendances
Write-Host "📦 Installation des dépendances Python"
pip install --upgrade pip
pip install -r ../requirements.txt

# Lancer le backend
Write-Host "🚀 Lancement du serveur"
uvicorn main:app --reload
