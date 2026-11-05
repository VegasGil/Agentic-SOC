from crewai import Agent, LLM
from tools.kql_runner import run_playbook, write_report_with_ollama

llm = LLM(model="ollama_chat/qwen2.5:3b", base_url="http://localhost:11434", temperature=0.1)

edith = Agent(
    role="Cazador de Amenazas",
    goal="Buscar anomalías ejecutando playbooks.",
    backstory="Eres E.D.I.T.H., un sistema proactivo.",
    tools=[run_playbook, write_report_with_ollama],
    llm=llm,
    verbose=True,
    max_iter=5
)