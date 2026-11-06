# 🛡️ Agentic-SOC: El Centro de Operaciones de Seguridad Autónomo

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![CrewAI](https://img.shields.io/badge/AI-CrewAI-red.svg)](https://www.crewai.com/)
[![Ollama](https://img.shields.io/badge/AI-Ollama%20(Local)-orange.svg)](https://ollama.com/)
[![Splunk](https://img.shields.io/badge/SIEM-Splunk-green.svg)](https://www.splunk.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Agentic-SOC** es la evolución de una arquitectura de ciberseguridad tradicional hacia un **SOC Multi-Agente (SOAR)**. Utiliza Inteligencia Artificial local orquestada mediante agentes autónomos (CrewAI) para investigar alertas de seguridad, buscar amenazas de forma proactiva y priorizar vulnerabilidades basándose en riesgo real.

Inspirado en los sistemas de Marvel, cada agente tiene una especialidad única, coordinados por un núcleo central.

> 🎥 **** *(Próximamente)*

# 🏗️ Arquitectura del Flujo (El Ecosistema)

El sistema está diseñado bajo una arquitectura de microservicios para IA, donde el orquestador delega el trabajo pesado a agentes especializados.

```mermaid
graph TD
    A[Alertas de Splunk] -->|Lectura| B(J.A.R.V.I.S. - Orquestador)
    B -->|Triaje| C(V.I.S.I.O.N. - Analista)
    
    C -->|Incidente DFIR| D[F.R.I.D.A.Y.]
    C -->|Auditoria Red| E[E.D.I.T.H.]
    C -->|Auditoria Codigo| F[K.A.R.E.N.]
    C -->|Desconocido| G[Escalado a Humano]

    D -->|Investigacion| H(Microsoft Defender)
    E -->|Busqueda Proactiva| H
    F -->|Busqueda CVEs| H

    H -.->|Evidencia| I(Carpeta /data)
    
    D -->|Analisis| J(Ollama Local)
    E -->|Analisis| J
    F -->|EPSS/KEV| J

 Los Agentes (El Equipo)
1. J.A.R.V.I.S. (El Orquestador)

Es el director del SOC. Se encarga de leer las alertas entrantes de Splunk, coordinar al agente de triaje (Visión) y llamar al especialista adecuado (F.R.I.D.A.Y., E.D.I.T.H. o K.A.R.E.N.) dependiendo de la naturaleza del incidente.
2. V.I.S.I.O.N. (Analista de Triaje)

El primer filtro. Lee la alerta cruda y decide, basándose en el contexto, qué agente debe investigar. Si no reconoce la amenaza, la escala a un humano.
3. F.R.I.D.A.Y. (Especialista DFIR)

Rápida y resolutiva. Es la encargada de los Incidentes (DFIR). Cuando Visión detecta Malware o Ransomware, Friday se conecta a Microsoft Defender, ejecuta playbooks KQL (búsqueda de logins, procesos, conexiones de red), guarda la evidencia y redacta el informe forense.
4. E.D.I.T.H. (Cazador de Amenazas)

Encuentra lo que otros no ven. Se encarga del Threat Hunting proactivo. Audita la infraestructura en busca de "Equipos Zombie" (máquinas encendidas sin uso humano) o comportamientos anómalos, sin esperar a que salte una alarma.
5. K.A.R.E.N. (Gestora de Vulnerabilidades y ASPM)

Analiza el entorno y el código. Es la experta en RBVM (Risk-Based Vulnerability Management). Busca CVEs en los endpoints (Defender) y en el código (Trivy/ASPM). Cruza los resultados con las bases de datos de EPSS (probabilidad de explotación) y CISA KEV (explotación activa) para priorizar qué parchear primero. Se actualiza automáticamente cada 24h.
6. D.E.T.E.C.T.O.R. (Traductor Sigma)

El ingeniero de detección. Convierte reglas universales Sigma (YAML) en consultas KQL nativas para Defender, garantizando la portabilidad del código.
🚀 Despliegue Rápido (Instalación)

    Clona el repositorio:
    bash

    git clone https://github.com/VegasGil/Agentic-SOC.git
    cd Agentic-SOC

    Instala las dependencias:
    bash

    python -m venv .venv
    source .venv/bin/activate  # En Windows: .\.venv\Scripts\activate
    pip install -r requirements.txt

    Configura tus variables de entorno (.env):
    Necesitarás las credenciales de Splunk, Azure (Defender) y un modelo local en Ollama.
    dotenv

    # Ollama
    OLLAMA_URL=http://localhost:11434/api/chat
    OLLAMA_MODEL=qwen2.5:3b

    # Splunk
    SPLUNK_HOST=tu_ip
    SPLUNK_REST_PORT=8089
    SPLUNK_USER=admin
    SPLUNK_PASS=tu_password
    HEC_TOKEN=tu_hec_token

    # Azure (Defender)
    AZURE_TENANT_ID=tu_tenant
    AZURE_CLIENT_ID=tu_client
    AZURE_CLIENT_SECRET=tu_secret

    Inicia Ollama en segundo plano:
    bash

    ollama run qwen2.5:3b

    Ejecuta el Orquestador:
    bash

    python jarvis.py

🧪 Testing y CI/CD

El proyecto cuenta con un pipeline de GitHub Actions que garantiza que el código no se rompa y que los agentes estén correctamente configurados.

    Pytest: 10 tests unitarios con mocks (no dependen de red ni credenciales).

    Semgrep (SAST): Análisis estático del código Python.

    Trivy (SCA): Escaneo de dependencias vulnerables.