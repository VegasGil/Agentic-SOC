import pytest
from unittest.mock import MagicMock
# Importamos la función desde jarvis
from jarvis import procesar_alertas

def test_jarvis_router_mock(mocker):
    # 1. Simulamos la lista de alertas
    mock_alerts = [
        {"id": "1", "computerDnsName": "falex", "title": "XMRig Malware"},
        {"id": "2", "computerDnsName": "soc-appserver-01", "title": "CVE-2024-1234"},
        {"id": "3", "computerDnsName": "pc-01", "title": "Equipos Zombie"}
    ]
    
    # 2. Simulamos que el archivo de estado y alertas existen
    mocker.patch("jarvis.os.path.exists", return_value=True)
    mocker.patch("jarvis.open", mocker.mock_open(read_data="[]"), create=True)
    mocker.patch("jarvis.json.load", side_effect=[mock_alerts, []])
    mocker.patch("jarvis.json.dump")
    
    # 3. Simulamos la función de Splunk (para que no intente conectarse)
    mocker.patch("jarvis.fetch_splunk_alerts")
    
    # 4. Simulamos la CLASE Crew completa para evitar que CrewAI cargue sus archivos internos
    mock_crew_class = mocker.patch("jarvis.Crew")
    mock_crew_instance = mock_crew_class.return_value
    
    # 5. Hacemos que "Visión" devuelva las decisiones simuladas
    # Para el bucle: 1ra alerta -> FRIDAY, 2da -> KAREN, 3ra -> EDITH
    mock_crew_instance.kickoff.side_effect = [
        MagicMock(raw="FRIDAY"), 
        MagicMock(raw="KAREN"), 
        MagicMock(raw="EDITH")
    ]

    # 6. Simulamos la ejecución de la herramienta (Azure/Ollama)
    mock_tool = mocker.patch("jarvis.run_and_analyze")
    mock_tool.run.return_value = "Informe simulado."

    # 7. Ejecutamos Jarvis
    procesar_alertas()

    # 8. Verificamos que la herramienta de Azure se llamó
    # 4 veces: 2 de Friday, 1 de Karen, 1 de Edith
    assert mock_tool.run.call_count == 4