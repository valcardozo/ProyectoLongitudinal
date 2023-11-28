import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

# Función para leer datos desde un archivo Excel
def leer_datos_excel(archivo):
    df_candidatos = pd.read_excel(archivo, sheet_name='candidatos')
    df_puestos = pd.read_excel(archivo, sheet_name='puestos')
    return df_candidatos, df_puestos

# Función para procesar los datos leídos del Excel
def procesar_datos(df_candidatos, df_puestos):
    calificaciones_candidatos = df_candidatos.iloc[:, 1:].values
    requerimientos_puestos = df_puestos.iloc[:, 1:].values
    calificaciones_puestos = np.max(requerimientos_puestos) - requerimientos_puestos
    return calificaciones_candidatos, calificaciones_puestos

def generar_poblacion(tam_poblacion, num_puestos):
    return [np.random.permutation(num_puestos) for _ in range(tam_poblacion)]

def calcular_aptitud(individuo, calificaciones_candidatos, calificaciones_puestos):
    aptitud = 0
    for puesto_idx, candidato_idx in enumerate(individuo):
        candidato = calificaciones_candidatos[candidato_idx]
        puesto = calificaciones_puestos[puesto_idx]
        aptitud += np.sum(candidato * puesto)
    return aptitud

def seleccionar_mejores(poblacion, valores_aptitud, num_seleccionados):
    indices_seleccionados = np.argsort(valores_aptitud)[-num_seleccionados:]
    return [poblacion[i] for i in indices_seleccionados]

# Función para evaluar toda la población
def evaluar_poblacion(poblacion, calificaciones_candidatos, calificaciones_puestos):
    return np.array([calcular_aptitud(individuo, calificaciones_candidatos, calificaciones_puestos) for individuo in poblacion])

def cruce(individuo1, individuo2):
    punto_cruce = random.randint(1, len(individuo1) - 1)
    # Mezcla de genes con permutaciones para asegurar la unicidad
    genes1 = set(individuo1[:punto_cruce])
    genes2 = set(individuo2[punto_cruce:])
    hijo1 = np.array(list(genes1) + list(set(individuo2) - genes1))
    hijo2 = np.array(list(genes2) + list(set(individuo1) - genes2))
    np.random.shuffle(hijo1)
    np.random.shuffle(hijo2)
    return hijo1, hijo2

def mutar(individuo, tasa_mutacion):
    for i in range(len(individuo)):
        if random.random() < tasa_mutacion:
            j = random.randint(0, len(individuo) - 1)
            individuo[i], individuo[j] = individuo[j], individuo[i]
    return individuo


def algoritmo_genetico(archivo_excel, tam_poblacion, num_puestos, generaciones, probabilidad_mutacion_inicial):
    df_candidatos, df_puestos = leer_datos_excel(archivo_excel)
    calificaciones_candidatos, calificaciones_puestos = procesar_datos(df_candidatos, df_puestos)

    poblacion = generar_poblacion(tam_poblacion, num_puestos)
    
    for generacion in range(generaciones):
        valores_aptitud = evaluar_poblacion(poblacion, calificaciones_candidatos, calificaciones_puestos)

        # Seleccionar los mejores para cruzar
        mejores = seleccionar_mejores(poblacion, valores_aptitud, tam_poblacion // 2)

        # Generar la nueva población
        nueva_poblacion = []
        while len(nueva_poblacion) < tam_poblacion:
            padre1, padre2 = random.sample(mejores, 2)
            hijo1, hijo2 = cruce(padre1, padre2)
            nueva_poblacion.append(mutar(hijo1, probabilidad_mutacion_inicial))
            if len(nueva_poblacion) < tam_poblacion:
                nueva_poblacion.append(mutar(hijo2, probabilidad_mutacion_inicial))

        poblacion = nueva_poblacion
        probabilidad_mutacion_inicial *= 0.99
        # Evaluar la última generación y seleccionar la mejor solución
    valores_aptitud = evaluar_poblacion(poblacion, calificaciones_candidatos, calificaciones_puestos)
    mejor_solucion = poblacion[np.argmax(valores_aptitud)]
    return mejor_solucion

def asignar_puestos(mejor_solucion, df_candidatos, df_puestos):
    asignaciones = []
    candidatos_asignados = set()
    for puesto_idx in mejor_solucion:
        # Encuentra un candidato no asignado aún
        candidato_idx = 0
        while candidato_idx in candidatos_asignados:
            candidato_idx = (candidato_idx + 1) % len(df_candidatos)

        candidato_id = df_candidatos.iloc[candidato_idx]['ID']
        puesto_id = df_puestos.iloc[puesto_idx]['ID']
        asignaciones.append((candidato_id, puesto_id))

        # Marcar el candidato como asignado
        candidatos_asignados.add(candidato_idx)

    return asignaciones


## Configuración y ejecución
archivo_excel = 'datosGen.xlsx'
tam_poblacion = 100
num_puestos = 50
generaciones = 100
probabilidad_mutacion_inicial = 0.1

mejor_solucion = algoritmo_genetico(archivo_excel, tam_poblacion, num_puestos, generaciones, probabilidad_mutacion_inicial)
df_candidatos, df_puestos = leer_datos_excel(archivo_excel)
asignaciones = asignar_puestos(mejor_solucion, df_candidatos, df_puestos)

# Mostrar resultados
print("Asignaciones de puestos:")
for candidato_id, puesto_id in asignaciones:
    print(f"Candidato {candidato_id} asignado al puesto {puesto_id}")

