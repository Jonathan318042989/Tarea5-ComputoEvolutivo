import sys
import random
import numpy as np
import matplotlib.pyplot as plt
from Funciones import Funciones

class AlgoritmoGenetico:
    
    def __init__(self, funcion_objetivo, dominio, tamano_poblacion=100, num_generaciones=1000, prob_mutacion=0.1, num_puntos_cruza=2, elitismo=False, reemplazo="generacional", semilla = 0, numero_ejecucion = 31, nombre_funcion=""):
        self.funcion_objetivo = funcion_objetivo
        self.dominio = dominio
        self.tamano_poblacion = tamano_poblacion
        self.num_generaciones = num_generaciones
        self.prob_mutacion = prob_mutacion
        self.num_puntos_cruza = num_puntos_cruza
        self.elitismo = elitismo
        self.reemplazo = reemplazo
        self.semilla = semilla
        self.nombre = nombre_funcion
        self.numero_ejecucion = numero_ejecucion

    def inicializar_poblacion(self):
        poblacion = []
        for _ in range(self.tamano_poblacion):
            solucion = [random.uniform(self.dominio[0], self.dominio[1]) for _ in range(len(self.dominio))]
            poblacion.append(solucion)
        return poblacion

    def evaluar_poblacion(self, poblacion):
        evaluaciones = []
        for individuo in poblacion:
            evaluacion = self.funcion_objetivo(individuo)
            evaluaciones.append((individuo, evaluacion))
        return evaluaciones

    def seleccionar_padres(self, evaluaciones):
        total_fitness = sum(1 / evaluacion[1] for evaluacion in evaluaciones)
        padres_seleccionados = []
        while len(padres_seleccionados) < 2:
            punto = random.uniform(0, total_fitness)
            acumulado = 0
            for individuo, evaluacion in evaluaciones:
                acumulado += 1 / evaluacion
                if acumulado > punto:
                    padres_seleccionados.append(individuo)
                    break
        return padres_seleccionados

    def cruzar_padres(self, padre1, padre2):
        puntos_cruza = sorted(random.sample(range(len(padre1)), self.num_puntos_cruza))
        hijo1 = []
        hijo2 = []
        for i in range(len(padre1)):
            if i in puntos_cruza:
                hijo1.append(padre2[i])
                hijo2.append(padre1[i])
            else:
                hijo1.append(padre1[i])
                hijo2.append(padre2[i])
        return hijo1, hijo2

    def mutar(self, individuo):
        for i in range(len(individuo)):
            if random.random() < self.prob_mutacion:
                individuo[i] = random.uniform(self.dominio[0], self.dominio[1])
        return individuo

    def reemplazar_generacional(self, poblacion, evaluaciones):
        nueva_generacion = []
        while len(nueva_generacion) < self.tamano_poblacion:
            padres = self.seleccionar_padres(evaluaciones)
            hijos = self.cruzar_padres(padres[0], padres[1])
            hijo1_mutado = self.mutar(hijos[0])
            hijo2_mutado = self.mutar(hijos[1])
            nueva_generacion.extend([hijo1_mutado, hijo2_mutado])
        return nueva_generacion

    def reemplazar_generacional_elitismo(self, poblacion, evaluaciones):
        nueva_generacion = []
        mejor_solucion = min(evaluaciones, key=lambda x: x[1])[0]
        nueva_generacion.append(mejor_solucion)
        while len(nueva_generacion) < self.tamano_poblacion:
            padres = self.seleccionar_padres(evaluaciones)
            hijos = self.cruzar_padres(padres[0], padres[1])
            hijo1_mutado = self.mutar(hijos[0])
            hijo2_mutado = self.mutar(hijos[1])
            nueva_generacion.extend([hijo1_mutado, hijo2_mutado])
        return nueva_generacion

    def reemplazar_peores(self, poblacion, evaluaciones):
        nueva_generacion = []
        poblacion_ordenada = sorted(evaluaciones, key=lambda x: x[1])
        mitad = len(poblacion_ordenada) // 2
        mejor_mitad = poblacion_ordenada[:mitad]
        for individuo, _ in mejor_mitad:
            nueva_generacion.append(individuo)
        while len(nueva_generacion) < self.tamano_poblacion:
            padres = self.seleccionar_padres(evaluaciones)
            hijos = self.cruzar_padres(padres[0], padres[1])
            hijo1_mutado = self.mutar(hijos[0])
            hijo2_mutado = self.mutar(hijos[1])
            nueva_generacion.extend([hijo1_mutado, hijo2_mutado])
        return nueva_generacion

    def encuentra_peor(self, evaluaciones, peor):
        peor_candidato = max(evaluaciones, key=lambda x: x[1])[1]
        if peor_candidato > peor:
            return peor_candidato
        else:
            return peor 

    def calcula_promedio(self, evaluaciones, promedio_actual):
        suma = 0
        for i in range(len(evaluaciones)):
            suma += evaluaciones[i][1]
        suma /= len(evaluaciones)    
        promedio_actual += suma
        return promedio_actual/2

   # def distancia_euclidiana(self, poblacion):
        

    def ejecutar(self):
        poblacion = self.inicializar_poblacion()
        #print(poblacion[0])
        mejor_aptitud_por_generacion = []
        archivo = "output/" + self.nombre + "/Genetico" + "/" + self.reemplazo + "/" + self.nombre + "_" + self.reemplazo + "_" + str(self.numero_ejecucion) + ".txt"
        file = open(archivo, 'w')
        file.write("iteracion  mejor_solucion       peor_solucion         promedio               distancia_euclidiana                 distancia_hamming\n")
        peor = 0
        promedio = 0
        mejor = float("inf")
        for _ in range(self.num_generaciones):
            evaluaciones = self.evaluar_poblacion(poblacion)
            mejor_aptitud = min(evaluaciones, key=lambda x: x[1])[1]
            mejor_aptitud_por_generacion.append(mejor_aptitud)
            if self.reemplazo == "generacional":
                poblacion = self.reemplazar_generacional(poblacion, evaluaciones)
            elif self.reemplazo == "generacional_elitismo":
                poblacion = self.reemplazar_generacional_elitismo(poblacion, evaluaciones)
            elif self.reemplazo == "peores":
                poblacion = self.reemplazar_peores(poblacion, evaluaciones)
            if mejor > mejor_aptitud:
                mejor = mejor_aptitud
            peor = self.encuentra_peor(evaluaciones, peor)
            promedio += self.calcula_promedio(evaluaciones, promedio)
            mejor_aptitud_por_generacion.append(mejor_aptitud)
        file.close()
        return poblacion, mejor_aptitud_por_generacion, mejor, peor, promedio

def graficar_evolucion(funcion_objetivo, dominio, titulo, reemplazo):
    ag = AlgoritmoGenetico(funcion_objetivo, dominio, reemplazo=reemplazo)
    _, mejor_aptitud_por_generacion = ag.ejecutar()
    plt.plot(mejor_aptitud_por_generacion)
    plt.title(titulo)
    plt.xlabel("Generación")
    plt.ylabel("Mejor Aptitud")
    plt.show()
    
def ejecucion(funcion_seleccionada, funcion_objetivo, dominio, reemplazo):
    ag = AlgoritmoGenetico(funcion_objetivo, dominio, reemplazo=reemplazo, nombre_funcion = funcion_seleccionada)
    poblacion, mejor_aptitud_por_generacion, mejor, peor, promedio = ag.ejecutar()
    print(ag.semilla)
    print(mejor)

if __name__ == "__main__":
    dominios = {
        "sphere": (-5.12, 5.12),
        "rastrigin": (-5.12, 5.12),
        "ackley": (-30, 30),
        "griewank": (-600, 600),
        "rosenbrock": (-2.048, 2.048)
    }

    funciones = {
        "sphere": Funciones.sphere,
        "rastrigin": Funciones.rastrigin,
        "ackley": Funciones.ackley,
        "griewank": Funciones.griewank,
        "rosenbrock": Funciones.rosenbrock
    }

    reemplazos = ["generacional", "generacional_elitismo", "peores"]

    if len(sys.argv) != 3:
        print("Uso: python Optimizacion_Cont.py <funcion> <reemplazo>")
        sys.exit(1)

    funcion_seleccionada = sys.argv[1]
    reemplazo_seleccionado = sys.argv[2]

    if funcion_seleccionada not in funciones:
        print("La función seleccionada no está disponible.")
        sys.exit(1)

    if reemplazo_seleccionado not in reemplazos:
        print("El esquema de reemplazo seleccionado no está disponible.")
        sys.exit(1)

    funcion_objetivo = funciones[funcion_seleccionada]
    dominio = dominios[funcion_seleccionada]
    titulo = f"Evolución de Aptitud para {funcion_seleccionada} con {reemplazo_seleccionado.capitalize()}"

    ejecucion(funcion_seleccionada, funcion_objetivo, dominio, reemplazo_seleccionado)
