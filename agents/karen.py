import os
from crewai import Agent, LLM
from tools.kql_raw_fetcher import fetch_cves_raw
from tools.rbvm_enricher import prioritize_cves
from tools.aspm_tool import scan_application_aspm
from tools.verdict_sender import send_verdict
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

llm = LLM(model="ollama_chat/qwen2.5:3b", base_url="http://localhost:11434", temperature=0.1)

karen = Agent(
    role="Gestor de Vulnerabilidades (RBVM/ASPM)",
    goal="Identificar CVEs en infraestructura y código, priorizar el riesgo y enviar reportes a Splunk.",
    backstory="Eres K.A.R.E.N., experta en Risk-Based Vulnerability Management.",
    tools=[fetch_cves_raw, prioritize_cves, scan_application_aspm, send_verdict],
    llm=llm,
    verbose=True,
    max_iter=5
)

def ejecutar_karen(equipo: str, tipo_auditoria: str = "infraestructura"):
    print(f"🛡️ K.A.R.E.N. iniciando Auditoría ({tipo_auditoria})...")

    # --- BYPASS DEMO ---
    if os.getenv("AZURE_TENANT_ID") == "demo":
        print("   -> [DEMO MODE] K.A.R.E.N. simula la auditoría (sin Azure/Ollama).")
        if tipo_auditoria == "aspm":
            reporte_tecnico = "[DEMO] Escaneo ASPM simulado: 0 vulnerabilidades críticas."
        else:
            reporte_tecnico = (
                f"[DEMO] CVEs simuladas para {equipo}: "
                "CVE-2021-44228 (Critical, KEV: SÍ), CVE-2024-1234 (High). Prioridad: CRÍTICA."
            )
        informe_ejecutivo = (
            f"[DEMO] Informe ejecutivo K.A.R.E.N. para {equipo}: "
            "se detectaron CVEs críticas. Recomendación: PARCHE INMEDIATO (24h)."
        )
        print("   -> Enviando reporte a Splunk...")
        send_verdict.run(informe_ejecutivo, "K.A.R.E.N.")
        return informe_ejecutivo
    # --- FIN BYPASS DEMO ---

    if tipo_auditoria == "aspm":
        reporte_tecnico = scan_application_aspm.run(target_path=".")
    else:
        cves_json = fetch_cves_raw.run(equipo)
        reporte_tecnico = prioritize_cves.run(cves_json)

    print("   -> Solicitando a Ollama el informe ejecutivo...")
    ollama_base = os.getenv("OLLAMA_URL", "http://localhost:11434")
    client = OpenAI(base_url=f"{ollama_base}/v1", api_key="ollama")
    prompt = f"""Eres un experto en ciberseguridad y gestión de vulnerabilidades.
    Aquí tienes el reporte técnico de las CVEs encontradas:
    {reporte_tecnico}
    
    Instrucciones:
    1. Si el reporte dice 'Prioridad: CRÍTICA' o 'KEV: SÍ', tu recomendación debe ser 'PARCHE INMEDIATO (24h)'.
    2. Si el reporte dice 'Prioridad: BAJA', recomienda programar el parcheo.
    
    Redacta un resumen ejecutivo (máx 4 líneas) que sea directo y accionable.
    """
    
    try:
        response = client.chat.completions.create(
            model="qwen2.5:3b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        informe_ejecutivo = response.choices[0].message.content
    except Exception as e:
        informe_ejecutivo = f"(Error Ollama) Reporte técnico:\n{reporte_tecnico}"

    print("   -> Enviando reporte a Splunk...")
    send_verdict.run(informe_ejecutivo, "K.A.R.E.N.")
    
    return informe_ejecutivo