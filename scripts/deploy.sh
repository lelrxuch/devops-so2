#!/bin/bash
# ============================================================
#  deploy.sh  Script de despliegue automatizado
#  Proyecto DevOps SO2
# ============================================================
set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log()  { echo -e "${GREEN}[]${NC} $1"; }
warn() { echo -e "${YELLOW}[!]${NC} $1"; }
err()  { echo -e "${RED}[]${NC} $1"; exit 1; }

echo ""
echo "=============================================="
echo "   DEPLOY  Infraestructura DevOps SO2"
echo "=============================================="
echo ""

#  1. Verificar Docker 
log "Verificando Docker..."
docker info > /dev/null 2>&1 || err "Docker no est corriendo. Incialo primero."
log "Docker OK"

#  2. Verificar modo Swarm 
SWARM_STATUS=$(docker info --format '{{.Swarm.LocalNodeState}}' 2>/dev/null)
if [ "$SWARM_STATUS" != "active" ]; then
    warn "Swarm no activo. Inicializando Docker Swarm..."
    docker swarm init --advertise-addr 127.0.0.1 || true
    log "Swarm inicializado"
else
    log "Docker Swarm activo"
fi

#  3. Variables de entorno 
export DOCKER_USERNAME=${DOCKER_USERNAME:-"yourusername"}
export IMAGE_TAG=${IMAGE_TAG:-"latest"}

warn "Usando imagen: ${DOCKER_USERNAME}/devops-so2-app:${IMAGE_TAG}"

#  4. Build de imgenes locales 
log "Construyendo imagen de la aplicacin..."
docker build -t ${DOCKER_USERNAME}/devops-so2-app:${IMAGE_TAG} ./app
log "Imagen construida"

log "Construyendo imagen de Nginx..."
docker build -t devops-so2-nginx:latest ./nginx
log "Nginx construido"

#  5. Deploy del stack 
log "Desplegando stack en Docker Swarm..."
docker stack deploy -c docker-compose.yml devops_stack
log "Stack desplegado"

#  6. Esperar servicios 
log "Esperando que los servicios inicien (30s)..."
sleep 30

#  7. Verificar servicios 
echo ""
echo "Estado de los servicios:"
docker stack services devops_stack

#  8. Health check 
echo ""
log "Verificando health check de la aplicacin..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/health || echo "000")
if [ "$HTTP_CODE" = "200" ]; then
    log "Aplicacin respondiendo correctamente! HTTP $HTTP_CODE"
else
    warn "Aplicacin retorn HTTP $HTTP_CODE  puede estar iniciando todava"
fi

echo ""
echo "=============================================="
echo "   DEPLOY COMPLETADO"
echo "=============================================="
echo "  App:        http://localhost"
echo "  Prometheus: http://localhost:9090"
echo "  Grafana:    http://localhost:3000  (admin/admin123)"
echo "=============================================="
echo ""
