from crewai import Agent, LLM
from tools.kql_runner import run_and_analyze
from tools.verdict_sender import send_verdict # <-- NUEVA HERRAMIENTA

llm = LLM(model="ollama_chat/qwen2.5:3b", base_url="http://localhost:11434", temperature=0.1)

friday = Agent(
    role="Especialista DFIR",
    goal="Investigar alertas ejecutando playbooks KQL en Microsoft Defender y redactando informes.",
    backstory="Eres F.R.I.D.A.Y., una IA forense experta. Sabes usar KQL para encontrar el origen de un ataque.",
    tools=[run_and_analyze, send_verdict], # <-- Añadida al agente
    llm=llm,
    verbose=True,
    max_iter=5
)

def ejecutar_friday(equipo: str, incidente: str):
    print("🕵️ F.R.I.D.A.Y. iniciando DFIR...")
    print("   -> Buscando Logins...")
    res1 = run_and_analyze.run(playbook_filename='dfir_fase1_identificacion.kql', equipo=equipo, incidente=incidente)
    
    print("   -> Buscando Procesos...")
    res2 = run_and_analyze.run(playbook_filename='dfir_fase2_procesos.kql', equipo=equipo, incidente=incidente)
    
    reporte_final = f"Logins:\n{res1}\nProcesos:\n{res2}"
    
    # Enviar a Splunk automáticamente
    print("   -> Enviando reporte a Splunk...")
    send_verdict.run(reporte_final, "F.R.I.D.A.Y.")
    
    return reporte_final

def ejecutar_edith_hunting(equipo: str):
    print("🎯 E.D.I.T.H. iniciando Caza Proactiva (0-Day / LotL)...")
    
    print("   -> Buscando descargas sospechosas en Azure...")
    reporte = run_and_analyze.run(
        playbook_filename='hunting_suspicious_processes.kql', 
        equipo=equipo, 
        incidente="Caza de Amenazas (Comportamiento Anómalo)"
    )
    
    print("   -> Enviando reporte a Splunk...")
    send_verdict.run(reporte, "E.D.I.T.H.")
    
    return reporte