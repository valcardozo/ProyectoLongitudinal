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

def algoritmo_genetico_con_variacion(tam_poblacion, num_puestos, generaciones, probabilidad_mutacion_inicial):
    poblacion = generar_poblacion(tam_poblacion, num_puestos)
    mejores_valores = []
    valores_promedio = []
    valores_minimos = []

    probabilidad_mutacion = probabilidad_mutacion_inicial

    for generacion in range(generaciones):
        valores_aptitud = funcion_aptitud(poblacion)

        # Registrar estadísticas
        mejores_valores.append(np.max(valores_aptitud))
        valores_promedio.append(np.mean(valores_aptitud))
        valores_minimos.append(np.min(valores_aptitud))

        # Seleccionar padres y aplicar cruce
        padres = seleccionar_padres(poblacion, valores_aptitud)
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

        # Ajustar la probabilidad de mutación dinámicamente
        if generacion % 10 == 0 and generacion > 0:
            if np.mean(valores_aptitud) > np.mean(valores_promedio[-10:]):
                probabilidad_mutacion *= 1.2  # Aumentar la probabilidad de mutación
            else:
                probabilidad_mutacion *= 0.8  # Reducir la probabilidad de mutación

        probabilidad_mutacion = np.clip(probabilidad_mutacion, 0.001, 0.1)  # Asegurar que esté en un rango adecuado

    return mejores_valores, valores_promedio, valores_minimos

def algoritmo_genetico_sin_cruce(tam_poblacion, num_puestos, generaciones, probabilidad_mutacion_inicial):
    poblacion = generar_poblacion(tam_poblacion, num_puestos)
    mejores_valores = []
    valores_promedio = []
    valores_minimos = []

    probabilidad_mutacion = probabilidad_mutacion_inicial

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

        # Ajustar la probabilidad de mutación dinámicamente
        if generacion % 10 == 0 and generacion > 0:
            if np.mean(valores_aptitud) > np.mean(valores_promedio[-10:]):
                probabilidad_mutacion *= 1.2  # Aumentar la probabilidad de mutación
            else:
                probabilidad_mutacion *= 0.8  # Reducir la probabilidad de mutación

        probabilidad_mutacion = np.clip(probabilidad_mutacion, 0.001, 0.1)  # Asegurar que esté en un rango adecuado

    return mejores_valores, valores_promedio, valores_minimos

# Parámetros del algoritmo genético con variación en la probabilidad de mutación
tam_poblacion = 50
num_puestos = 50
generaciones = 50
probabilidad_mutacion_inicial = 0.01

# Ejecutar el algoritmo genético con variación en la probabilidad de mutación y con y sin cruce
mejores_valores_con_variacion, valores_promedio_con_variacion, valores_minimos_con_variacion = algoritmo_genetico_con_variacion(
    tam_poblacion, num_puestos, generaciones, probabilidad_mutacion_inicial)

mejores_valores_sin_variacion, valores_promedio_sin_variacion, valores_minimos_sin_variacion = algoritmo_genetico_sin_cruce(
    tam_poblacion, num_puestos, generaciones, probabilidad_mutacion_inicial)

# Visualizar resultados con y sin variación en la probabilidad de mutación
generaciones_rango = range(1, generaciones + 1)

plt.plot(generaciones_rango, mejores_valores_con_variacion, label='Máximo (con variación en mutación y cruce)')
plt.plot(generaciones_rango, valores_promedio_con_variacion, label='Promedio (con variación en mutación y cruce)')
plt.plot(generaciones_rango, valores_minimos_con_variacion, label='Mínimo (con variación en mutación y cruce)')

plt.plot(generaciones_rango, mejores_valores_sin_variacion, label='Máximo (sin variación en mutación y con cruce)')
plt.plot(generaciones_rango, valores_promedio_sin_variacion, label='Promedio (sin variación en mutación y con cruce)')
plt.plot(generaciones_rango, valores_minimos_sin_variacion, label='Mínimo (sin variación en mutación y con cruce)')

plt.title('Comparativo de Algoritmos Genéticos con y sin Variación en Mutación, y con y sin Cruce')
plt.xlabel('Generaciones')
plt.ylabel('Valor de Aptitud')
plt.legend()
plt.show()
