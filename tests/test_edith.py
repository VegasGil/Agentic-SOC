from agents.edith import edith
from tools.kql_runner import run_and_analyze

def test_edith_agent_initialization():
    assert edith.role == "Cazador de Amenazas"
    assert run_and_analyze in edith.tools
# Al final de tu test_edith.py actual
def test_edith_sigma_hunting(mocker):
    # Simulamos la herramienta de caza con Sigma
    mock_hunt = mocker.patch("agents.edith.hunt_with_sigma")
    mock_hunt.run.return_value = "Informe Sigma simulado"
    
    mock_send = mocker.patch("agents.edith.send_verdict")
    mock_send.run.return_value = "Enviado"

    from agents.edith import ejecutar_edith_sigma
    resultado = ejecutar_edith_sigma("falex")

    assert resultado == "Informe Sigma simulado"
    mock_hunt.run.assert_called_once()
    mock_send.run.assert_called_once()