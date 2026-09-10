#!/bin/bash
# Quick setup script for Railway deployment

echo "🚀 Animal Rescue - Railway Deployment Setup"
echo "=============================================="

# Install Railway CLI if not present
if ! command -v railway &> /dev/null; then
    echo "Installing Railway CLI..."
    curl -fsSL https://railway.app/install.sh | sh
fi

# Generate SECRET_KEY
echo ""
echo "Generating Django SECRET_KEY..."
SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
echo "Generated SECRET_KEY: $SECRET_KEY"

# Create .env file
echo ""
echo "Creating .env file..."
cp .env.example .env

# Update SECRET_KEY in .env
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s/your-secret-key-here-change-in-production/$SECRET_KEY/" .env
else
    sed -i "s/your-secret-key-here-change-in-production/$SECRET_KEY/" .env
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update .env with your ALLOWED_HOSTS domain"
echo "2. Commit and push to GitHub:"
echo "   git add ."
echo "   git commit -m 'Add Railway deployment configuration'"
echo "   git push"
echo "3. Go to Railway dashboard: https://railway.app/dashboard"
echo "4. Create new project from your GitHub repository"
echo "5. Add PostgreSQL plugin and configure environment variables"
echo "6. Watch the deployment logs!"
echo ""
echo "📖 See RAILWAY_DEPLOYMENT.md for detailed instructions"
