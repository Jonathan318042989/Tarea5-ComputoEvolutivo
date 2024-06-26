import random
import numpy as np
from Funciones import *
from Codificacion import *
import sys

class Recocido:
    
    def __init__(self):
        self.funciones = {"sphere", "rastrigin", "ackley", "griewank", "rosenbrock"}
        self.semilla = 0
        self.dominio = ()
        
    def operador_vecindad(self, actual):
        """Funcion que genera un vecino aleatorio
           cambiando un bit aleatorio del original

        Args:
            actual (list(integer)): Solucion actual representado en un
                arreglo de 0 y 1
        """
        indices_aleatorios = np.random.randint(len(actual), size=5)
        vecino = actual.copy()
        for i in range(len(indices_aleatorios)):
            vecino[indices_aleatorios[i]] = (vecino[indices_aleatorios[i]] + 1) % 2
        return vecino
    
    def enfriamiento_lineal(self, temperatura_actual, iteracion, velocidad_enfriamiento):
        """Función que simula el enfriamiento lineal

        Args:
            temperatura_actual (float): Temperatura actual
            iteracion (int): Iteracion actual del algoritmo
            velocidad_enfriamiento (float): Velocidad de enfriamiento

        Returns:
            float: Nueva temperatura resultante del enfriamiento
        """
        return temperatura_actual - velocidad_enfriamiento * iteracion
    
    def enfriamiento_exponencial(self, temperatura_actual, iteracion, factor_enfriamiento):
        """Función que simula el enfriamiento exponencial

        Args:
            temperatura_actual (float): Temperatura actual
            iteracion (int): Iteracion actual del algoritmo
            factor_enfriamiento (float): Factor de enfriamiento

        Returns:
            float: Nueva temperatura resultante del enfriamiento
        """
        return temperatura_actual * factor_enfriamiento
    
    def genera_inicial(self, dimension, funcion):
        """Genera los valores iniciales para el recocido simulado

        Args:
            dimension (int): Tamaño de la entrada para la funcion a evaluar
            funcion (str): Funcion a evaluar

        Returns:
            (list(float)): Lista con los valores para evaluar la funcion dada
        """
        if funcion == "sphere" or funcion == "rastrigin":
            return np.random.uniform(dominio_sphere_rastrigin[0], dominio_sphere_rastrigin[1], [dimension])
        elif funcion == "ackley":
            return np.random.uniform(dominio_ackley[0], dominio_ackley[1], [dimension])    
        elif funcion == "griewank":
            return np.random.uniform(dominio_griewank[0], dominio_griewank[1], [dimension])    
        elif funcion == "rosenbrock":
            return np.random.uniform(dominio_rosenbrock[0], dominio_rosenbrock[1], [dimension])    
            
    def evalua_soluciones(self, solucion_actual, solucion_candidata, funcion):
        """Evalua la funcion decodificando 

        Args:
            solucion_actual (list(int)): Codificacion de los valores actuales
            solucion_candidata (list(int)): Codificacion de los valores candidatos
            funcion (str): Funcion a evaluar

        Returns:
            (tuple): resultados de las evaluaciones
        """
        decodificacion_actual = Codificacion().decodifica_vector(solucion_actual, 22, 0, 2)
        decodificacion_candidata = Codificacion().decodifica_vector(solucion_candidata, 22, 0, 2)
        
        if funcion == "sphere":
            return Funciones().sphere(decodificacion_actual), Funciones().sphere(decodificacion_candidata)
        elif funcion == "rastrigin":
            return Funciones.rastrigin(decodificacion_actual), Funciones.rastrigin(decodificacion_candidata)            
        elif funcion == "ackley":
            return Funciones.ackley(decodificacion_actual), Funciones.ackley(decodificacion_candidata)
        elif funcion == "griewank":
            return Funciones.griewank(decodificacion_actual), Funciones.griewank(decodificacion_candidata)
        elif funcion == "rosenbrock":
            return Funciones.rosenbrock(decodificacion_actual), Funciones.rosenbrock(decodificacion_candidata)
            
    def evalua_solucion_final(self, solucion, funcion):
        """Evalua la solución que queda al final del recocido simulado

        Args:
            solucion (list(list(int))): Lista que representa a la solución actual
            funcion (str): Función que se evaluará

        Returns:
            float: Float con la evaluación de la solución final
        """
        decodificacion = Codificacion().decodifica_vector(solucion, 22, 0, 2)
        if funcion == "sphere":
            return Funciones().sphere(decodificacion)
        elif funcion == "rastrigin":
            return Funciones.rastrigin(decodificacion)
        elif funcion == "ackley":
            return Funciones.ackley(decodificacion)
        elif funcion == "griewank":
            return Funciones.griewank(decodificacion)
        elif funcion == "rosenbrock":
            return Funciones.rosenbrock(decodificacion)
    
    def recocido_simulado(self, temperatura, dimension, iteraciones, funcion, enfriamiento="lineal", velocidad_enfriamiento=1.0, factor_enfriamiento=0.95, ejecucion=31):
        """Implementacion de recocido simulado

        Args:
            temperatura (float): Temperatura inicial
            dimension (int): Dimension del espacio de búsqueda
            iteraciones (int): Número de iteraciones
            funcion (str): Función de optimización
            enfriamiento (str): Tipo de esquema de enfriamiento (lineal o exponencial)
            velocidad_enfriamiento (float): Velocidad de enfriamiento para el enfriamiento lineal
            factor_enfriamiento (float): Factor de enfriamiento para el enfriamiento exponencial

        Returns:
            float: Mejor valor encontrado por el algoritmo
        """
        archivo = "output/" + funcion + "/Recocido" + "/" + enfriamiento + "/" + funcion + "_" + enfriamiento + "_" + str(ejecucion) + ".txt"
        file = open(archivo, 'w')
        file.write("iteracion  mejor_solucion    distancia_euclidiana                 distancia_hamming\n")
        valores_iniciales = self.genera_inicial(dimension, funcion)
        solucion_actual = Codificacion().codifica_vector(valores_iniciales, 22, self.dominio[0], self.dominio[1])
        for i in range(iteraciones):
            solucion_candidata = self.operador_vecindad(solucion_actual)
            evaluaciones = self.evalua_soluciones(solucion_actual, solucion_candidata, funcion)
            sol_actual = evaluaciones[0]
            if evaluaciones[0] > evaluaciones[1]:
                solucion_actual = solucion_candidata
                sol_actual = evaluaciones[1]
            else:
                if np.random.random() < np.exp(-((evaluaciones[1] - evaluaciones[0]) / temperatura)):
                    solucion_actual = solucion_candidata
                    
            if enfriamiento == "lineal":
                temperatura = self.enfriamiento_lineal(temperatura, i, velocidad_enfriamiento)
            elif enfriamiento == "exponencial":
                temperatura = self.enfriamiento_exponencial(temperatura, i, factor_enfriamiento)
            distancia_euclideana = np.linalg.norm(np.array(solucion_candidata) - np.array(solucion_actual))
            distancia_hamming = np.count_nonzero(np.array(solucion_candidata)!=np.array(solucion_actual))
            file.write(str(i) + "         " + str(sol_actual) + "        " + str(distancia_euclideana) + "                                 " + str(distancia_hamming) + "\n")
        file.write("// Funcion: " + funcion + " Enfriamiento: " + enfriamiento + " Semilla: " + str(self.semilla))
        file.close()
        return self.evalua_solucion_final(solucion_actual, funcion)
                    
if __name__ == "__main__":
    if len(sys.argv) >= 6: 
        rec = Recocido()
        nombre_funcion = sys.argv[1]
        temperatura = float(sys.argv[2])
        dimensiones = int(sys.argv[3])
        iteraciones = int(sys.argv[4])
        tipo_enfriamiento = sys.argv[5]
        #ejecucion = sys.argv[6] #Parametro usado para nombrar al archivo
        rec.semilla = np.random.randint(1, math.pow(2, 31))
        if len(sys.argv) == 7:
            rec.semilla = int(sys.argv[6])
        random.seed(rec.semilla)
        np.random.seed(rec.semilla)
        
        if nombre_funcion in rec.funciones:
            rec.dominio = Funciones().dominios(nombre_funcion)
            print(rec.recocido_simulado(temperatura, dimensiones, iteraciones, nombre_funcion, enfriamiento=tipo_enfriamiento))
            print(f"La semila es {rec.semilla}")
        else:
            print("Función no reconocida, las opciones son sphere rastrigin ackley griewank rosenbrock ")
    else:
        print("Se ejecuta como: python Recocido.py <funcion> <temperatura> <dimension> <iteraciones> <tipo_enfriamiento>")
