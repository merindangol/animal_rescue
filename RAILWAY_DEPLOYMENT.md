# Railway Deployment Guide for Animal Rescue Django Project

## Prerequisites
- GitHub account with your project repository
- Railway account (sign up at https://railway.app)
- Project pushed to GitHub

## Step 1: Connect Your GitHub Repository
1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Authorize Railway to access your GitHub account
5. Select your `animal_rescue` repository

## Step 2: Configure Environment Variables
1. In your Railway project, go to "Variables"
2. Add the following environment variables:

   **Required:**
   - `SECRET_KEY`: Generate a secure key (use Django's default or create a new one)
   - `DEBUG`: Set to `False`
   - `ALLOWED_HOSTS`: Your domain (e.g., `yourdomain.railway.app`)

   **Database (Railway PostgreSQL Plugin):**
   - Railway will automatically provide `DATABASE_URL` when you add the PostgreSQL plugin

3. Click "Add Plugin" and select "PostgreSQL"
4. This will automatically populate database credentials

## Step 3: Database Setup
1. Add PostgreSQL plugin (see Step 2)
2. Railway will automatically handle the `DATABASE_URL` environment variable
3. Update your `.env` or environment variables:
   ```
   USE_POSTGRES=True
   ```

## Step 4: Deployment Configuration
The following files are already configured for Railway:
- **Procfile**: Defines the web server (Gunicorn) and release commands
- **runtime.txt**: Specifies Python 3.11.9
- **requirements.txt**: Lists all dependencies

## Step 5: Database Migrations
1. Go to the "Deployments" tab
2. Check the build logs - migrations should run automatically via the Procfile release command
3. If migrations fail, you can run them manually via the Railway CLI:
   ```bash
   railway run python manage.py migrate
   ```

## Step 6: Create Superuser (Admin)
Run this command to create an admin user:
```bash
railway run python manage.py createsuperuser
```

## Step 7: Static Files
- WhiteNoise is configured to serve static files
- Run `python manage.py collectstatic` during build (included in Procfile)
- No additional static file server needed

## Step 8: Custom Domain (Optional)
1. In Railway project settings, go to "Domains"
2. Add your custom domain
3. Follow the DNS configuration instructions

## Troubleshooting

### Build Fails
- Check build logs in Railway dashboard
- Ensure all dependencies are in `requirements.txt`
- Verify `Procfile` syntax

### Database Connection Issues
- Check that PostgreSQL plugin is active
- Verify `USE_POSTGRES=True` in environment variables
- Check database credentials in Railway PostgreSQL settings

### Static Files Not Loading
- Run: `railway run python manage.py collectstatic --noinput`
- Verify `STATIC_ROOT` and `STATIC_URL` in settings.py

### Media Files
- Railway's filesystem is ephemeral (resets on redeploy)
- For persistent media storage, consider using:
  - AWS S3
  - Google Cloud Storage
  - Digital Ocean Spaces
  - Railway's new persistent volumes (beta)

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `DEBUG` | Django debug mode | `False` |
| `SECRET_KEY` | Django secret key | `your-secret-key` |
| `ALLOWED_HOSTS` | Comma-separated allowed domains | `yourdomain.railway.app` |
| `USE_POSTGRES` | Enable PostgreSQL | `True` |
| `DATABASE_URL` | Auto-set by Railway PostgreSQL | (auto) |

## Useful Railway CLI Commands

```bash
# View logs
railway logs

# Run management commands
railway run python manage.py <command>

# SSH into container
railway shell

# Open Railway dashboard
railway open
```

## Next Steps
1. Test your deployment at your Railway URL
2. Set up a custom domain
3. Configure media storage (if needed)
4. Set up error tracking (Sentry recommended)
5. Monitor logs in Railway dashboard
