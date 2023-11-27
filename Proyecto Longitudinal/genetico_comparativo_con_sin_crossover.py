import numpy as np
import matplotlib.pyplot as plt

def generar_poblacion(tam_poblacion, num_puestos):
    return np.random.randint(num_puestos, size=(tam_poblacion, num_puestos))

def funcion_aptitud(cromosomas):
    return -np.sum(np.abs(np.diff(cromosomas, axis=1)), axis=1)

def seleccionar_padres(cromosomas, valores_aptitud):
    probabilidades = valores_aptitud / valores_aptitud.sum()
    num_padres = len(cromosomas) // 2 * 2  # Asegurar que sea un número par
    indices_seleccionados = np.random.choice(len(cromosomas), size=num_padres, p=probabilidades, replace=True)
    return cromosomas[indices_seleccionados]

def cruce(padre1, padre2):
    punto_cruce = np.random.randint(1, len(padre1))
    hijo1 = np.concatenate((padre1[:punto_cruce], padre2[punto_cruce:]))
    hijo2 = np.concatenate((padre2[:punto_cruce], padre1[punto_cruce:]))
    return hijo1, hijo2

def mutar(cromosomas, probabilidad_mutacion):
    mascara = np.random.rand(*cromosomas.shape) < probabilidad_mutacion
    cromosomas[mascara] = np.random.randint(cromosomas.shape[1], size=np.sum(mascara))
    return cromosomas

def algoritmo_genetico_con_cruce(tam_poblacion, num_puestos, generaciones, probabilidad_mutacion):
    poblacion = generar_poblacion(tam_poblacion, num_puestos)
    mejores_valores = []
    valores_promedio = []
    valores_minimos = []

    for generacion in range(generaciones):
        valores_aptitud = funcion_aptitud(poblacion)

        # Registrar estadísticas
        mejores_valores.append(np.max(valores_aptitud))
        valores_promedio.append(np.mean(valores_aptitud))
        valores_minimos.append(np.min(valores_aptitud))

        # Seleccionar padres y aplicar cruce
        padres = seleccionar_padres(poblacion, valores_aptitud)

        # Asegurar que tengamos un número par de padres para el cruce
        if len(padres) % 2 != 0:
            padres = padres[:-1]

        hijos = []
        for i in range(0, len(padres), 2):
            hijo1, hijo2 = cruce(padres[i], padres[i + 1])
            hijos.append(hijo1)
            hijos.append(hijo2)
        hijos = np.array(hijos)

        # Aplicar mutación a la descendencia
        hijos_mutados = mutar(hijos, probabilidad_mutacion)

        # Combinar padres e hijos mutados para la siguiente generación
        poblacion[:len(hijos_mutados)] = hijos_mutados

    return mejores_valores, valores_promedio, valores_minimos

def algoritmo_genetico_sin_cruce(tam_poblacion, num_puestos, generaciones, probabilidad_mutacion):
    poblacion = generar_poblacion(tam_poblacion, num_puestos)
    mejores_valores = []
    valores_promedio = []
    valores_minimos = []

    for generacion in range(generaciones):
        valores_aptitud = funcion_aptitud(poblacion)

        # Registrar estadísticas
        mejores_valores.append(np.max(valores_aptitud))
        valores_promedio.append(np.mean(valores_aptitud))
        valores_minimos.append(np.min(valores_aptitud))

        # Seleccionar padres y aplicar mutación
        padres = seleccionar_padres(poblacion, valores_aptitud)
        hijos_mutados = mutar(padres, probabilidad_mutacion)

        # Combinar padres e hijos mutados para la siguiente generación
        poblacion[:len(hijos_mutados)] = hijos_mutados

    return mejores_valores, valores_promedio, valores_minimos

# Parámetros del algoritmo genético con cruce
tam_poblacion = 50
num_puestos = 50
generaciones = 200
probabilidad_mutacion = 0.001

# Ejecutar ambos algoritmos
mejores_valores_con_cruce, valores_promedio_con_cruce, valores_minimos_con_cruce = algoritmo_genetico_con_cruce(
    tam_poblacion, num_puestos, generaciones, probabilidad_mutacion)

mejores_valores_sin_cruce, valores_promedio_sin_cruce, valores_minimos_sin_cruce = algoritmo_genetico_sin_cruce(
    tam_poblacion, num_puestos, generaciones, probabilidad_mutacion)

# Visualizar resultados
generaciones_rango = range(1, generaciones + 1)

plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.plot(generaciones_rango, mejores_valores_con_cruce, label='Máximo (con cruce)')
plt.plot(generaciones_rango, valores_promedio_con_cruce, label='Promedio (con cruce)')
plt.plot(generaciones_rango, valores_minimos_con_cruce, label='Mínimo (con cruce)')
plt.title('Con Cruce')
plt.xlabel('Generaciones')
plt.ylabel('Valor de Aptitud')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(generaciones_rango, mejores_valores_sin_cruce, label='Máximo (sin cruce)')
plt.plot(generaciones_rango, valores_promedio_sin_cruce, label='Promedio (sin cruce)')
plt.plot(generaciones_rango, valores_minimos_sin_cruce, label='Mínimo (sin cruce)')
plt.title('Sin Cruce')
plt.xlabel('Generaciones')
plt.ylabel('Valor de Aptitud')
plt.legend()

plt.tight_layout()
plt.show()