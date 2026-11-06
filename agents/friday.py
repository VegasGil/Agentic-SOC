from crewai import Agent, LLM
from tools.kql_runner import run_and_analyze # Debe ser esta

llm = LLM(model="ollama_chat/qwen2.5:3b", base_url="http://localhost:11434", temperature=0.1)

friday = Agent(
    role="Especialista DFIR",
    goal="Investigar alertas ejecutando playbooks KQL en Microsoft Defender y redactando informes.",
    backstory="Eres F.R.I.D.A.Y., una IA forense experta. Sabes usar KQL para encontrar el origen de un ataque.",
    tools=[run_and_analyze], # Debe usar run_and_analyze
    llm=llm,
    verbose=True,
    max_iter=5
)

def ejecutar_friday(equipo: str, incidente: str):
    from tools.kql_runner import run_and_analyze
    print("🕵️ F.R.I.D.A.Y. iniciando DFIR...")
    print("   -> Buscando Logins...")
    res1 = run_and_analyze.run(playbook_filename='dfir_fase1_identificacion.kql', equipo=equipo, incidente=incidente)
    print("   -> Buscando Procesos...")
    res2 = run_and_analyze.run(playbook_filename='dfir_fase2_procesos.kql', equipo=equipo, incidente=incidente)
    return f"Logins:\n{res1}\nProcesos:\n{res2}"