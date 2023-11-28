# Algoritmo Genético y Método Húngaro para la Asignación Óptima de Candidatos a Puestos

Este repositorio combina dos enfoques para la asignación óptima de candidatos a puestos de trabajo: un Algoritmo Genético y el Método Húngaro. Este repositorio presenta soluciones avanzadas y eficientes para el desafío de asignar de manera óptima candidatos a diferentes puestos en una organización, utilizando principios de genética y optimización matemática.

## Algoritmo Genético para Asignación de Candidatos

### ¿Qué hace este algoritmo?

El Algoritmo Genético imita los procesos evolutivos naturales como la selección, el cruce genético y la mutación. Su objetivo es asignar eficientemente candidatos a una serie de puestos, maximizando la adecuación y competencias de cada candidato para el puesto asignado.

#### Características Clave:
- **Generación de Población Inicial**: Crea soluciones candidatas, cada una representando una posible asignación de candidatos a puestos.
- **Evaluación de Aptitud**: Calcula la "aptitud" de cada solución, basándose en cuán bien los candidatos asignados se ajustan a los puestos.
- **Selección, Cruce y Mutación**: Procesos inspirados en la biología para mejorar y diversificar las soluciones.
- **Iteración a través de Generaciones**: Mejora continuamente la calidad de las soluciones a lo largo de múltiples generaciones.

## Método Húngaro para Asignación Óptima

### ¿Qué hace este algoritmo?

El Método Húngaro es una técnica de optimización que asigna de manera eficiente recursos a tareas. En este contexto, asigna candidatos a puestos de trabajo basándose en una matriz de puntuaciones o calificaciones.

#### Características Principales:
- **Carga y Transformación de Datos**: Utiliza datos de un archivo Excel para crear una matriz de costos.
- **Optimización y Asignación**: Aplica el Método Húngaro para encontrar la asignación de menor costo, es decir, la mejor coincidencia entre candidatos y puestos.
- **Resultados y Validación**: Genera una lista detallada de las asignaciones y valida la precisión del proceso.

## Aplicaciones

Ambos algoritmos son útiles en entornos donde la asignación de recursos humanos es crítica para el rendimiento y la eficiencia organizacional. Proporcionan herramientas automatizadas y optimizadas para la asignación de personal, asegurando el uso más efectivo de los recursos humanos.

## Implementación

El código proporcionado en este repositorio está escrito en Python, utilizando bibliotecas como NumPy, Pandas, y Scipy. Los algoritmos son altamente personalizables y pueden ser adaptados para ajustarse a diferentes requisitos y criterios de aptitud específicos.

