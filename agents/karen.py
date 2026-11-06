from crewai import Agent, LLM
from tools.kql_runner import run_and_analyze
from tools.rbvm_enricher import prioritize_cves
from tools.aspm_tool import scan_application_aspm # <-- Nueva

llm = LLM(model="ollama_chat/qwen2.5:3b", base_url="http://localhost:11434", temperature=0.1)

karen = Agent(
    role="Gestor de Vulnerabilidades (RBVM/ASPM)",
    goal="Identificar CVEs en infraestructura (Defender) y código (ASPM), enriquecerlas y priorizar.",
    backstory="Eres K.A.R.E.N., experta en Risk-Based Vulnerability Management.",
    tools=[run_and_analyze, prioritize_cves, scan_application_aspm],
    llm=llm,
    verbose=True,
    max_iter=5
)

# Y actualizamos su ejecutor
def ejecutar_karen(equipo: str, tipo_auditoria: str = "infraestructura"):
    print(f"🛡️ K.A.R.E.N. iniciando Auditoría ({tipo_auditoria})...")
    
    if tipo_auditoria == "aspm":
        # Escaneo de Código
        return scan_application_aspm.run(target_path=".")
    else:
        # Escaneo de Infraestructura (Defender)
        cves_json = run_and_analyze.run(
            playbook_filename='vuln_cve_equipo.kql', 
            equipo=equipo, 
            incidente="Auditoría de Vulnerabilidades"
        )
        return prioritize_cves.run(cves_json)