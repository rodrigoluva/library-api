# Deployment

Production deployment guide for the Library API project.

---

## 🚀 Deployment Options

### Option 1: Docker Compose (Recommended for Small/Medium)

```yaml
# deployment/docker-compose.yml
version: '3.8'

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://library_user:${POSTGRES_PASSWORD}@postgres:5432/library_api
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - JWT_ALGORITHM=HS256
      - JWT_EXPIRATION_MINUTES=15
    depends_on:
      postgres:
        condition: service_healthy
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 512M
          cpu: "1.0"

  postgres:
    image: postgres:16-alpine
    environment:
      - POSTGRES_DB=library_api
      - POSTGRES_USER=library_user
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U library_user -d library_api"]
      interval: 5s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - api
    restart: unless-stopped

volumes:
  postgres_data:
```

### Option 2: Kubernetes (Recommended for Scale)

```yaml
# deployment/k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: library-api
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: library-api
  template:
    metadata:
      labels:
        app: library-api
    spec:
      containers:
      - name: api
        image: your-registry/library-api:1.0.0
        ports:
        - containerPort: 8000
        envFrom:
        - secretRef:
            name: library-api-secrets
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health_check
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /health_check
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: library-api
  namespace: production
spec:
  selector:
    app: library-api
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

### Option 3: Platform as a Service (Simplest)

| Platform | Command | Notes |
|----------|---------|-------|
| **Render** | Git push triggers deploy | Free tier, Postgres included |
| **Railway** | Git push or CLI | Free tier available |
| **Fly.io** | `fly deploy` | Edge deployment |
| **Heroku** | Git push | Hobby tier available |
| **Vercel** | Git push | Serverless, free tier |
| **DigitalOcean App** | Git push or CLI | Simple PaaS |

---

## 🐳 Docker Setup

### Dockerfile

```dockerfile
# Dockerfile
FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc > /dev/null 2>&1 && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Copy project files
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && poetry install --no-dev

# Copy application code
COPY library_api/ ./library_api/
COPY migrations/ ./migrations/
COPY alembic.ini ./
COPY .env.example ./.env

# Run migrations
RUN poetry run alembic upgrade head

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health_check')" || exit 1

CMD ["poetry", "run", "uvicorn", "library_api.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Build and Run

```bash
# Build the image
docker build -t library-api:latest .

# Run the container
docker run -d \
  --name library-api \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/library_api \
  -e JWT_SECRET_KEY=your-secret-key \
  library-api:latest

# Check logs
docker logs -f library-api

# Stop
docker stop library-api
```

---

## ⚙️ Production Environment Configuration

### `.env` (Production)

```env
# Secure PostgreSQL connection (SSL required)
DATABASE_URL=postgresql+asyncpg://library_user:SECURE_PASSWORD@db-host:5432/library_api

# Strong JWT secret (≥32 chars, from secrets manager)
JWT_SECRET_KEY=production-secret-from-vault-or-secrets-manager
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=15
```

### Environment-Specific Config

| Variable | Development | Staging | Production |
|----------|------------|---------|------------|
| `DATABASE_URL` | SQLite | PostgreSQL | PostgreSQL + SSL |
| `JWT_EXPIRATION_MINUTES` | 30 | 10 | 5-15 |
| Log Level | DEBUG | INFO | WARNING |
| CORS Origins | `*` | App domain | App domain |
| Rate Limit | Disabled | 100/min | 100/min |

---

## 🗄️ Database Migration in Production

### Step-by-Step Process

```bash
# 1. Create migration
poetry run alembic revision --autogenerate -m "description"

# 2. Review generated migration
cat migrations/versions/<revision>_description.py

# 3. Test migration on staging
poetry run alembic upgrade head

# 4. Deploy application
# 5. Run migrations on production
poetry run alembic upgrade head

# Rollback if needed
# poetry run alembic downgrade -1
```

### Backup Strategy

```bash
# PostgreSQL backup (daily)
pg_dump -h db-host -U library_user library_api > backup_$(date +%Y%m%d).sql

# Restore from backup
psql -h db-host -U library_user library_api < backup_20260727.sql
```

---

## 📊 Monitoring & Observability

### Health Check Endpoint

```bash
curl http://<host>:8000/health_check
# Returns: {"status": "200 OK"}
```

### Metrics to Monitor

| Metric | Tool | Alert Threshold |
|--------|------|-----------------|
| Response time | Prometheus | >500ms (p99) |
| Error rate | Grafana | >1% of requests |
| CPU usage | Kubernetes | >80% |
| Memory usage | Kubernetes | >85% |
| DB connections | PostgreSQL metrics | >80% of max_connections |
| Active borrow records | Custom | >90% of total copies |

### Logging Strategy

```python
# library_api/app.py (logging configuration)
import logging

logging.basicConfig(
    level=logging.WARNING,  # Production: WARNING or ERROR
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
```

---

## 🔒 Production Security Checklist

- [ ] `JWT_SECRET_KEY` stored in secrets manager (not `.env`)
- [ ] `DATABASE_URL` uses SSL/TLS for PostgreSQL (`sslmode=require`)
- [ ] HTTPS enforced (nginx/ALB terminates TLS)
- [ ] `JWT_EXPIRATION_MINUTES ≤ 15 minutes`
- [ ] `DEBUG` logging disabled in production
- [ ] Rate limiting enabled
- [ ] CORS restricted to known origins
- [ ] Database user has minimal required permissions
- [ ] Automated backups configured
- [ ] Docker image uses non-root user
- [ ] Secrets not in version control
- [ ] Dependencies scanned for vulnerabilities (`poetry audit`)

---

## 🔄 CI/CD Pipeline Steps

```mermaid
graph LR
    A[Git Push] --> B[CI Pipeline]
    B --> C[Lint & Format Check]
    C --> D[Run Tests]
    D --> E[Build Docker Image]
    E --> F[Push to Registry]
    F --> G[Deploy to Staging]
    G --> H[Run Migration]
    H --> I[Run Smoke Tests]
    I --> J[Deploy to Production]
    J --> K[Run Migration]
    K --> L[Health Check]
```

---

## 🔗 Next Steps

