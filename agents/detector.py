import os
from crewai import Agent, LLM
from crewai.tools import tool

# Importamos las librerías de Sigma directamente
from sigma.collection import SigmaCollection
from sigma.backends.kusto import KustoBackend
from sigma.pipelines.microsoft365defender import microsoft_365_defender_pipeline

llm = LLM(model="ollama_chat/qwen2.5:3b", base_url="http://localhost:11434", temperature=0.1)

@tool("Traducir Sigma a KQL")
def convert_sigma_to_kql(sigma_file: str) -> str:
    """Usa pySigma para traducir una regla YAML de Sigma a KQL para Defender."""
    print(f"   -> [D.E.T.E.C.T.O.R.] Traduciendo {sigma_file} a KQL...")
    
    file_path = f"playbooks/{sigma_file}"
    if not os.path.exists(file_path):
        return f"Error: No se encontró el archivo {sigma_file}"
        
    try:
        # 1. Leer el archivo YAML
        with open(file_path, "r", encoding="utf-8") as f:
            yaml_data = f.read()
            
        # 2. Cargar la regla en Sigma
        sigma_rules = SigmaCollection.from_yaml(yaml_data)
        
        # 3. Inicializar el backend de Kusto con el pipeline de Defender
        backend = KustoBackend(processing_pipeline=microsoft_365_defender_pipeline())
        
        # 4. Convertir a KQL
        kql_queries = backend.convert(sigma_rules)
        
        return f"Regla KQL generada:\n{kql_queries[0]}"
    except Exception as e:
        return f"Error al traducir: {e}"

detector = Agent(
    role="Ingeniero de Detección (D.E.T.E.C.T.O.R.)",
    goal="Leer reglas Sigma y traducirlas a KQL para Defender.",
    backstory="Eres D.E.T.E.C.T.O.R., el experto en Detection-as-Code.",
    tools=[convert_sigma_to_kql],
    llm=llm,
    verbose=True,
    max_iter=3
)