#!/bin/bash
set -e

echo "======================================"
echo " Generando Dockerfile"
echo "======================================"

cat << 'EOF' > Dockerfile
FROM python:3.11-slim

WORKDIR /app

ENV PIP_PROGRESS_BAR=off
ENV PIP_NO_CACHE_DIR=1
ENV VALORANT_API_LANGUAGE=es-ES
ENV AGENTE_VALORANT=Gekko

COPY requirements.txt .
RUN python -m pip install --no-cache-dir --progress-bar off -r requirements.txt

COPY app.py .

CMD ["python", "app.py"]
EOF

echo "======================================"
echo " Construyendo imagen Docker"
echo "======================================"

docker build -t valorant-agent-advisor .

echo "======================================"
echo " Eliminando contenedor previo si existe"
echo "======================================"

docker rm -f samplerunning 2>/dev/null || true

echo "======================================"
echo " Ejecutando contenedor"
echo "======================================"

docker run --name samplerunning -e AGENTE_VALORANT=Gekko valorant-agent-advisor

echo "======================================"
echo " Contenedor finalizado correctamente"
echo "======================================"