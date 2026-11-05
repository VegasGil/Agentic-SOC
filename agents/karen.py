from crewai import Agent, LLM
from tools.kql_runner import run_playbook, write_report_with_ollama

llm = LLM(model="ollama_chat/qwen2.5:3b", base_url="http://localhost:11434", temperature=0.1)

karen = Agent(
    role="Gestor de Vulnerabilidades (RBVM)",
    goal="Identificar y priorizar vulnerabilidades.",
    backstory="Eres K.A.R.E.N., la analista de riesgos.",
    tools=[run_playbook, write_report_with_ollama],
    llm=llm,
    verbose=True,
    max_iter=5
)