---
title: "Docker Compose para desarrollo: Mi setup definitivo"
date: 2024-03-05T16:45:00+01:00
draft: false
tags: ["docker", "devops", "desarrollo", "postgresql", "redis"]
slug: docker-compose-desarrollo
description: "Un docker-compose.yml completo para desarrollo local con PostgreSQL, Redis, Nginx y más, listo para copiar y pegar."
---

## Por qué Docker Compose

Después de años configurando entornos de desarrollo, Docker Compose se ha convertido en mi herramienta imprescindible. Te permite:

- ✅ Entorno consistente entre desarrolladores
- ✅ Setup de proyecto en minutos (no horas)
- ✅ Múltiples versiones de bases de datos sin conflictos
- ✅ Fácil de destruir y recrear

## Mi setup base

Este es mi `docker-compose.yml` para un proyecto web típico:

```yaml
version: '3.8'

services:
  # Base de datos principal
  db:
    image: postgres:15-alpine
    container_name: proyecto_db
    environment:
      POSTGRES_DB: miapp_dev
      POSTGRES_USER: developer
      POSTGRES_PASSWORD: dev_password_123
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./scripts/init-db.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U developer"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Cache con Redis
  redis:
    image: redis:7-alpine
    container_name: proyecto_redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes

  # Aplicación web (ejemplo con Python/Django)
  web:
    build: .
    container_name: proyecto_web
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
    ports:
      - "8000:8000"
    environment:
      - DEBUG=True
      - DATABASE_URL=postgresql://developer:dev_password_123@db:5432/miapp_dev
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started

  # Worker para tareas asíncronas (Celery)
  worker:
    build: .
    container_name: proyecto_worker
    command: celery -A config worker -l info
    volumes:
      - .:/app
    environment:
      - DATABASE_URL=postgresql://developer:dev_password_123@db:5432/miapp_dev
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis

  # Nginx para servir estáticos en desarrollo
  nginx:
    image: nginx:alpine
    container_name: proyecto_nginx
    ports:
      - "80:80"
    volumes:
      - ./nginx/dev.conf:/etc/nginx/nginx.conf:ro
      - static_volume:/usr/share/nginx/html/static:ro
    depends_on:
      - web

  # Mailhog para emails en desarrollo
  mailhog:
    image: mailhog/mailhog:latest
    container_name: proyecto_mailhog
    ports:
      - "1025:1025"  # SMTP
      - "8025:8025"  # Web UI

volumes:
  postgres_data:
  redis_data:
  static_volume:
```

## Dockerfile optimizado

El `Dockerfile` correspondiente:

```dockerfile
FROM python:3.11-slim

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements y instalar dependencias
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copiar código
COPY . .

# Exponer puerto
EXPOSE 8000

# Usuario no-root
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser
```

## Comandos útiles

Creo un `Makefile` para simplificar:

```makefile
.PHONY: up down restart logs shell db-shell test clean

up:
	docker-compose up -d

down:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f

shell:
	docker-compose exec web bash

db-shell:
	docker-compose exec db psql -U developer -d miapp_dev

test:
	docker-compose exec web pytest

clean:
	docker-compose down -v
	docker system prune -f
```

Ahora solo hago:

```bash
make up      # Levantar todo
make logs    # Ver logs
make shell   # Entrar al contenedor
make clean   # Limpiar todo
```

## Script de inicialización de BD

En `scripts/init-db.sql`:

```sql
-- Crear extensiones útiles
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Crear esquema inicial
CREATE TABLE IF NOT EXISTS usuarios (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    nombre VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices
CREATE INDEX idx_usuarios_email ON usuarios(email);

-- Datos de prueba
INSERT INTO usuarios (email, nombre) VALUES
    ('test@ejemplo.com', 'Usuario Test'),
    ('admin@ejemplo.com', 'Admin')
ON CONFLICT DO NOTHING;
```

## Tips y trucos

### 1. Variables de entorno con .env

Crea un `.env`:

```bash
POSTGRES_PASSWORD=super_secret_pass
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True
```

Y úsalo en docker-compose:

```yaml
services:
  db:
    env_file:
      - .env
```

### 2. Healthchecks son cruciales

Siempre añade healthchecks para evitar race conditions:

```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U $POSTGRES_USER"]
  interval: 10s
  timeout: 5s
  retries: 5
```

### 3. Named volumes para persistencia

```yaml
volumes:
  postgres_data:  # Named volume
  ./local:/data   # Bind mount
```

### 4. Networks personalizadas

Para proyectos complejos:

```yaml
networks:
  frontend:
  backend:

services:
  web:
    networks:
      - frontend
      - backend
  db:
    networks:
      - backend
```

## Monitorización con ctop

Instala `ctop` para monitorizar contenedores:

```bash
# Instalar
sudo wget https://github.com/bcicen/ctop/releases/download/v0.7.7/ctop-0.7.7-linux-amd64 -O /usr/local/bin/ctop
sudo chmod +x /usr/local/bin/ctop

# Usar
ctop
```

## Conclusión

Este setup me ha ahorrado **horas** de configuración en cada nuevo proyecto. Lo mejor: es reproducible y versionable con git.

El archivo está en mi [GitHub](https://github.com) si quieres la versión completa con más servicios (Elasticsearch, RabbitMQ, etc.).

¿Usas Docker Compose? ¿Qué servicios incluyes en tu setup?
