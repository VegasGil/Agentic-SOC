from agents.edith import edith
from tools.kql_runner import run_and_analyze

def test_edith_agent_initialization():
    assert edith.role == "Cazador de Amenazas"
    assert run_and_analyze in edith.tools