import subprocess

#funciones
arg1 = {"sphere", "ackley", "griewank", "rastrigin", "rosenbrock"}
#temperatura
arg2 = "1000"
#dimension
arg3 = "10"
#iteraciones
arg4 = "1000"
#tipo de enfriamiento
arg5 = {"lineal", "exponencial"}

for i in range(30):
    for f in arg1:
        for t in arg5:
            subprocess.run(['python', 'src/Recocido.py', f, arg2, arg3, arg4, t, str(i+1)])