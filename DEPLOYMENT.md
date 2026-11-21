# Kirana Store Production Deployment Guide

This guide covers deploying the Kirana Store Modular Monolith across staging and production environments using Docker Compose, PostgreSQL, and Redis.

---

## 1. Architecture Overview

- **Centralized Backend API**: Node.js + Express + TypeScript on port `5000`
- **Database**: PostgreSQL 16 (with Prisma ORM) on port `5432`
- **Caching & Resilience**: Redis 7 on port `6379`
- **Frontend (3 Connected Interfaces)**: Next.js 14 on port `3000`
  1. Customer E-Commerce Website (`/`)
  2. Admin Management Dashboard (`/admin`)
  3. Delivery Person Mobile PWA (`/delivery`)

---

## 2. Prerequisites

- Docker 24+ & Docker Compose v2+
- Node.js 20+ (for local development or CI/CD runners)
- Domain names with SSL certificates (e.g. `shop.apnakirana.com`)

---

## 3. Environment Variables Configuration

Create a production `.env` file in the root directory:

```env
# Database
DATABASE_URL="postgresql://kirana_user:SecurePostgresPassword123!@postgres:5432/kirana_db?schema=public"

# Redis
REDIS_URL="redis://redis:6379"

# JWT Authentication
JWT_SECRET="production-secure-32-chars-minimum-secret-key-xyz987"
JWT_EXPIRES_IN="7d"

# Razorpay Online Payments (Live or Test credentials)
RAZORPAY_KEY_ID="rzp_live_yourActualKeyId"
RAZORPAY_KEY_SECRET="yourActualKeySecret"

# Cloudinary Image Storage
CLOUDINARY_CLOUD_NAME="your_cloud_name"
CLOUDINARY_API_KEY="your_api_key"
CLOUDINARY_API_SECRET="your_api_secret"

# Frontend Public API URL
NEXT_PUBLIC_API_URL="https://api.apnakirana.com"
FRONTEND_URL="https://apnakirana.com"
```

---

## 4. Single-Command Deployment via Docker Compose

Run the following command to build and launch all 4 services:

```bash
docker compose up -d --build
```

### Apply Database Migrations & Seed Data:

```bash
docker compose exec backend npx prisma migrate deploy --schema=./src/prisma/schema.prisma
docker compose exec backend npm run seed
```

---

## 5. Reverse Proxy Configuration (Nginx)

Place Nginx in front of Docker containers for SSL termination:

```nginx
server {
    listen 80;
    server_name apnakirana.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name apnakirana.com;

    ssl_certificate /etc/letsencrypt/live/apnakirana.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/apnakirana.com/privkey.pem;

    # Frontend (Customer, Admin, Delivery PWA)
    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Centralized Backend API
    location /api/v1/ {
        proxy_pass http://127.0.0.1:5000/api/v1/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 6. Service Health Check

Verify all endpoints:
- Backend Health: `curl http://localhost:5000/health`
- Customer Store: `curl -I http://localhost:3000/`
- Admin Dashboard: `curl -I http://localhost:3000/admin`
- Delivery PWA: `curl -I http://localhost:3000/delivery`
