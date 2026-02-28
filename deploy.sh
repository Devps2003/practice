#!/bin/bash
# Quick deploy script for Founding Engineer HQ

echo "🚀 Deploying Founding Engineer HQ to Streamlit Cloud"
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit: Founding Engineer HQ"
    echo ""
    echo "✅ Git initialized. Next steps:"
    echo ""
    echo "1. Create a PRIVATE GitHub repo: https://github.com/new"
    echo "2. Copy the repo URL (e.g., https://github.com/yourusername/founding-engineer-hq.git)"
    echo "3. Run these commands:"
    echo ""
    echo "   git remote add origin YOUR_REPO_URL_HERE"
    echo "   git branch -M main"
    echo "   git push -u origin main"
    echo ""
    echo "4. Then go to https://share.streamlit.io and deploy!"
    echo ""
    echo "📖 Full guide: See DEPLOY.md"
else
    echo "✅ Git repo exists. Pushing to GitHub..."
    echo ""
    echo "Run these commands:"
    echo "  git add ."
    echo "  git commit -m 'Update app'"
    echo "  git push origin main"
    echo ""
    echo "Streamlit Cloud will auto-deploy on push."
fi
