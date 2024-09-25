import random

def crear_cuadrícula(filas, columnas, num_minas):
    cuadrícula = [[0 for _ in range(columnas)] for _ in range(filas)]
    minas = set()
    while len(minas) < num_minas:
        fila = random.randint(0, filas - 1)
        columna = random.randint(0, columnas - 1)
        if (fila, columna) not in minas:
            cuadrícula[fila][columna] = -1
            minas.add((fila, columna))
    return cuadrícula

def imprimir_cuadrícula(cuadrícula):
    for fila in cuadrícula:
        print(" ".join(str(celda) for celda in fila))

def jugar(cuadrícula):
    filas, columnas = len(cuadrícula), len(cuadrícula[0])
    while True:
        imprimir_cuadrícula(cuadrícula)
        fila = int(input("Ingrese la fila: "))
        columna = int(input("Ingrese la columna: "))
        if cuadrícula[fila][columna] == -1:
            print("¡Has detonado una mina! Game over.")
            break
        else:
            print("No hay mina en esa posición.")

cuadrícula = crear_cuadrícula(10, 10, 10)
jugar(cuadrícula)