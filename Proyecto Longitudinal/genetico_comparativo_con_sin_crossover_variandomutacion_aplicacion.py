import numpy as np
import matplotlib.pyplot as plt


def generar_poblacion(tam_poblacion, num_puestos):
    return np.random.randint(2, size=(tam_poblacion, num_puestos))

def seleccionar_padres(poblacion, valores_aptitud):
    padres_indices = np.random.choice(len(poblacion), size=len(poblacion)//2, p=valores_aptitud/np.sum(valores_aptitud), replace=False)
    return poblacion[padres_indices]

def cruce(padre1, padre2):
    punto_cruce = np.random.randint(1, len(padre1))
    hijo1 = np.concatenate((padre1[:punto_cruce], padre2[punto_cruce:]))
    hijo2 = np.concatenate((padre2[:punto_cruce], padre1[punto_cruce:]))
    return hijo1, hijo2

def mutar(poblacion, probabilidad_mutacion):
    mascara_mutacion = np.random.rand(*poblacion.shape) < probabilidad_mutacion
    poblacion_mutada = poblacion ^ mascara_mutacion
    return poblacion_mutada

def funcion_aptitud(poblacion, candidatos, calificaciones):
    num_puestos = poblacion.shape[1]
    num_candidatos = len(candidatos)

    # Ajustar las calificaciones para que coincidan con la población
    calificaciones_ajustadas = np.repeat(calificaciones[np.newaxis, :, :], len(poblacion), axis=0)

    # Ajustar la población para que coincida con las calificaciones
    poblacion_ajustada = np.repeat(poblacion[:, np.newaxis, :], num_candidatos, axis=1)

    # Calcular la aptitud
    aptitud = np.sum(poblacion_ajustada * calificaciones_ajustadas, axis=(1, 2))

    return aptitud


def asignar_puestos(mejor_solucion, candidatos, calificaciones):
    if len(mejor_solucion.shape) == 1:
        num_candidatos, num_puestos = len(mejor_solucion), len(mejor_solucion)
    else:
        num_candidatos, num_puestos = mejor_solucion.shape
    
    asignaciones = np.zeros(num_puestos, dtype=int)

    for i in range(num_puestos):
        if len(mejor_solucion.shape) == 1:
            opciones_disponibles = [c for c in range(num_candidatos) if mejor_solucion[c] == 0]
        else:
            opciones_disponibles = [c for c in range(num_candidatos) if mejor_solucion[c, i] == 0]

        if opciones_disponibles:
            opciones_ordenadas = sorted(opciones_disponibles, key=lambda x: calificaciones[x, i], reverse=True)
            puesto_asignado = opciones_ordenadas[0]
            asignaciones[i] = puesto_asignado
            if len(mejor_solucion.shape) == 1:
                mejor_solucion[puesto_asignado] = 1
            else:
                mejor_solucion[puesto_asignado, i] = 1  # Marcar el puesto como asignado para el candidato

    return asignaciones

def algoritmo_genetico(tam_poblacion, num_puestos, candidatos, calificaciones, generaciones, probabilidad_mutacion_inicial):
    poblacion = generar_poblacion(tam_poblacion, num_puestos)
    mejores_valores = []
    valores_promedio = []
    valores_minimos = []
    
    mejor_solucion = None  # Agregamos esta línea para asegurarnos de que 'mejor_solucion' esté definido

    for generacion in range(1, generaciones + 1):
        valores_aptitud = funcion_aptitud(poblacion, candidatos, calificaciones)

        mejores_valores.append(np.max(valores_aptitud))
        valores_promedio.append(np.mean(valores_aptitud))
        valores_minimos.append(np.min(valores_aptitud))

        padres = seleccionar_padres(poblacion, valores_aptitud)
        hijos = []

        for i in range(0, len(padres), 2):
            hijo1, hijo2 = cruce(padres[i], padres[i + 1])
            hijos.extend([hijo1, hijo2])

        probabilidad_mutacion_actual = probabilidad_mutacion_inicial * (1 - generacion / generaciones)
        hijos_mutados = mutar(np.array(hijos), probabilidad_mutacion_actual)
        poblacion[:len(hijos_mutados)] = hijos_mutados

        mejor_solucion = poblacion[np.argmax(valores_aptitud)]

    asignaciones = asignar_puestos(mejor_solucion, candidatos, calificaciones)

    return mejores_valores, valores_promedio, valores_minimos, asignaciones

    print(f"Generación {generacion}: Mejor valor {mejores_valores[-1]}, Asignaciones {asignaciones}")


# Configuración de prueba
tam_poblacion = 2500  # Ajustar el tamaño de la población
num_puestos = 50      # Ajustar la cantidad de puestos
candidatos = [
    {'lista': list(range(50)), 'otras_opciones': []} for _ in range(50)  # 50 candidatos con listas de 50 opciones
]
calificaciones = np.random.rand(len(candidatos), num_puestos)
generaciones = 50
probabilidad_mutacion_inicial = 0.01

# Ejecutar el algoritmo genético
mejores_valores, valores_promedio, valores_minimos, asignaciones = algoritmo_genetico(
    tam_poblacion, num_puestos, candidatos, calificaciones, generaciones, probabilidad_mutacion_inicial
)

# Mostrar resultados
print("Mejores valores:", mejores_valores)
print("Valores promedio:", valores_promedio)
print("Valores mínimos:", valores_minimos)
print("Asignaciones:", asignaciones)

# Visualizar resultados gráficamente
generaciones_range = range(1, generaciones + 1)

plt.figure(figsize=(10, 6))

plt.subplot(2, 1, 1)
plt.plot(generaciones_range, mejores_valores, label='Mejores valores')
plt.plot(generaciones_range, valores_promedio, label='Valores promedio')
plt.plot(generaciones_range, valores_minimos, label='Valores mínimos')
plt.title('Evolución de los valores de aptitud')
plt.xlabel('Generación')
plt.ylabel('Valor de aptitud')
plt.legend()

plt.subplot(2, 1, 2)
plt.bar(range(num_puestos), asignaciones, color='blue', alpha=0.7)
plt.title('Asignación de puestos en la última generación')
plt.xlabel('Puesto')
plt.ylabel('Candidato asignado')

plt.tight_layout()
plt.show()

plt.show()


