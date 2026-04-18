# Deployment Guide

## Production Deployment Checklist

### Pre-Deployment
- [ ] All tests passing
- [ ] Code reviewed
- [ ] Documentation updated
- [ ] Environment variables configured
- [ ] Database backup created
- [ ] SSL certificate obtained
- [ ] Domain name configured
- [ ] Monitoring setup

## Environment Setup

### Production Environment Variables

#### Backend (.env)
```env
# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Security
SECRET_KEY=<generate-strong-random-key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Environment
ENVIRONMENT=production
DEBUG=False
```

#### Frontend (.env.production)
```env
REACT_APP_API_URL=https://api.yourdomain.com
REACT_APP_ENVIRONMENT=production
```

## Deployment Options

### Option 1: AWS Deployment

#### Backend (AWS Elastic Beanstalk)

1. **Install AWS CLI and EB CLI**
```bash
pip install awscli awsebcli
aws configure
```

2. **Initialize Elastic Beanstalk**
```bash
cd backend
eb init -p python-3.11 exam-registration-api
```

3. **Create environment**
```bash
eb create exam-registration-prod
```

4. **Deploy**
```bash
eb deploy
```

5. **Set environment variables**
```bash
eb setenv DATABASE_URL=postgresql://... SECRET_KEY=...
```

#### Frontend (AWS S3 + CloudFront)

1. **Build production bundle**
```bash
cd frontend
npm run build
```

2. **Create S3 bucket**
```bash
aws s3 mb s3://exam-registration-frontend
```

3. **Upload files**
```bash
aws s3 sync build/ s3://exam-registration-frontend --acl public-read
```

4. **Configure CloudFront**
- Create CloudFront distribution
- Point to S3 bucket
- Configure SSL certificate
- Set custom domain

#### Database (AWS RDS)

1. **Create RDS PostgreSQL instance**
```bash
aws rds create-db-instance \
  --db-instance-identifier exam-registration-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username admin \
  --master-user-password <password> \
  --allocated-storage 20
```

2. **Configure security groups**
- Allow inbound on port 5432 from backend
- Restrict access to specific IPs

3. **Run migrations**
```bash
psql -h <rds-endpoint> -U admin -d postgres -f database/schema.sql
```

### Option 2: Heroku Deployment

#### Backend

1. **Install Heroku CLI**
```bash
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

2. **Create Heroku app**
```bash
cd backend
heroku create exam-registration-api
```

3. **Add PostgreSQL**
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

4. **Create Procfile**
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

5. **Deploy**
```bash
git init
git add .
git commit -m "Initial commit"
git push heroku main
```

6. **Set environment variables**
```bash
heroku config:set SECRET_KEY=your-secret-key
```

7. **Run database migrations**
```bash
heroku pg:psql < database/schema.sql
```

#### Frontend

1. **Create Heroku app**
```bash
cd frontend
heroku create exam-registration-frontend
```

2. **Add buildpack**
```bash
heroku buildpacks:set mars/create-react-app
```

3. **Deploy**
```bash
git init
git add .
git commit -m "Initial commit"
git push heroku main
```

### Option 3: DigitalOcean Deployment

#### Backend (App Platform)

1. **Create app.yaml**
```yaml
name: exam-registration-api
services:
- name: api
  github:
    repo: your-username/exam-registration
    branch: main
    deploy_on_push: true
  source_dir: /backend
  run_command: uvicorn app.main:app --host 0.0.0.0 --port 8080
  environment_slug: python
  envs:
  - key: DATABASE_URL
    value: ${db.DATABASE_URL}
  - key: SECRET_KEY
    value: ${SECRET_KEY}
databases:
- name: db
  engine: PG
  version: "14"
```

2. **Deploy via CLI or UI**
```bash
doctl apps create --spec app.yaml
```

#### Frontend (Static Site)

1. **Build**
```bash
npm run build
```

2. **Deploy to DigitalOcean Spaces**
```bash
# Install s3cmd
pip install s3cmd

# Configure
s3cmd --configure

# Upload
s3cmd sync build/ s3://your-space/
```

### Option 4: Docker Deployment

#### Backend Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Frontend Dockerfile
```dockerfile
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

#### docker-compose.yml
```yaml
version: '3.8'

services:
  db:
    image: postgres:14
    environment:
      POSTGRES_DB: exam_registration
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./database/schema.sql:/docker-entrypoint-initdb.d/schema.sql
    ports:
      - "5432:5432"

  backend:
    build: ./backend
    environment:
      DATABASE_URL: postgresql://postgres:password@db:5432/exam_registration
      SECRET_KEY: your-secret-key
    ports:
      - "8000:8000"
    depends_on:
      - db

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  postgres_data:
```

#### Deploy with Docker Compose
```bash
docker-compose up -d
```

## SSL/TLS Configuration

### Using Let's Encrypt (Certbot)

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo certbot renew --dry-run
```

### Nginx Configuration
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # Frontend
    location / {
        root /var/www/frontend/build;
        try_files $uri /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Database Migration

### Backup Production Database
```bash
# PostgreSQL
pg_dump -h hostname -U username -d dbname > backup.sql

# Restore
psql -h hostname -U username -d dbname < backup.sql
```

### Automated Backups
```bash
# Cron job for daily backups
0 2 * * * pg_dump -h hostname -U username dbname | gzip > /backups/db_$(date +\%Y\%m\%d).sql.gz
```

## Monitoring & Logging

### Application Monitoring

#### Sentry (Error Tracking)
```python
# Backend
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FastApiIntegration()],
    traces_sample_rate=1.0,
)
```

```javascript
// Frontend
import * as Sentry from "@sentry/react";

Sentry.init({
  dsn: "your-sentry-dsn",
  integrations: [new Sentry.BrowserTracing()],
  tracesSampleRate: 1.0,
});
```

#### Logging
```python
# Backend logging
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### Performance Monitoring

#### New Relic
```bash
# Install
pip install newrelic

# Configure
newrelic-admin generate-config YOUR_LICENSE_KEY newrelic.ini

# Run
NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program uvicorn app.main:app
```

## Security Hardening

### Backend Security Headers
```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

app.add_middleware(HTTPSRedirectMiddleware)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["yourdomain.com"])

@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response
```

### Rate Limiting
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.get("/api/endpoint")
@limiter.limit("5/minute")
async def endpoint():
    return {"message": "Limited endpoint"}
```

## CI/CD Pipeline

### GitHub Actions

#### .github/workflows/deploy.yml
```yaml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Run tests
      run: |
        cd backend
        pip install -r requirements.txt
        pytest

  deploy-backend:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Deploy to Heroku
      uses: akhileshns/heroku-deploy@v3.12.12
      with:
        heroku_api_key: ${{secrets.HEROKU_API_KEY}}
        heroku_app_name: "exam-registration-api"
        heroku_email: "your-email@example.com"

  deploy-frontend:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Build and Deploy
      run: |
        cd frontend
        npm install
        npm run build
        # Deploy to S3 or other hosting
```

## Post-Deployment

### Health Checks
```python
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "database": check_database_connection(),
        "timestamp": datetime.utcnow()
    }
```

### Smoke Tests
```bash
# Test API
curl https://api.yourdomain.com/health

# Test frontend
curl https://yourdomain.com

# Test authentication
curl -X POST https://api.yourdomain.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test"}'
```

## Rollback Plan

### Quick Rollback
```bash
# Heroku
heroku rollback

# AWS Elastic Beanstalk
eb deploy --version previous-version

# Docker
docker-compose down
docker-compose up -d --build
```

## Maintenance Mode

### Nginx Maintenance Page
```nginx
if (-f /var/www/maintenance.html) {
    return 503;
}

error_page 503 @maintenance;
location @maintenance {
    rewrite ^(.*)$ /maintenance.html break;
}
```

## Cost Optimization

### Free Tier Options
- **Heroku**: Free dyno (sleeps after 30 min)
- **AWS**: Free tier (12 months)
- **DigitalOcean**: $5/month droplet
- **Vercel**: Free for frontend
- **Netlify**: Free for frontend
- **Railway**: Free tier available

### Estimated Monthly Costs

#### Small Scale (< 1000 users)
- Backend: $5-10 (DigitalOcean/Heroku)
- Database: $7-15 (Managed PostgreSQL)
- Frontend: $0-5 (Static hosting)
- **Total**: $12-30/month

#### Medium Scale (1000-10000 users)
- Backend: $25-50 (Multiple instances)
- Database: $15-50 (Larger instance)
- Frontend: $5-20 (CDN)
- Monitoring: $10-30
- **Total**: $55-150/month

## Support & Maintenance

### Regular Tasks
- [ ] Monitor error logs daily
- [ ] Check performance metrics weekly
- [ ] Update dependencies monthly
- [ ] Database backup verification weekly
- [ ] Security patches as needed
- [ ] SSL certificate renewal (automated)

### Emergency Contacts
- Database admin
- DevOps team
- Security team
- On-call developer

---

**Remember**: Always test in staging before deploying to production!
