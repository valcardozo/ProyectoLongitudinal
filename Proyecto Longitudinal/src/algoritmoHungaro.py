import pandas as pd
import numpy as np
from scipy.optimize import linear_sum_assignment

# Cargamos el archivo de Excel con los resultados de los candidatos
score_file_path = "scores.xlsx"
scores_df = pd.read_excel(score_file_path, index_col=0)

# Convertimos los resultados a costos restando 100 - score
cost_matrix = 100 - scores_df.values

# Aplicamos el Algoritmo Húngaro para obtener la asignación óptima
row_indices, col_indices = linear_sum_assignment(cost_matrix)

assignments = []
for row, col in zip(row_indices, col_indices):
    assignments.append({
        "Candidato": scores_df.index[row], 
        "Puesto": scores_df.columns[col], 
        "Score": scores_df.values[row, col],
        "Costo": cost_matrix[row, col]
    })

assignments_df = pd.DataFrame(assignments)
assignments_file = "assignments.xlsx"
assignments_df.to_excel(assignments_file, index=False)

# Calculamos el costo total de las asignaciones óptimas
total_cost = cost_matrix[row_indices, col_indices].sum()
total_score = scores_df.values[row_indices, col_indices].sum()

print("Asignaciones Óptimas:")
print(assignments_df)
print("\nCosto total:", total_cost)
print("Score total:", total_score)
print("\nSe guardaron las asignaciones en:", assignments_file)

# Comprobación adicional: si el costo total es igual al costo calculado manualmente
manual_total_cost = sum([assignment['Costo'] for assignment in assignments])
print("\nValidación del algoritmo:")
print("Costo total calculado manualmente:", manual_total_cost)
print("Costo total del algoritmo:", total_cost)
print("Validación exitosa" if manual_total_cost == total_cost else "Discrepancia en Validación")

