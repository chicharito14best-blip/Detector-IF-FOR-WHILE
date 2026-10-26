# prueba3_anidado.py
matriz = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

for fila in matriz:
    for numero in fila:
        if numero > 5:
            print("Valor mayor a 5 encontrado:", numero)