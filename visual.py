import subprocess
from tabulate import tabulate
from colorama import init, Fore, Style

init(autoreset=True)

def ejecutar_philo(args):
    comando = ["./philo"] + args
    proceso = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        salida = proceso.stdout.readline().decode().strip()
        if not salida:
            break
        yield salida
    proceso.wait()

def colorear_accion(accion):
    if accion == "is eating":
        return f"{Fore.GREEN}{accion}{Style.RESET_ALL}"
    elif accion == "died":
        return f"{Fore.RED}{accion}{Style.RESET_ALL}"
    else:
        return accion

def main():
    numero_filosofos = int(input("Ingrese el número de filósofos y tenedores: "))
    tiempo_para_morir = int(input("Ingrese el tiempo para morir (en milisegundos): "))
    tiempo_para_comer = int(input("Ingrese el tiempo para comer (en milisegundos): "))
    tiempo_para_dormir = int(input("Ingrese el tiempo para dormir (en milisegundos): "))
    argumentos = [str(numero_filosofos), str(tiempo_para_morir), str(tiempo_para_comer), str(tiempo_para_dormir)]

    # Agregar el número opcional de veces que cada filósofo debe comer
    veces_comer = input("Ingrese el número de veces que cada filósofo debe comer (opcional): ")
    if veces_comer:
        argumentos.append(veces_comer)

    # Ejecutar el proceso y capturar la salida
    salida_ejecutable = ejecutar_philo(argumentos)

    # Crear una tabla para almacenar las acciones de todos los filósofos
    tabla = {"Timestamp": []}
    for i in range(1, numero_filosofos + 1):
        tabla[f"Filósofo {i}"] = []

    # Procesar la salida para llenar la tabla
    for linea in salida_ejecutable:
        partes = linea.split()
        if len(partes) < 3:
            print("", linea)
            continue
        tiempo = partes[0]
        tabla["Timestamp"].append(tiempo)
        for i in range(1, numero_filosofos + 1):
            accion_filosofo = ""
            for t, a in zip(partes[1::2], partes[2::2]):
                if t == str(i):
                    index = partes.index(a) + 1
                    if index < len(partes):
                        accion_filosofo = a + " " + partes[index]
                    else:
                        accion_filosofo = a
                    break
            tabla[f"Filósofo {i}"].append(colorear_accion(accion_filosofo))

    # Imprimir la tabla
    print(tabulate(tabla, headers="keys", tablefmt="grid"))

if __name__ == "__main__":
    main()
