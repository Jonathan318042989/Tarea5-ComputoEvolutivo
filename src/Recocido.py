import random
import numpy as np
from Funciones import *
from Codificacion import *
import sys
class Recocido:
    
    def __init__(self):
        self.velocidad_enfriamiento = 10
        self.funciones = {"sphere", "rastrigin", "ackley", "griewank", "rosenbrock"}
        
    def operador_vecindad(self, actual):
        """Funcion que genera un vecino aleatorio
           cambiando un bit aleatorio del original

        Args:
            actual (list(integer)): Solucion actual representado en un
                arreglo de 0 y 1
        """
        indice_aleatorio = random.randrange(len(actual))
        vecino = actual
        vecino[indice_aleatorio] = (vecino[indice_aleatorio] + 1)%2
        return vecino
    
    def enfriamiento(self, temperatura_actual, iteracion):
        """Función que simula el enfriamiento lineal

        Args:
            temperatura_actual (int): Temperatura actual
            iteracion (int): Iteracion actual del algoritmo

        Returns:
            int:  nueva temperatura resultante del enfriamiento
        """
        return temperatura_actual - self.velocidad_enfriamiento * iteracion
    
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
    
    def recocido_simulado(self, temperatura, dimension, iteraciones, funcion):
        """Implementacion de recocido simulado

        Args:
            temperatura (_type_): _description_
            dimension (_type_): _description_
            iteraciones (_type_): _description_
            funcion (_type_): _description_
        """
        valores_iniciales = self.genera_inicial(dimension, funcion)
        solucion_actual = Codificacion().codifica_vector(valores_iniciales, 22, 0, 2)
        for i in range(iteraciones):
            solucion_candidata = self.operador_vecindad(solucion_actual)
            evaluaciones = self.evalua_soluciones(solucion_actual, solucion_candidata, funcion)
            if evaluaciones[0] > evaluaciones[1]:
                solucion_actual = solucion_candidata
            else:
                if np.random.random() < (np.exp([(-(evaluaciones[1]-evaluaciones[0])/temperatura)])):
                    solucion_actual = solucion_candidata
            temperatura = self.enfriamiento(temperatura, i)
        return self.evalua_solucion_final(solucion_actual, funcion)
                    
        
if __name__ == "__main__":
    if len(sys.argv) == 5: 
        rec = Recocido()
        nombre_funcion = sys.argv[1]
        temperatura = int(sys.argv[2])
        dimensiones = int(sys.argv[3])
        iteraciones = int(sys.argv[4])
        if nombre_funcion in rec.funciones:
            print(rec.recocido_simulado(temperatura, dimensiones, iteraciones, nombre_funcion))
        else:
            print("Función no reconocida, las opciones son sphere rastrigin ackley griewank rosenbrock ")
    else:
        print("Se ejecuta como: python Recocido.py <funcion> <temperatura> <dimension> <iteraciones>")
