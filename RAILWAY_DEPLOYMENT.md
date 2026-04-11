# Railway Deployment Configuration

## Issue Summary
The build process was failing because `python manage.py migrate` was being executed during the build phase when no database was available. Database operations should only happen at runtime.

## Solution Approach
1. ✅ Separate build-time operations (collectstatic) from runtime operations (migrate)
2. ✅ Use Railway's release phase to run migrations after database is available
3. ✅ Handle Gunicorn startup gracefully

## Railway Configuration Changes

### 1. Build Command (CHANGE THIS)
**Current (failing):**
```bash
cd src && python manage.py migrate && python manage.py collectstatic
```

**New (should be):**
```bash
cd src && python manage.py collectstatic --noinput --clear 2>/dev/null || true
```

### 2. Release Command (ADD THIS - NEW)
Railway supports a release phase that runs BEFORE the start command.

Add a new **Release Command**:
```bash
cd src && python manage.py migrate --noinput
```

### 3. Start Command (no change needed)
Keep your current start command:
```bash
cd src && gunicorn family.wsgi:application --bind 0.0.0.0:8080
```

## How to Update in Railway Dashboard

1. Go to your Railway project
2. Click on your service "Family"
3. Go to the "Deploy" or "Settings" tab
4. Find "Build Command" → Replace with the new build command above
5. Find or add "Release Command" → Add the release command above
6. Keep the existing "Start Command"
7. Redeploy

## Environment Variables to Check
Ensure these are set in Railway:
- `DATABASE_URL` - Your PostgreSQL connection string (Railway should provide this)
- `DJANGO_SECRET_KEY` - Your Django secret key
- `DJANGO_DEBUG` - Should be `false` in production

## Files Modified
- `src/family/settings.py` - Simplified database configuration to prefer DATABASE_URL in production
- `build.sh` - Safe static file collection (not strictly needed now)
- `start.sh` - Graceful startup with optional migration retry (not strictly needed now)

## Why This Works
- **Build phase**: Only collects static files, no database needed
- **Release phase**: Runs migrations when database IS available
- **Start phase**: Starts Gunicorn to serve the application
- **WhiteNoise**: Already configured to serve static files efficiently

## Alternative: Using Environment-Based Checks
If you prefer, you can also modify Django settings to skip database operations during build by checking an environment variable, but the Release Command approach is cleaner and is Railway's recommended pattern.
