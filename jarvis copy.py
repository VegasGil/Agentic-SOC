import os
import json
from crewai import Crew, Task
from agents.vision import vision
from tools.splunk_reader import fetch_splunk_alerts
from tools.kql_runner import run_and_analyze
from agents.friday import friday

STATE_FILE = "data/state_alerts.json"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return []

def save_state(state):
    os.makedirs("data", exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def procesar_alertas():
    # 1. Traer alertas de Splunk
    print(fetch_splunk_alerts.run())
    
    if not os.path.exists("data/splunk_alerts.json"):
        print("No hay archivo de alertas.")
        return

    with open("data/splunk_alerts.json", "r") as f:
        alertas = json.load(f)

    atendidas = load_state()

    if not alertas:
        print("No se encontraron alertas en Splunk.")
        return

    for alerta in alertas:
        alert_id = alerta.get("id", "unknown")
        equipo_afectado = alerta.get("computerDnsName", "falex")
        titulo = alerta.get("title", "Sin titulo")
        desc = alerta.get("description", "Sin descripcion")
        
        # 2. Verificar si ya fue atendida
        if alert_id in atendidas:
            print(f"[-] Alerta {alert_id} ya fue atendida anteriormente.")
            continue

        print(f"\n🚨 NUEVA ALERTA: {alert_id} - {titulo}")
        print(f"   Equipo afectado: {equipo_afectado}")
        
        # 3. Visión clasifica la alerta
        tarea_vision = Task(
            description=f"""Analiza esta alerta: '{titulo} - {desc}'.
            Determina quién debe investigar:
            - Si es Ransomware, Malware, Procesos -> Responde: FRIDAY
            - Si es Equipos Zombie -> Responde: EDITH
            - Si es CVE -> Responde: KAREN
            Responde SOLO con la palabra (FRIDAY, EDITH o KAREN).""",
            expected_output="FRIDAY, EDITH o KAREN",
            agent=vision
        )
        crew_vis = Crew(agents=[vision], tasks=[tarea_vision], verbose=False)
        decision = crew_vis.kickoff().raw.strip().upper()
        
        print(f"🤖 Jarvis enruta a: {decision}")

        # 4. Ejecutar al agente correspondiente
        if "FRIDAY" in decision:
            print("🕵️ F.R.I.D.A.Y. iniciando DFIR...")
            
            print("   -> Buscando Logins (Fase 1)...")
            res_logins = run_and_analyze.run(
                playbook_filename='dfir_fase1_identificacion.kql', 
                equipo=equipo_afectado, 
                incidente=titulo
            )
            
            print("   -> Buscando Procesos (Fase 2)...")
            res_procs = run_and_analyze.run(
                playbook_filename='dfir_fase2_procesos.kql', 
                equipo=equipo_afectado, 
                incidente=titulo
            )
            
            print("\n=== RESULTADO LOGINS ===")
            print(res_logins)
            print("\n=== RESULTADO PROCESOS ===")
            print(res_procs)

        elif "EDITH" in decision:
            print("🎯 E.D.I.T.H. iniciando Threat Hunting...")
            res_hunting = run_and_analyze.run(
                playbook_filename='hunting_zombie_machines.kql', 
                equipo=equipo_afectado, 
                incidente="Auditoría de Equipos Zombie"
            )
            print("\n=== RESULTADO HUNTING ===")
            print(res_hunting)

        elif "KAREN" in decision:
            print("🛡️ K.A.R.E.N. iniciando Auditoría de Vulnerabilidades...")
            res_vuln = run_and_analyze.run(
                playbook_filename='vuln_cve_equipo.kql', 
                equipo=equipo_afectado, 
                incidente="Auditoría de Vulnerabilidades"
            )
            print("\n=== RESULTADO VULNERABILIDADES ===")
            print(res_vuln)
            
        else:
            print("⚠️ Jarvis no reconoció la decisión de Visión. No se ejecutó ningún agente.")

        # 5. Marcar como atendida y guardar estado
        atendidas.append(alert_id)
        save_state(atendidas)
        print(f"✅ Alerta {alert_id} marcada como atendida.")

if __name__ == "__main__":
    print("🚀 Iniciando Jarvis (Modo Autónomo y Continuo)...")
    procesar_alertas()