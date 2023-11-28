import numpy as np
import matplotlib.pyplot as plt

def generar_poblacion(tam_poblacion, num_puestos):
    return np.random.randint(num_puestos, size=(tam_poblacion, num_puestos))

def funcion_aptitud(cromosomas):
    return -np.sum(np.abs(np.diff(cromosomas, axis=1)), axis=1)

def seleccionar_padres(cromosomas, valores_aptitud):
    probabilidades = valores_aptitud / valores_aptitud.sum()
    indices_seleccionados = np.random.choice(len(cromosomas), size=len(cromosomas) // 2, p=probabilidades, replace=True)
    return cromosomas[indices_seleccionados]

def mutar(cromosomas, probabilidad_mutacion):
    mascara = np.random.rand(*cromosomas.shape) < probabilidad_mutacion
    cromosomas[mascara] = np.random.randint(cromosomas.shape[1], size=np.sum(mascara))
    return cromosomas

def algoritmo_genetico_sin_cruce_optimizado(tam_poblacion, num_puestos, generaciones, probabilidad_mutacion):
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

        # Seleccionar padres y mutar
        padres = seleccionar_padres(poblacion, valores_aptitud)
        hijos_mutados = mutar(padres, probabilidad_mutacion)

        # Reemplazar la población con los hijos mutados
        poblacion[:len(hijos_mutados)] = hijos_mutados

    return mejores_valores, valores_promedio, valores_minimos

# Parámetros del algoritmo genético sin cruce optimizado
tam_poblacion = 50
num_puestos = 50
generaciones = 50
probabilidad_mutacion = 0.01

# Ejecutar el algoritmo genético sin cruce optimizado
mejores_valores, valores_promedio, valores_minimos = algoritmo_genetico_sin_cruce_optimizado(
    tam_poblacion, num_puestos, generaciones, probabilidad_mutacion)

# Visualizar resultados
generaciones_rango = range(1, generaciones + 1)

plt.plot(generaciones_rango, mejores_valores, label='Máximo (sin cruce)')
plt.plot(generaciones_rango, valores_promedio, label='Promedio (sin cruce)')
plt.plot(generaciones_rango, valores_minimos, label='Mínimo (sin cruce)')

plt.title('Evolución de la Función Objetivo en la Población (Sin Cruce) - Optimizado')
plt.xlabel('Generaciones')
plt.ylabel('Valor de Aptitud')
plt.legend()
plt.show()
