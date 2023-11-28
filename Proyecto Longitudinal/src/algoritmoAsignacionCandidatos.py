# Datos de ejemplo
puestos = ["Project Manager", "Gerente de Marketing", "Desarrollador Full Stack", "Desarrollador Frontend", "Tester", "Recepcionista"]
candidatos_calificaciones = {
    "Valentina": ["Gerente de Marketing", "Project Manager"],
    "Jorge": ["Desarrollador Full Stack"],
    "Federico": ["Desarrollador Full Stack", "Desarrollador Frontend"],
    "José": ["Gerente de Marketing","Recepcionista"],
    "Daniel":["Tester","Recepcionista"],
    "Jessica":["Recepcionista"],
    "Maria":["Gerente de Marketing"],
    "Rodrigo":["Desarrollador Frontend","Tester"],
    "Rafael":["Project Manager"],
    "Emilia":["Tester","Desarrollador Frontend"],
    "Eugenia":["Desarrollador Frontend"]
}

asignaciones = {}
candidatos_asignados = set()

def es_candidato_unico(candidato): #Prioridad a los candidatos con un solo puesto
    return len(candidatos_calificaciones[candidato]) == 1

def tiene_otras_opciones_disponibles(candidato, puesto_actual, asignaciones):
    return any(puesto != puesto_actual and puesto not in asignaciones for puesto in candidatos_calificaciones[candidato])

for puesto in puestos:
    candidatos_para_puesto = [c for c, calificaciones in candidatos_calificaciones.items() if puesto in calificaciones and c not in candidatos_asignados]

    # Ordenar candidatos por si son únicos, si tienen otras opciones disponibles y por la posición del puesto en su lista
    candidatos_para_puesto.sort(key=lambda c: (not es_candidato_unico(c), tiene_otras_opciones_disponibles(c, puesto, asignaciones), candidatos_calificaciones[c].index(puesto)))

    # Seleccionar el candidato más adecuado
    candidato_seleccionado = candidatos_para_puesto[0] if candidatos_para_puesto else None

    # Asignar el puesto al candidato seleccionado
    if candidato_seleccionado:
        asignaciones[puesto] = candidato_seleccionado
        candidatos_asignados.add(candidato_seleccionado)

print(asignaciones)



