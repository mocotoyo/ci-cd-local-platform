# Proyecto Final – Plataforma Local de CI/CD, Observabilidad y Seguridad

[![GitHub Actions](https://img.shields.io/github/workflow/status/mocotoyo/ci-cd-local-platform/CI%20Pipeline)](https://github.com/mocotoyo/ci-cd-local-platform/actions)
[![Docker](https://img.shields.io/badge/docker-ready-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

---

## Tabla de Contenidos
1. [Arquitectura General](#1-arquitectura-general)
2. [Estructura del Repositorio](#2-estructura-del-repositorio)
3. [Despliegue Local](#3-despliegue-local)
4. [Aplicación](#4-aplicación)
5. [CI/CD – GitHub Actions](#5-cicd--github-actions)
6. [Observabilidad – Logs (ELK)](#6-observabilidad--logs-elk)
7. [Métricas y Alertas](#7-métricas-y-alertas)
8. [Seguridad – Vault + Trivy](#8-seguridad--vault--trivy)
9. [Operación en Producción](#9-operación-en-producción)
10. [Evidencias para Certificación](#10-evidencias-para-certificación)
11. [Conclusión](#11-conclusión)

---

## 1. Arquitectura General

Tecnologías principales:

- **Docker Desktop + Docker Compose**
- **Aplicación:** Python (Flask)
- **CI/CD:** GitHub Actions
- **Observabilidad:** ELK (Elasticsearch, Logstash, Kibana)
- **Métricas y alertas:** Prometheus + Grafana
- **Seguridad:** Trivy + HashiCorp Vault
- **Operación:** Nginx (Load Balancer), healthchecks, restart policies

**Flujo:**

1. Commit en GitHub
2. Pipeline CI:
   - Build de imagen
   - Escaneo de seguridad (Trivy)
   - Bloqueo si hay vulnerabilidades HIGH/CRITICAL
3. Despliegue local con Docker Compose
4. Observabilidad y monitoreo activos
5. Simulación de fallos y escalabilidad

---

## 2. Estructura del Repositorio

ci-cd-local-platform/
├── app/
│ ├── app.py
│ ├── Dockerfile
│ └── requirements.txt
├── nginx/
│ └── nginx.conf
├── logstash/
│ └── pipeline/logstash.conf
├── prometheus/
│ └── prometheus.yml
├── docker-compose.yml
├── .github/
│ └── workflows/ci.yml
├── docs/
│ ├── arquitectura.md
│ └── evidencias.md
└── README.md

yaml
Copiar código

---

## 3. Despliegue Local

```bash
# Clonar repositorio
git clone git@github.com:mocotoyo/ci-cd-local-platform.git
cd ci-cd-local-platform

# Construir imágenes Docker
docker compose build

# Levantar la plataforma
docker compose up -d
Acceso a servicios:

App: http://localhost:8080

Grafana: http://localhost:3000

Kibana: http://localhost:5601

Prometheus: http://localhost:9090

Vault: http://localhost:8200

4. Aplicación
app/app.py:

python
Copiar código
from flask import Flask
import logging
from prometheus_client import Counter, generate_latest

app = Flask(__name__)
REQUESTS = Counter('app_requests_total', 'Total requests')

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

@app.route("/")
def hello():
    REQUESTS.inc()
    app.logger.info("Request received")
    return "Hello CI/CD Local Platform"

@app.route("/health")
def health():
    return "OK", 200

@app.route("/metrics")
def metrics():
    return generate_latest()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
app/Dockerfile:

dockerfile
Copiar código
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]
5. CI/CD – GitHub Actions
.github/workflows/ci.yml:

yaml
Copiar código
name: CI Pipeline
on: [push]

jobs:
  build-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build image
        run: docker build -t local-app:${{ github.sha }} app/

      - name: Trivy Scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: local-app:${{ github.sha }}
          severity: CRITICAL,HIGH
          exit-code: 1
Justificación certificación:

Integración real de seguridad en CI

Falla el pipeline ante riesgos críticos (DevSecOps real)

6. Observabilidad – Logs (ELK)
logstash/pipeline/logstash.conf:

conf
Copiar código
input {
  tcp {
    port => 5001
    codec => json
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
  }
}
Kibana permite visualizar logs centralizados de todas las instancias de la app.

7. Métricas y Alertas
prometheus/prometheus.yml:

yaml
Copiar código
scrape_configs:
  - job_name: "app"
    static_configs:
      - targets: ["app1:5000", "app2:5000"]
Grafana:

Requests por segundo

Disponibilidad de servicios

Alertas por caída de instancias

8. Seguridad – Vault + Trivy
Vault se utiliza para gestión de secretos:

bash
Copiar código
vault kv put secret/app DB_PASSWORD=supersecret
Trivy en CI/CD bloquea despliegues si hay vulnerabilidades HIGH/CRITICAL.

Justificación:

Buenas prácticas DevSecOps

Simulación de entorno productivo seguro

9. Operación en Producción
nginx/nginx.conf:

nginx
Copiar código
upstream app {
  server app1:5000;
  server app2:5000;
}

server {
  listen 80;
  location / {
    proxy_pass http://app;
  }
}
Alta disponibilidad: 2 instancias de la app

Restart automático de contenedores

Healthchecks activos

Balanceo de carga con Nginx

10. Evidencias para Certificación
En docs/evidencias.md:

Capturas de Grafana dashboards

Logs centralizados en Kibana

Pipeline CI bloqueando despliegues con Trivy

Balanceo Nginx funcionando con múltiples instancias

Aplicación reiniciándose tras fallos

11. Conclusión
Este proyecto demuestra competencias prácticas en:

DevOps

DevSecOps

Observabilidad

Operación de plataformas locales

Alineado a certificaciones como:

DevOps Engineer

SRE / Platform Engineer

Kubernetes / Cloud-Native (entorno local)


