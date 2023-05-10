import numpy as np
import sys
import matplotlib.pyplot as plt

datos 		  = np.genfromtxt("ks_200_1", delimiter = " ")

num_elementos = int(datos[0,0])
capacidad 	  = int(datos[0,1])
beneficio	  = datos[:,0][1:]
pesos 		  = datos[:,1][1:]

Iteraciones   = 100
N_Individuos  = 50
Seleccion_ind = int(0.5*(N_Individuos))


def Crear_Matriz(Individuos, elem):
	"""
	Creacion de una matriz de poblacion para los algoritmos
	EDA. 
	"""
	Matriz = np.zeros((Individuos, elem+1))

	for i in range(Individuos):
		for j in range(elem):
				Matriz[i][j] = 1 if np.random.uniform() > 0.5 else 0
	return  Matriz

def Funcion_Objetivo(elem, Cap, Pesos, Beneficios, Vector_Solucion):
	"""
	Parámetros de la función:
	Pesos: Vector de pesos para cada uno de los objetos 

	Retorna la funciób objetivo según la condicion que se cumpla
	"""
	prod_peso_solucion = np.dot(Pesos, Vector_Solucion)

	if prod_peso_solucion <= Cap:
		return np.dot(Beneficios, Vector_Solucion)

	else:
		return Cap - prod_peso_solucion


#########################
### Inicio del ciclo ####

Poblacion_Inicial = Crear_Matriz(N_Individuos,num_elementos)

for i in range(Iteraciones):

	# Evaluacion de la población:
	for ii in range(N_Individuos):
		Poblacion_Inicial[ii, -1] = Funcion_Objetivo(num_elementos, capacidad, 
								pesos, beneficio, Poblacion_Inicial[ii,0:num_elementos])

	# Reordenamiento de la matriz,  reverse = True para problemas de maximizacion
	Poblacion_Inicial = np.array(sorted(Poblacion_Inicial, key = lambda x: x[-1], reverse = True))
	
	# Seleccion de los individuos:
	Poblacion_Seleccionada = np.zeros((Seleccion_ind, num_elementos + 1))
	Poblacion_Seleccionada = Poblacion_Inicial[0:Seleccion_ind]

	# Estimacion de media y desviación:
	Parametros = np.array([np.mean(Poblacion_Seleccionada[:,i]) for i in range(num_elementos)])
	
	# Creacion de nueva poblacion:
	Nueva_Poblacion = np.zeros((N_Individuos, num_elementos + 1))

	# Creacion de la poblacion basado en los parámetros calculados
	for jj in range(N_Individuos):
		for kk in range(num_elementos):
			Nueva_Poblacion[jj,kk] =  1 if np.random.uniform() < Parametros[kk] else 0 

	# Evaluacion de la población:
	for ll in range(N_Individuos):
		Nueva_Poblacion[ll, -1] = Funcion_Objetivo(num_elementos, capacidad, 
								pesos, beneficio, Nueva_Poblacion[ll,0:num_elementos])

	# Renombre de la nueva generacion de individuos
	Poblacion_Inicial = Nueva_Poblacion.copy()
	
# Reordenamiento de la matriz,  reverse = True para problemas de maximizacion
Poblacion_Inicial = np.array(sorted(Poblacion_Inicial, key = lambda x: x[-1], reverse = True))

print("\n##########################################################################")
print("La mejor solución encontrada para el problema de la mochila es la siguiente:")
print(Poblacion_Inicial[0, -1])
print("##########################################################################\n")