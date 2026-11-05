import os
from dotenv import load_dotenv
from tools.kql_runner import run_kql

load_dotenv()

print("🔌 Probando conexión con Azure Defender...")
# Consulta de prueba: Ver los últimos eventos de inicio de sesión
query = "DeviceLogonEvents | take 3"

# Llamamos a la función de la herramienta directamente (sin CrewAI)
# run_kql es el objeto de la herramienta, usamos .run() o ._run() dependiendo de la versión
resultado = run_kql.run(query) 

print("\n=== RESULTADO DE AZURE ===")
print(resultado)