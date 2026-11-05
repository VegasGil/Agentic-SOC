from crewai import Task
from agents import friday, edith

dfir_task = Task(
    description="""Usa la herramienta 'Leer Playbook KQL Local' para leer 'dfir_fase1_identificacion.kql'. 
    Reemplaza <NOMBRE_DEL_EQUIPO> por 'falex' y ejecútalo con la herramienta 'Ejecutar Consulta KQL en Defender'. 
    IMPORTANTE: NO inventes datos. Si la herramienta falla, reporta el error tal cual.""",
    expected_output="El usuario que inició sesión en el equipo falex.",
    agent=friday
)

hunting_task = Task(
    description="""Usa la herramienta 'Leer Playbook KQL Local' para leer 'hunting_zombie_machines.kql' y ejecútalo con 'Ejecutar Consulta KQL en Defender'. 
    Devuelve los equipos encontrados. IMPORTANTE: NO inventes datos. Si no hay datos, dilo.""",
    expected_output="Lista de equipos encontrados en el playbook.",
    agent=edith
)