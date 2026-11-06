from crewai import Agent, LLM
from tools.kql_runner import run_and_analyze
from tools.rbvm_enricher import prioritize_cves # <-- Nueva herramienta

llm = LLM(model="ollama_chat/qwen2.5:3b", base_url="http://localhost:11434", temperature=0.1)

karen = Agent(
    role="Gestor de Vulnerabilidades (RBVM)",
    goal="Identificar CVEs, enriquecerlas con EPSS/KEV y priorizar el parcheo.",
    backstory="Eres K.A.R.E.N., experta en Risk-Based Vulnerability Management.",
    tools=[run_and_analyze, prioritize_cves], # <-- Añadimos la herramienta
    llm=llm,
    verbose=True,
    max_iter=5
)

# ... (tu código actual de karen) ...

def ejecutar_karen(equipo: str):
    """Lógica encapsulada de K.A.R.E.N. para que Jarvis no sepa qué hace por dentro."""
    from tools.kql_runner import run_and_analyze
    from tools.rbvm_enricher import prioritize_cves
    
    print("🛡️ K.A.R.E.N. iniciando auditoría de vulnerabilidades...")
    
    # 1. Obtener CVEs
    print("   -> Buscando CVEs en Defender...")
    cves_json = run_and_analyze.run(
        playbook_filename='vuln_cve_equipo.kql', 
        equipo=equipo, 
        incidente="Auditoría de Vulnerabilidades"
    )
    
    # 2. Enriquecer
    print("   -> Enriqueciendo con EPSS y KEV...")
    reporte = prioritize_cves.run(cves_json)
    
    return reporte