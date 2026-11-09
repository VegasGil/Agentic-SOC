import os
from crewai import Agent, LLM

llm = LLM(
    model="ollama_chat/qwen2.5:3b",
    base_url=os.getenv("OLLAMA_URL", "http://localhost:11434"),
    temperature=0.1
)

vision = Agent(
    role="Analista de Triaje (Visión)",
    goal="Leer la alerta inicial y determinar de qué tipo de incidente se trata (DFIR o Hunting).",
    backstory="Eres V.I.S.I.O.N., el primer filtro del SOC. Tu trabajo es leer la alerta de Nirvana y decir a quién despertar.",
    llm=llm,
    verbose=True
)