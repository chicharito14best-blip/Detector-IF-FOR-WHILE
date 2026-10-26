import tkinter as tk
from tkinter import filedialog, messagebox
import re

def analizar_codigo(codigo_fuente):
    # Ahora incluimos elif y else
    patron = re.compile(r'^\s*(if|elif|else|for|while)\b')
    conteo = {'if': 0, 'elif': 0, 'else': 0, 'for': 0, 'while': 0}
    detalles = []

    en_comillas_triples = False
    tipo_comilla = ""

    lineas = codigo_fuente.splitlines()
    for num_linea, linea in enumerate(lineas, start=1):
        linea_limpia = linea.strip()
        
        if not linea_limpia:
            continue

        # Detectar si entramos o salimos de comillas triples (multilínea)
        if '"""' in linea_limpia:
            if not en_comillas_triples:
                en_comillas_triples = True
                tipo_comilla = '"""'
            elif tipo_comilla == '"""':
                en_comillas_triples = False
                
        elif "'''" in linea_limpia:
            if not en_comillas_triples:
                en_comillas_triples = True
                tipo_comilla = "'''"
            elif tipo_comilla == "'''":
                en_comillas_triples = False

        coincidencia = patron.match(linea)
        if coincidencia:
            instruccion = coincidencia.group(1)
            
            # Clasificar el hallazgo
            if linea_limpia.startswith('#'):
                detalles.append(f"LÍNEA {num_linea}: COMENTARIO DETECTADO\n→ Se encontró '{instruccion}' pero está comentado.\n")
            elif en_comillas_triples or linea_limpia.startswith(('"', "'")):
                detalles.append(f"LÍNEA {num_linea}: ADVERTENCIA\n→ Se encontró dentro de las comillas la siguiente expresión: '{instruccion}'.\n")
            else:
                conteo[instruccion] += 1
                detalles.append(f"LÍNEA {num_linea}: INSTRUCCIÓN '{instruccion.upper()}'\n→ {linea_limpia}\n")

    return conteo, detalles

def cargar_archivo():
    ruta_archivo = filedialog.askopenfilename(
        title="Seleccionar código Python",
        filetypes=[("Archivos de Python", "*.py"), ("Todos los archivos", "*.*")]
    )
    
    if ruta_archivo:
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                contenido = archivo.read()
                
            texto_codigo.delete('1.0', tk.END)
            texto_codigo.insert(tk.END, contenido)
            
            texto_resultados.delete('1.0', tk.END)
            texto_explicacion.delete('1.0', tk.END)
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el archivo:\n{e}")

def ejecutar_detector():
    codigo = texto_codigo.get('1.0', tk.END).strip()
    
    if not codigo:
        messagebox.showwarning("Advertencia", "No hay código para analizar.")
        return
        
    conteo, detalles = analizar_codigo(codigo)
    
    # Renderizar Resultados
    texto_resultados.delete('1.0', tk.END)
    if detalles:
        for detalle in detalles:
            texto_resultados.insert(tk.END, detalle + "\n")
    else:
        texto_resultados.insert(tk.END, "NO SE ENCONTRARON INSTRUCCIONES DE CONTROL.\n\nEl archivo no contiene if, elif, else, for o while.")
        
    # Renderizar Explicación Teórica actualizada
    texto_explicacion.delete('1.0', tk.END)
    explicacion = "FUNCIONALIDAD PRINCIPAL:\n\n"
    
    if conteo['if'] > 0 or conteo['elif'] > 0 or conteo['else'] > 0:
        explicacion += "• Lógica de control (IF / ELIF / ELSE):\n  (IF)Evalúa una condición. Si es verdadera, ejecuta el bloque de código interno. Bifurca el flujo del programa.Evalúa condiciones lógicas. 'if' inicia la evaluación, 'elif' permite encadenar múltiples condiciones alternativas, y 'else' actúa como el caso por defecto si ninguna condición anterior se cumple.\n\n"
    if conteo['for'] > 0:
        explicacion += "• Lógica de control (FOR):\n  Itera sobre una secuencia de elementos (como listas o rangos). Ejecuta el bloque un número determinado de veces.\n\n"
    if conteo['while'] > 0:
        explicacion += "• Lógica de control (WHILE):\n  Ejecuta repetidamente un bloque de código mientras una condición booleana se mantenga verdadera.\n\n"
        
    if sum(conteo.values()) == 0:
        explicacion += "No hay estructuras ejecutables que explicar en este archivo (pueden estar comentadas o ser texto)."
        
    texto_explicacion.insert(tk.END, explicacion)
# ==========================================
# CONFIGURACIÓN VISUAL Y VENTANA
# ==========================================
COLOR_FONDO_APP = "#E5F0F9"
COLOR_BOTONES = "#2C5B9C"
COLOR_TEXTO_TITULO = "#1A2E4C"
COLOR_FONDO_EDITOR = "#121A2F"
COLOR_TEXTO_EDITOR = "#8BE9FD"
COLOR_MARCOS = "#C4DDF0"

ventana = tk.Tk()
ventana.title("Herramienta de Análisis de Código")
ventana.geometry("1200x700")
ventana.configure(bg=COLOR_FONDO_APP)

# --- PANEL SUPERIOR (Botones y Título) ---
frame_top = tk.Frame(ventana, bg=COLOR_FONDO_APP)
frame_top.pack(fill=tk.X, padx=20, pady=15)

btn_cargar = tk.Button(frame_top, text="📂 CARGAR ARCHIVO.PY", command=cargar_archivo, 
                       bg=COLOR_BOTONES, fg="white", font=("Segoe UI", 11, "bold"), 
                       relief="flat", padx=15, pady=8, cursor="hand2")
btn_cargar.pack(side=tk.LEFT, padx=(0, 10))

btn_analizar = tk.Button(frame_top, text="🔍 ANALIZAR ARCHIVO", command=ejecutar_detector, 
                         bg=COLOR_BOTONES, fg="white", font=("Segoe UI", 11, "bold"), 
                         relief="flat", padx=15, pady=8, cursor="hand2")
btn_analizar.pack(side=tk.LEFT)

lbl_titulo = tk.Label(frame_top, text="HERRAMIENTA DE ANÁLISIS DE CÓDIGO PY", 
                      bg=COLOR_FONDO_APP, fg=COLOR_TEXTO_TITULO, font=("Segoe UI", 16, "bold"))
lbl_titulo.pack(side=tk.RIGHT)

# --- PANEL CENTRAL (3 Columnas) ---
frame_central = tk.Frame(ventana, bg=COLOR_FONDO_APP)
frame_central.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

# Configurar el grid para que las 3 columnas tengan el mismo tamaño
frame_central.columnconfigure(0, weight=1, uniform="col")
frame_central.columnconfigure(1, weight=1, uniform="col")
frame_central.columnconfigure(2, weight=1, uniform="col")
frame_central.rowconfigure(0, weight=1)

# Función auxiliar para crear cada columna con su estilo
def crear_columna(parent, col, titulo, bg_contenido, fg_contenido, font_contenido):
    # Marco exterior con borde azul claro
    marco = tk.Frame(parent, bg=COLOR_MARCOS, bd=2, relief="flat")
    marco.grid(row=0, column=col, sticky="nsew", padx=10, pady=5)
    
    # Encabezado
    lbl_header = tk.Label(marco, text=titulo, bg=COLOR_MARCOS, fg=COLOR_TEXTO_TITULO, 
                          font=("Segoe UI", 12, "bold"), pady=10)
    lbl_header.pack(fill=tk.X)
    
    # Área de texto
    texto = tk.Text(marco, wrap=tk.WORD, font=font_contenido, bg=bg_contenido, fg=fg_contenido, bd=0, padx=10, pady=10)
    texto.pack(fill=tk.BOTH, expand=True, padx=2, pady=(0, 2))
    
    return texto

# Columna 1: Código Fuente
texto_codigo = crear_columna(frame_central, 0, "</> CÓDIGO FUENTE", 
                             COLOR_FONDO_EDITOR, COLOR_TEXTO_EDITOR, ("Consolas", 11))

# Columna 2: Líneas Detectadas
texto_resultados = crear_columna(frame_central, 1, "≡ LÍNEAS DETECTADAS", 
                                 "white", "#333333", ("Segoe UI", 11, "bold"))

# Columna 3: Explicación Teórica
texto_explicacion = crear_columna(frame_central, 2, "📄 EXPLICACIÓN TEÓRICA", 
                                  "white", "#333333", ("Segoe UI", 11))

if __name__ == "__main__":
    ventana.mainloop()