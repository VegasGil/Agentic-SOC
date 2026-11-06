from crewai import Agent, LLM
from tools.kql_raw_fetcher import fetch_cves_raw # <-- Nueva herramienta
from tools.rbvm_enricher import prioritize_cves
from tools.aspm_tool import scan_application_aspm
from tools.verdict_sender import send_verdict
from openai import OpenAI

# ... (tu LLM y agente karen) ...
# (Asegúrate de añadir fetch_cves_raw a la lista de tools del agente)

def ejecutar_karen(equipo: str, tipo_auditoria: str = "infraestructura"):
    print(f"🛡️ K.A.R.E.N. iniciando Auditoría ({tipo_auditoria})...")
    
    if tipo_auditoria == "aspm":
        reporte_tecnico = scan_application_aspm.run(target_path=".")
    else:
        # 1. Buscar CVEs (Python puro, sin Ollama)
        cves_json = fetch_cves_raw.run(equipo)
        
        # 2. Priorizar
        reporte_tecnico = prioritize_cves.run(cves_json)

    # 3. Pasar a Ollama para redactar el informe final
    print("   -> Solicitando a Ollama el informe ejecutivo...")
    client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
    prompt = f"Eres un experto en ciberseguridad. Aquí tienes el reporte técnico:\n{reporte_tecnico}\nRedacta un resumen ejecutivo (máx 4 líneas)."
    
    try:
        response = client.chat.completions.create(
            model="qwen2.5:3b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        informe_ejecutivo = response.choices[0].message.content
    except Exception as e:
        informe_ejecutivo = f"(Error Ollama) Reporte técnico:\n{reporte_tecnico}"

    # 4. Enviar a Splunk
    send_verdict.run(informe_ejecutivo, "K.A.R.E.N.")
    return informe_ejecutivo