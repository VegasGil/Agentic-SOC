import os
import json
import requests
import urllib3
from crewai.tools import tool
from dotenv import load_dotenv

load_dotenv()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

@tool("Obtener Alertas Nuevas de Splunk")
def fetch_splunk_alerts() -> str:
    """Conecta a Splunk, descarga las últimas alertas de Defender y las guarda en data/splunk_alerts.json."""
    print("   -> [Splunk] Buscando alertas en Oracle...")
    
    splunk_host = os.getenv("SPLUNK_HOST")
    splunk_port = os.getenv("SPLUNK_REST_PORT", "8089")
    splunk_user = os.getenv("SPLUNK_USER", "admin")
    splunk_pass = os.getenv("SPLUNK_PASS")

    if not splunk_host or not splunk_pass:
        return "Error: Faltan credenciales de Splunk en el .env"

    if not splunk_host.startswith("http"):
        splunk_host = f"https://{splunk_host}"

    url = f"{splunk_host}:{splunk_port}/services/search/jobs/export"
    data = {
        "search": 'search index=* sourcetype="ms:defender:atp:alerts" | head 10',
        "output_mode": "json",
        "earliest_time": "-7d",
        "latest_time": "now"
    }

    try:
        response = requests.post(url, data=data, auth=(splunk_user, splunk_pass), verify=False, timeout=30)
        response.raise_for_status()

        alerts = []
        for line in response.text.splitlines():
            if not line.strip(): continue
            obj = json.loads(line)
            if "result" in obj:
                raw_json = obj["result"].get("_raw", "{}")
                try:
                    parsed_alert = json.loads(raw_json)
                    alerts.append(parsed_alert)
                except:
                    pass
        
        # Guardamos todas las alertas en local
        os.makedirs("data", exist_ok=True)
        with open("data/splunk_alerts.json", "w", encoding="utf-8") as f:
            json.dump(alerts, f, indent=4)

        return f"Se encontraron {len(alerts)} alertas. Guardadas en data/splunk_alerts.json."
    except Exception as e:
        return f"Error conectando a Splunk: {e}"