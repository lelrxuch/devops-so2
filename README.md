#  Proyecto Final  Infraestructura DevOps en la Nube
### Sistemas Operativos II | Universidad Mariano Glvez

[![CI/CD Pipeline](https://github.com/TU_USUARIO/devops-so2/actions/workflows/cicd.yml/badge.svg)](https://github.com/TU_USUARIO/devops-so2/actions)
[![Docker Pulls](https://img.shields.io/docker/pulls/TU_USUARIO/devops-so2-app)](https://hub.docker.com/r/TU_USUARIO/devops-so2-app)

##  Descripcin

Infraestructura DevOps completa implementada con Docker, GitHub Actions CI/CD, Nginx como reverse proxy, PostgreSQL, y monitoreo con Prometheus + Grafana. Desplegada en **Render.com** (cloud gratuito).

##  Tecnologas

| Categora | Tecnologa |
|-----------|-----------|
| Contenedores | Docker, Docker Swarm |
| CI/CD | GitHub Actions |
| Registry | Docker Hub |
| Cloud | Render.com (free tier) |
| App | Python Flask + Gunicorn |
| Proxy | Nginx |
| Base de datos | PostgreSQL 16 |
| Monitoreo | Prometheus + Grafana |

##  Arquitectura

```
Usuario
   
   
Nginx (puerto 80)  Reverse Proxy
   
   
Flask App (puerto 5000)  2 rplicas (Swarm)
   
   
PostgreSQL (puerto 5432)

GitHub  GitHub Actions  Docker Hub  Render.com
```

##  Inicio Rpido (local)

```bash
# 1. Clonar el repositorio
git clone https://github.com/TU_USUARIO/devops-so2.git
cd devops-so2

# 2. Levantar con Docker Compose
docker compose up -d

# 3. Verificar que todo corre
docker compose ps

# 4. Abrir la app
open http://localhost
```

##  Deploy en la Nube (Render.com)

1. Crear cuenta en [render.com](https://render.com) (gratuito, sin tarjeta)
2. Conectar tu repositorio de GitHub
3. Crear **Web Service**  seleccionar el repositorio
4. Configurar:
   - **Runtime:** Docker
   - **Dockerfile path:** `./app/Dockerfile`
   - **Port:** 5000
5. Agregar variables de entorno:
   - `APP_ENV=production`
6. Click **Deploy**

##  Pipeline CI/CD

El pipeline se activa automticamente con cada `git push` a `main`:

```
Push a main
    
    
[CI] Instalar dependencias
    
    
[CI] Ejecutar pruebas
    
    
[CI] Build imagen Docker
    
    
[CI] Health check del contenedor
    
    
[CD] Push a Docker Hub
    
    
[CD] Deploy automtico a Render.com
    
    
[CD] Verificacin final
```

### Secrets necesarios en GitHub

| Secret | Descripcin |
|--------|-------------|
| `DOCKER_USERNAME` | Tu usuario de Docker Hub |
| `DOCKER_TOKEN` | Token de acceso de Docker Hub |
| `RENDER_SERVICE_ID` | ID del servicio en Render |
| `RENDER_API_KEY` | API Key de Render |
| `RENDER_APP_URL` | URL de tu app en Render |

##  Monitoreo

| Servicio | URL | Credenciales |
|----------|-----|-------------|
| App | http://localhost |  |
| Prometheus | http://localhost:9090 |  |
| Grafana | http://localhost:3000 | admin / admin123 |

##  Docker Swarm

```bash
# Inicializar Swarm
docker swarm init

# Desplegar stack completo
bash scripts/deploy.sh

# Ver servicios
docker stack services devops_stack

# Escalar la app a 3 rplicas
docker service scale devops_stack_app=3
```

##  Estructura del Proyecto

```
devops-so2/
 app/
    app.py              # Aplicacin Flask
    Dockerfile          # Multi-stage build
    requirements.txt
 nginx/
    Dockerfile
    nginx.conf          # Reverse proxy config
 monitoring/
    prometheus.yml      # Configuracin Prometheus
 scripts/
    deploy.sh           # Script de despliegue
 .github/workflows/
    cicd.yml            # Pipeline GitHub Actions
 docker-compose.yml      # Entorno completo local
 docker-stack.yml        # Docker Swarm stack
 README.md
```

##  Autores

Proyecto Final  Sistemas Operativos II  
Universidad Mariano Glvez de Guatemala  
2025
# Pipeline test
