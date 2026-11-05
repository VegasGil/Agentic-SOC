from crewai import Crew, Task
from agents.friday import friday
from agents.edith import edith
from agents.karen import karen
from agents.vision import vision

# Importamos las herramientas
from tools.splunk_reader import get_latest_alert
from tools.kql_runner import write_report_with_ollama, run_and_analyze

# 1. Configuramos las herramientas de cada agente
# Friday lee de Splunk
friday.tools = [get_latest_alert, write_report_with_ollama]
# Edith y Karen van directo a Azure
edith.tools = [run_and_analyze]
karen.tools = [run_and_analyze]

def procesar_alerta(alerta_texto: str):
    print(f"\n🚨 ALERTA RECIBIDA: {alerta_texto}\n")
    
    # --- PASO 1: VISIÓN DECIDE QUIÉN ACTÚA ---
    tarea_decision = Task(
        description=f"""Analiza esta alerta: '{alerta_texto}'.
        Si es un incidente de seguridad (Ransomware, Malware, Logins, EICAR), responde EXACTAMENTE con: FRIDAY.
        Si es una solicitud de auditoría (Equipos Zombie), responde EXACTAMENTE con: EDITH.
        Si es una solicitud de vulnerabilidades (CVE), responde EXACTAMENTE con: KAREN.""",
        expected_output="La palabra FRIDAY, EDITH o KAREN.",
        agent=vision
    )
    
    crew_decision = Crew(agents=[vision], tasks=[tarea_decision], verbose=False)
    decision = crew_decision.kickoff().raw.strip().upper()
    
    print(f"🤖 J.A.R.V.I.S. ha decidido: {decision}")
    
    # --- PASO 2: ENRUTAMIENTO ---
    if "FRIDAY" in decision:
        print("🕵️ Despertando a F.R.I.D.A.Y. para análisis DFIR...")
        tarea_friday = Task(
            description="""Sigue estos pasos estrictamente:
            1. Usa la herramienta 'Buscar Ultima Alerta en Splunk'.
            2. Toma el TEXTO EXACTO que devuelve esa herramienta.
            3. Pasa ese texto como 'contexto' a 'Redactar Informe Forense con Ollama', usando 'Alerta de Defender' como 'incidente'.""",
            expected_output="Informe forense redactado.",
            agent=friday
        )
        crew = Crew(agents=[friday], tasks=[tarea_friday], verbose=True)
        print("\n=== RESULTADO ===")
        print(crew.kickoff())
        
    elif "EDITH" in decision:
        print("🎯 Despertando a E.D.I.T.H. para Threat Hunting...")
        tarea_edith = Task(
            description="""Usa la herramienta 'Ejecutar y Analizar Playbook' con: playbook_filename='hunting_zombie_machines.kql', equipo='cualquiera', incidente='Auditoría de Equipos'.""",
            expected_output="Informe de equipos redactado.",
            agent=edith
        )
        crew = Crew(agents=[edith], tasks=[tarea_edith], verbose=True)
        print("\n=== RESULTADO ===")
        print(crew.kickoff())
        
    elif "KAREN" in decision:
        print("🛡️ Despertando a K.A.R.E.N. para auditoría de vulnerabilidades...")
        tarea_karen = Task(
            description="""Usa la herramienta 'Ejecutar y Analizar Playbook' con: playbook_filename='vuln_cve_equipo.kql', equipo='falex', incidente='Auditoría de Vulnerabilidades'.""",
            expected_output="Informe de vulnerabilidades redactado.",
            agent=karen
        )
        crew = Crew(agents=[karen], tasks=[tarea_karen], verbose=True)
        print("\n=== RESULTADO ===")
        print(crew.kickoff())
    else:
        print("⚠️ J.A.R.V.I.S. no pudo determinar qué agente usar. Respuesta:", decision)

if __name__ == "__main__":
    # Prueba: Simulamos una alerta de Ransomware que envía Nirvana
    alerta = "Process created: vssadmin.exe delete shadows /all /quiet en el host falex"
    procesar_alerta(alerta)