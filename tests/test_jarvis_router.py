import pytest
from unittest.mock import MagicMock
from jarvis import procesar_alertas

def test_jarvis_router_mock(mocker):
    # 1. Simulamos la lista de alertas
    mock_alerts = [
        {"id": "1", "computerDnsName": "falex", "title": "XMRig Malware"},
        {"id": "2", "computerDnsName": "soc-appserver-01", "title": "CVE-2024-1234"},
        {"id": "3", "computerDnsName": "pc-01", "title": "Equipos Zombie"}
    ]
    
    # 2. Simulamos la lectura de archivos
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("json.load", side_effect=[mock_alerts, []]) # 1ro alertas, 2do estado vacío
    mocker.patch("json.dump")
    
    # 3. Simulamos la función de Splunk
    mocker.patch("jarvis.fetch_splunk_alerts")
    
    # 4. Simulamos la ejecución de la herramienta (Azure + Ollama)
    mock_tool = mocker.patch("jarvis.run_and_analyze")
    mock_tool.run.return_value = "Informe simulado."

    # 5. Ejecutamos
    procesar_alertas()

    # 6. Verificamos que la herramienta de Azure se llamó (4 veces: 2 de Friday, 1 Karen, 1 Edith)
    assert mock_tool.run.call_count == 4