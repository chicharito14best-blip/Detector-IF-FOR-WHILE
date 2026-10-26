# prueba4_menu.py
opcion_valida = False

while True:
    entrada = input("Ingrese 'salir' para terminar: ")
    
    if entrada == "salir":
        print("Terminando ejecución.")
        break
        
    if entrada == "ayuda":
        print("Mostrando menú de ayuda...")