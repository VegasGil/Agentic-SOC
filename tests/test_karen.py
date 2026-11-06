from agents.karen import karen
from tools.kql_runner import run_and_analyze
from tools.rbvm_enricher import prioritize_cves
from tools.aspm_tool import scan_application_aspm

def test_karen_agent_initialization():
    # Actualizado al nuevo rol que incluye ASPM
    assert karen.role == "Gestor de Vulnerabilidades (RBVM/ASPM)"
    assert run_and_analyze in karen.tools
    assert prioritize_cves in karen.tools
    assert scan_application_aspm in karen.tools