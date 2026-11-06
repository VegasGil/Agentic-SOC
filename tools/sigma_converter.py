# tools/sigma_converter.py
import sys

def convert_sigma_to_kql(yaml_content: str) -> str:
    try:
        from sigma.collection import SigmaCollection
        from sigma.backends.kusto import KustoBackend
        from sigma.pipelines.microsoft365defender import microsoft_365_defender_pipeline
        
        # Cargar la regla
        rules = SigmaCollection.from_yaml(yaml_content)
        
        # Configurar el backend con el pipeline de Defender
        backend = KustoBackend(processing_pipeline=microsoft_365_defender_pipeline())
        
        # Convertir
        kql_queries = backend.convert(rules)
        return kql_queries[0]
    except Exception as e:
        return f"Error en la traducción: {e}"

if __name__ == "__main__":
    # Prueba rápida con el YAML que tenías
    with open("playbooks/sigma_xmrig.yml", "r") as f:
        yaml_text = f.read()
    print(convert_sigma_to_kql(yaml_text))