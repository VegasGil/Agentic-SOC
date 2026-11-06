from crewai import Agent, LLM
from tools.kql_runner import run_and_analyze # <-- Importamos la herramienta nueva

llm = LLM(model="ollama_chat/qwen2.5:3b", base_url="http://localhost:11434", temperature=0.1)

edith = Agent(
    role="Cazador de Amenazas",
    goal="Buscar anomalías ejecutando playbooks.",
    backstory="Eres E.D.I.T.H., un sistema proactivo.",
    tools=[run_and_analyze], # <-- Usamos SOLO la herramienta nueva
    llm=llm,
    verbose=True,
    max_iter=5
)

def ejecutar_edith(equipo: str):
    from tools.kql_runner import run_and_analyze
    print("🎯 E.D.I.T.H. iniciando Threat Hunting...")
    return run_and_analyze.run(playbook_filename='hunting_zombie_machines.kql', equipo=equipo, incidente="Auditoría de Equipos")