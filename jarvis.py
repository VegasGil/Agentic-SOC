import os
import json
from crewai import Crew, Task
from agents.vision import vision
from tools.splunk_reader import fetch_splunk_alerts

# Importamos los ejecutores de los agentes (la lógica vive en cada archivo)
from agents.friday import ejecutar_friday
from agents.edith import ejecutar_edith
from agents.karen import ejecutar_karen

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

        # 4. ENRUTAMIENTO LIMPIO (Jarvis solo llama a la función)
        if "FRIDAY" in decision:
            reporte = ejecutar_friday(equipo_afectado, titulo)
            print("\n=== RESULTADO F.R.I.D.A.Y. ===")
            print(reporte)
            
        elif "EDITH" in decision:
            reporte = ejecutar_edith(equipo_afectado)
            print("\n=== RESULTADO E.D.I.T.H. ===")
            print(reporte)
            
        elif "KAREN" in decision:
            reporte = ejecutar_karen(equipo_afectado)
            print("\n=== RESULTADO K.A.R.E.N. (RBVM) ===")
            print(reporte)
            
        else:
            print("⚠️ Jarvis no reconoció la decisión de Visión.")

        # 5. Marcar como atendida y guardar estado
        atendidas.append(alert_id)
        save_state(atendidas)
        print(f"✅ Alerta {alert_id} marcada como atendida.")

if __name__ == "__main__":
    print("🚀 Iniciando Jarvis (Modo Refactorizado con Agentes Autónomos)...")
    procesar_alertas()