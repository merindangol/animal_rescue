# Railway Deployment Checklist

## 📋 Pre-Deployment Setup

- [x] Created `requirements.txt` with all dependencies
- [x] Created `Procfile` for Railway build/release process
- [x] Created `runtime.txt` specifying Python 3.11.9
- [x] Created `.gitignore` to exclude sensitive files
- [x] Updated `settings.py` for production:
  - [x] Added environment variable support
  - [x] Configured DEBUG mode
  - [x] Set up ALLOWED_HOSTS
  - [x] Added WhiteNoise middleware for static files
  - [x] Configured PostgreSQL database support
  - [x] Added production security settings

## 🚀 Quick Start Guide

### Step 1: Prepare Your Local Environment
```bash
# Copy environment example
cp .env.example .env

# Edit .env with your values (Windows: setup_railway.bat)
# On Unix/Mac: ./setup_railway.sh
setup_railway.bat
```

### Step 2: Commit and Push to GitHub
```bash
git add .
git commit -m "Add Railway deployment configuration"
git push
```

### Step 3: Deploy on Railway
1. Visit https://railway.app/dashboard
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your `animal_rescue` repository
5. Authorize and let Railway build your project

### Step 4: Configure Environment Variables (In Railway Dashboard)
Under Variables, set:
- `DEBUG=False`
- `SECRET_KEY=your-generated-secret-key`
- `ALLOWED_HOSTS=yourdomain.railway.app`

### Step 5: Add PostgreSQL Plugin
1. Click "Add Plugin"
2. Select "PostgreSQL"
3. Railway will auto-populate database credentials

### Step 6: Monitor Deployment
1. Watch the build logs
2. Migrations should run automatically
3. Your app will be live at `yourproject.railway.app`

## 📁 Files Created/Modified

| File | Purpose |
|------|---------|
| `requirements.txt` | Python dependencies |
| `Procfile` | Railway build & release commands |
| `runtime.txt` | Python version specification |
| `.gitignore` | Exclude sensitive files from git |
| `.env.example` | Template for environment variables |
| `RAILWAY_DEPLOYMENT.md` | Detailed deployment guide |
| `setup_railway.sh` | Unix/Mac setup script |
| `setup_railway.bat` | Windows setup script |
| `animal_rescue/settings.py` | Updated for production |

## 🔧 Configuration Details

### Database
- **Development**: SQLite (db.sqlite3)
- **Production**: PostgreSQL (via Railway plugin)
- Automatically switched via `USE_POSTGRES` environment variable

### Static Files
- Served by WhiteNoise (no separate server needed)
- Compressed and minified automatically
- Location: `staticfiles/` directory

### Media Files
- Stored in `media/` directory
- ⚠️ Note: Railway filesystem is ephemeral
- Recommendation: Use S3, Google Cloud Storage, or similar for persistent storage

## ⚠️ Important Notes

1. **SECRET_KEY**: Change the default immediately
   - Generate a new one: `python manage.py shell`
   - Then: `from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())`

2. **ALLOWED_HOSTS**: Update with your actual domain
   - Format: `yourdomain.com,www.yourdomain.com`
   - Include Railway subdomain initially

3. **DEBUG Mode**: Always set to `False` in production
   - Never set to `True` on public servers
   - Exposes sensitive information

4. **Database**: PostgreSQL is recommended for production
   - SQLite won't work well with ephemeral filesystem
   - Railway's PostgreSQL plugin handles backups automatically

5. **Media Storage**: Consider external storage
   - Railway containers reset on redeployment
   - Use AWS S3, Google Cloud Storage, or similar

## 🐛 Troubleshooting

### Build Fails
```bash
# Check requirements.txt syntax
pip install -r requirements.txt

# Verify Procfile syntax
cat Procfile
```

### Application Crashes
```bash
# View Railway logs
railway logs

# Run migrations manually
railway run python manage.py migrate
```

### Static Files Missing
```bash
# Collect static files
python manage.py collectstatic --noinput
```

### Database Connection Error
- Verify PostgreSQL plugin is active
- Check environment variables match plugin credentials
- Run migrations: `railway run python manage.py migrate`

## 📞 Support Resources

- Railway Docs: https://docs.railway.app
- Django Deployment: https://docs.djangoproject.com/en/6.1/howto/deployment/
- WhiteNoise Docs: http://whitenoise.evans.io/
- PostgreSQL: https://www.postgresql.org/docs/

## ✅ Post-Deployment

After successful deployment:

1. **Create Superuser**
   ```bash
   railway run python manage.py createsuperuser
   ```

2. **Access Admin Panel**
   - Visit: `https://yourdomain.railway.app/admin`

3. **Set Up Custom Domain**
   - Railway dashboard → Domains → Add Domain
   - Follow DNS configuration instructions

4. **Monitor Logs**
   - Railway dashboard → Logs
   - Set up error alerts (Sentry recommended)

5. **Regular Maintenance**
   - Monitor database size
   - Regular backups (Railway handles this)
   - Update dependencies periodically
