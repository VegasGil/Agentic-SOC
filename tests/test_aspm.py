import json
import os
from tools.aspm_engine import prioritize_aspm

def test_aspm_prioritization(tmp_path):
    # 1. Crear un archivo de Trivy falso
    trivy_data = {
        "Results": [{
            "Vulnerabilities": [
                {"VulnerabilityID": "CVE-2021-44228", "PkgName": "log4j", "Severity": "CRITICAL"},
                {"VulnerabilityID": "CVE-2024-1234", "PkgName": "libpcre2", "Severity": "HIGH"}
            ]
        }]
    }
    trivy_file = tmp_path / "trivy_results.json"
    trivy_file.write_text(json.dumps(trivy_data))

    # 2. Ejecutar el motor SIN enviar a Splunk (enviar_splunk=False)
    resultado = prioritize_aspm.run(str(trivy_file), enviar_splunk=False)
    
    # 3. Verificar
    assert "CVE-2021-44228" in resultado
    assert "CVE-2024-1234" in resultado
    # Log4j debe tener mayor riesgo que libpcre2
    pos_log4j = resultado.find("CVE-2021-44228")
    pos_libpcre = resultado.find("CVE-2024-1234")
    assert pos_log4j < pos_libpcre, "Log4j debería estar primero"