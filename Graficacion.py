import matplotlib.pyplot as plt 

class Graficacion:
    @staticmethod
    def grafica_txt(archivos, titulo, iteraciones):
        x = []
        y = []
        i = 0
        for archivo in archivos:
            z = []
            for linea in open(archivo, 'r'):
                lineas = [i for i in linea.split()]
                if(lineas[0] == "iteracion" or lineas[0] == "//"):
                    continue
                if int(lineas[0])%int(iteraciones/20) == 0 or int(lineas[0]) == iteraciones-1:
                    if i == 0:
                        x.append(lineas[0])
                    z.append(float(lineas[1]))
            y.append(z)
            i += 1
        plt.title(titulo)
        plt.xlabel("Iteraciones")
        plt.ylabel("Evaluacion")
        #plt.yticks(y)
        colores = ('r', 'b', 'g', 'c', 'm')
        labels = ('exponencial', 'lineal', 'generacional', 'generacional_elitismo', 'reemplazo_peores')
        for i in range(len(y)):
            plt.plot(x,y[i],marker ='o', c = colores[i], label=labels[i])
        plt.legend(loc='best')
        plt.savefig('output/Graficas/evolucion_aptitud_1.png')
        plt.show()
files = ["output/sphere/Recocido/exponencial/sphere_exponencial_23.txt", "output/sphere/Recocido/lineal/sphere_lineal_8.txt"]

Graficacion.grafica_txt(files, "Sphere", 1000)