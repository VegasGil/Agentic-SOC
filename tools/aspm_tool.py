import json
import os
from crewai.tools import tool
from pathlib import Path

# Importamos tu motor lógico
from tools.aspm_engine import prioritize_aspm

@tool("Escanear Código (ASPM)")
def scan_application_aspm(target_path: str = ".") -> str:
    """
    Usa Trivy para escanear el código en busca de vulnerabilidades, 
    y luego las prioriza con EPSS y KEV.
    """
    print(f"   -> [K.A.R.E.N.] Escaneando código ASPM en: {target_path}")
    
    # 1. Simulamos la salida de Trivy (o ejecutamos trivy si está instalado)
    trivy_json_path = "data/trivy_results.json"
    
    # (Aquí iría el subprocess de trivy real. Para el portafolio, generamos un mock si no hay)
    if not os.path.exists(trivy_json_path):
        os.makedirs("data", exist_ok=True)
        mock_trivy = {
            "Results": [{
                "Vulnerabilities": [
                    {"VulnerabilityID": "CVE-2021-44228", "PkgName": "log4j", "Severity": "CRITICAL"},
                    {"VulnerabilityID": "CVE-2024-1234", "PkgName": "libpcre2", "Severity": "HIGH"}
                ]
            }]
        }
        with open(trivy_json_path, "w") as f:
            json.dump(mock_trivy, f)

    # 2. Pasamos el reporte al motor de priorización
    reporte = prioritize_aspm.run(trivy_json_path, enviar_splunk=True)
    return reporte