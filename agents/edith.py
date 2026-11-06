from crewai import Agent, LLM
from tools.kql_runner import run_and_analyze
from tools.verdict_sender import send_verdict
from tools.sigma_hunter import hunt_with_sigma # <-- NUEVA HERRAMIENTA

llm = LLM(model="ollama_chat/qwen2.5:3b", base_url="http://localhost:11434", temperature=0.1)

edith = Agent(
    role="Cazador de Amenazas",
    goal="Buscar anomalías ejecutando playbooks KQL o reglas Sigma, y enviar reportes a Splunk.",
    backstory="Eres E.D.I.T.H., un sistema proactivo. No esperas a que salte la alarma; tú sales a buscar al enemigo usando lo último en detección (Sigma).",
    tools=[run_and_analyze, send_verdict, hunt_with_sigma], # <-- Añadida
    llm=llm,
    verbose=True,
    max_iter=5
)

# Función original (Equipos Zombie)
def ejecutar_edith(equipo: str):
    print("🎯 E.D.I.T.H. iniciando Threat Hunting (Equipos Zombie)...")
    reporte_tecnico = run_and_analyze.run(
        playbook_filename='hunting_zombie_machines.kql', 
        equipo=equipo, 
        incidente="Auditoría de Equipos Zombie"
    )
    send_verdict.run(reporte_tecnico, "E.D.I.T.H.")
    return reporte_tecnico

# NUEVA FUNCIÓN: Caza con Sigma (Movimiento Lateral, PowerShell Ofuscado, etc.)
def ejecutar_edith_sigma(equipo: str):
    print("🎯 E.D.I.T.H. iniciando Caza basada en Sigma (MITRE ATT&CK)...")
    
    # Aquí apuntamos a la regla Sigma que creamos
    ruta_sigma = "playbooks/sigma_hunting_mitre.yml"
    
    print(f"   -> Analizando regla: {ruta_sigma}")
    reporte = hunt_with_sigma.run(ruta_sigma, equipo)
    
    print("   -> Enviando reporte a Splunk...")
    send_verdict.run(reporte, "E.D.I.T.H. (Sigma Hunting)")
    
    return reporte