from crewai import Agent, LLM
from tools.kql_runner import run_playbook, write_report_with_ollama

llm = LLM(model="ollama_chat/qwen2.5:3b", base_url="http://localhost:11434", temperature=0.1)

friday = Agent(
    role="Especialista DFIR",
    goal="Investigar incidentes ejecutando playbooks y redactando informes.",
    backstory="Eres F.R.I.D.A.Y., una IA forense experta.",
    tools=[run_playbook, write_report_with_ollama],
    llm=llm,
    verbose=True,
    max_iter=5
)