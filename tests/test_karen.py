from agents.karen import karen
from tools.kql_runner import run_and_analyze

def test_karen_agent_initialization():
    assert karen.role == "Gestor de Vulnerabilidades (RBVM)"
    assert run_and_analyze in karen.tools