# prueba5_falsos_positivos.py
informacion = "El ciclo for es muy útil"
if_condition = True
texto = "while esto sea verdad"

if if_condition:
    for i in range(3):
        print(informacion, texto)