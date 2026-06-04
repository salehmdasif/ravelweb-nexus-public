# Deployment Overview: Ravelweb Nexus

## Deployment Architecture

```
Internet
   |
   └── Nginx (reverse proxy + SSL termination)
          |
          └── Gunicorn (WSGI server, multiple workers)
                 |
                 └── Flask Application
                        |
                        ├── PostgreSQL (main DB + all tenant DBs)
                        └── Redis (rate limiting + session revocation)
```

Everything runs on a single Ubuntu VPS using Docker Compose. Each service runs in its
own container. Nginx handles SSL termination via Let's Encrypt certificates.

---

## Environment Summary

| Environment | Stack | Purpose |
|-------------|-------|---------|
| Development | Python + local PostgreSQL + local Redis | Local development |
| Production | Docker Compose on Ubuntu VPS + Nginx + Gunicorn | Live platform |

---

## Docker Compose Services

```yaml
# Structure only -- values are placeholders

services:
  app:
    build: .
    restart: always
    env_file: .env.production
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    restart: always
    volumes:
      - pgdata:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    restart: always

  nginx:
    image: nginx:alpine
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - /etc/letsencrypt:/etc/letsencrypt

volumes:
  pgdata:
```

---

## Dockerfile Overview

```dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "run:app"]
```

---

## Nginx Configuration (Summary)

```nginx
server {
    listen 80;
    server_name YOUR_DOMAIN;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name YOUR_DOMAIN;

    ssl_certificate     /etc/letsencrypt/live/YOUR_DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/YOUR_DOMAIN/privkey.pem;

    location / {
        proxy_pass http://app:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /app/static/;
        expires 7d;
    }
}
```

---

## Environment Variables

All configuration is injected via environment variables. No secrets are in the image.

```env
# Application
SECRET_KEY=YOUR_VALUE_HERE
FLASK_ENV=production
FLASK_DEBUG=0

# Databases
MAIN_DATABASE_URL=YOUR_VALUE_HERE

# Redis
REDIS_URL=YOUR_VALUE_HERE
RATELIMIT_STORAGE_URI=YOUR_VALUE_HERE

# License
LICENSE_JWT_SECRET=YOUR_VALUE_HERE

# JWT (Mobile API)
JWT_SECRET_KEY=YOUR_VALUE_HERE
JWT_ACCESS_TOKEN_EXPIRES=1800
JWT_REFRESH_TOKEN_EXPIRES=604800

# Google OAuth
GOOGLE_CLIENT_ID=YOUR_VALUE_HERE
GOOGLE_CLIENT_SECRET=YOUR_VALUE_HERE

# SMTP
MAIL_SERVER=YOUR_VALUE_HERE
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=YOUR_VALUE_HERE
MAIL_PASSWORD=YOUR_VALUE_HERE
MAIL_DEFAULT_SENDER=YOUR_VALUE_HERE
```

---

## Production Safety Checks

The application validates the environment at startup and refuses to start if:

- `SECRET_KEY` is not set.
- `LICENSE_JWT_SECRET` is not set.
- In production mode: `JWT_SECRET_KEY` is not set.
- In production mode: `FLASK_DEBUG` is not `0`.
- In production mode: default placeholder secrets are detected.

This prevents accidental production deployments with insecure defaults.

---

## Database Initialization

On a fresh server, the main database schema is initialized by running:

```bash
python init_main_db.py
python create_superadmin.py
```

Tenant databases are provisioned automatically through the application when users
activate license keys. No manual steps are needed per tenant.

---

## Migration Strategy

Schema changes are applied using numbered SQL migration files:

```
migrations/
├── main_db/
│   ├── 001_main_db_changes.sql
│   ├── 002_saas_tables.sql
│   └── ...
└── tenant_db/
    └── 001_tenant_schema.sql
```

The consolidated `tenant_db/001_tenant_schema.sql` is the single source of truth for
all new tenant databases. It is applied automatically during provisioning.

Incremental migration files in `migrations/` (numbered 001 to 029+) are applied manually
to existing tenant databases using a migration runner script (`apply.py`).

---

## Backup Strategy

**PostgreSQL:** The entire PostgreSQL data volume is backed up via VPS snapshot. For
more granular recovery, `pg_dump` can target individual tenant databases by name.
The list of tenant database names is available from the `tenant_databases` table in
the main database.

**Redis:** Redis stores only ephemeral data (rate limit counters, revocation signals).
Redis backup is not required for data integrity.

---

## Monitoring and Logging

Application logs are written in two formats simultaneously:

- `logs/app.log`: Human-readable text log for terminal inspection.
- `logs/app.json.log`: Structured JSON log for log aggregation tools.

Log level is configurable via environment. In production, the default is `INFO`.

500 errors trigger a non-blocking email alert via SMTP if `MAIL_USERNAME` is configured.

---

## SSL Certificate Renewal

Let's Encrypt certificates auto-renew via a cron job on the host:

```
0 12 * * * certbot renew --quiet && docker exec nginx nginx -s reload
```

---

## Scaling Considerations

The current single-server deployment handles dozens of concurrent tenants. To scale
horizontally:

1. Move PostgreSQL and Redis to managed cloud services (RDS, ElastiCache).
2. Deploy multiple application containers behind a load balancer.
3. The application is stateless between requests (session data is in cookies, not
   server memory), so no sticky sessions are required.
