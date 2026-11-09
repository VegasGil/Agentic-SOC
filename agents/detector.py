from crewai import Agent, LLM
from tools.sigma_converter import convert_sigma_to_kql
import os

llm = LLM(
    model="ollama_chat/qwen2.5:3b",
    base_url=os.getenv("OLLAMA_URL", "http://localhost:11434"),
    temperature=0.1
)

detector = Agent(
    role="Ingeniero de Detección (D.E.T.E.C.T.O.R.)",
    goal="Leer reglas Sigma (YAML) y traducirlas a KQL para Microsoft Defender.",
    backstory="Eres D.E.T.E.C.T.O.R., el experto en Detection-as-Code. Sabes convertir reglas universales a lenguajes nativos.",
    tools=[convert_sigma_to_kql],
    llm=llm,
    verbose=True,
    max_iter=3
)

def ejecutar_detector(ruta_sigma: str):
    """Lee un archivo YAML y lo traduce a KQL."""
    if not os.path.exists(ruta_sigma):
        return f"Error: No se encontró el archivo {ruta_sigma}"
        
    with open(ruta_sigma, "r", encoding="utf-8") as f:
        yaml_content = f.read()
        
    print(f"⚙️ D.E.T.E.C.T.O.R. traduciendo {ruta_sigma}...")
    kql = convert_sigma_to_kql.run(yaml_content)
    return kql