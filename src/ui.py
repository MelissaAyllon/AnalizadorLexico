import tkinter as tk
from lexer.lexer import lexer_errors
from lexer.lexer import get_tokens  # Asegúrate de que la función get_tokens esté definida en lexer.py
from lexer.parser import parser  # Asegúrate de que tu parser esté definido en parser.py
from lexer.parser import parser_errors
from lexer.parser import semantic_errors  # Asegúrate de que tu parser tenga una lista de errores semánticos

# Crear la ventana principal
root = tk.Tk()
root.title("DART EDITOR")

# Configurar el tamaño de la ventana
root.geometry("800x600")
root.config(bg="#1c1c1c")

# Título
title_label = tk.Label(root, text="DART EDITOR", font=("Helvetica", 24, "bold"), fg="white", bg="#1c1c1c")
title_label.pack(pady=20)

# Frame para los Tokens
frame_tokens = tk.Frame(root, bg="#1c1c1c")
frame_tokens.pack(side=tk.LEFT, padx=20, fill="y", expand=True)

# Título Tokens
tokens_title = tk.Label(frame_tokens, text="Tokens", font=("Helvetica", 14, "bold"), fg="white", bg="#1c1c1c")
tokens_title.pack(pady=10)

# Caja de texto para Tokens
tokens_text = tk.Text(frame_tokens, height=10, width=30, bg="#2d2d2d", fg="white", font=("Courier", 12))
tokens_text.insert(tk.END, "Tokens aparecerán aquí...")
tokens_text.config(state=tk.DISABLED)  # Hacer el campo solo lectura
tokens_text.pack()

# Frame para los Errores
frame_errors = tk.Frame(root, bg="#1c1c1c")
frame_errors.pack(side=tk.LEFT, padx=20, fill="y", expand=True)

# Título Errores
errors_title = tk.Label(frame_errors, text="Errores", font=("Helvetica", 14, "bold"), fg="white", bg="#1c1c1c")
errors_title.pack(pady=10)

# Caja de texto para Errores
errors_text = tk.Text(frame_errors, height=10, width=30, bg="#2d2d2d", fg="white", font=("Courier", 12))
errors_text.insert(tk.END, "Errores aparecerán aquí...")
errors_text.config(state=tk.DISABLED)  # Hacer el campo solo lectura
errors_text.pack()

def update_tokens(tokens_list):
    tokens_text.config(state=tk.NORMAL)  # Hacer el campo editable temporalmente
    tokens_text.delete(1.0, tk.END)  # Limpiar la caja de texto

    # Insertar los tokens en el área de texto
    tokens_text.insert(tk.END, "Tokens encontrados:\n")
    tokens_text.insert(tk.END, "\n".join(tokens_list) + "\n")
    
    tokens_text.config(state=tk.DISABLED)  # Volver a poner en modo solo lectura


def update_errors():
    errors_text.config(state=tk.NORMAL)  # Cambiar el estado a normal para permitir cambios
    errors_text.delete(1.0, tk.END)  # Limpiar la caja de texto
    
    # Configurar tags
    errors_text.tag_configure("error", foreground="red")
    errors_text.tag_configure("info", foreground="white")
    
    # Mostrar errores léxicos
    if lexer_errors:
        errors_text.insert(tk.END, "Errores léxicos:\n", "error")
        errors_text.insert(tk.END, "\n".join(lexer_errors) + "\n", "error")
    else:
        errors_text.insert(tk.END, "No hay errores léxicos.\n", "info")
    
    # Mostrar errores sintácticos
    if parser_errors:
        errors_text.insert(tk.END, "Errores sintácticos:\n", "error")
        errors_text.insert(tk.END, "\n".join(parser_errors) + "\n", "error")
    else:
        errors_text.insert(tk.END, "No hay errores sintácticos.\n", "info")
    
    # Mostrar errores semánticos
    if semantic_errors:
        errors_text.insert(tk.END, "Errores semánticos:\n", "error")
        errors_text.insert(tk.END, "\n".join(semantic_errors) + "\n", "error")
    else:
        errors_text.insert(tk.END, "No hay errores semánticos.\n", "info")
    
    errors_text.config(state=tk.DISABLED)  # Volver a poner en modo solo lectura



def process_code(data):
    lexer_errors.clear()  # Limpiar errores anteriores
    parser_errors.clear()  # Limpiar errores anteriores
    semantic_errors.clear()  # Limpiar errores semánticos anteriores

    # Paso 1: Tokenización (Lexer)
    tokens_list = get_tokens(data)  # Llama a tu lexer para obtener los tokens
    print(f"Tokens encontrados: {tokens_list}")  # Esto es para verificar los tokens

    # Paso 2: Mostrar los tokens en la UI
    update_tokens(tokens_list)  # Llamar a esta función para actualizar la UI con los tokens

    # Paso 3: Parseo (Parser)
    try:
        result = parser.parse(data)  # Llama al parser para procesar los tokens
    except Exception as e:
        print(f"Error en el parser: {e}")
    
    # Paso 4: Actualizar errores en la UI
    update_errors()  # Llama a esta función para actualizar la UI con los errores


# Crear área de código
frame_code = tk.Frame(root, bg="#333333")
frame_code.pack(pady=20, fill="both", expand=True)

# Título del editor
editor_title = tk.Label(frame_code, text="Código de entrada", font=("Helvetica", 14, "bold"), fg="white", bg="#333333")
editor_title.pack(pady=5)

# Frame para el editor con números de línea
code_frame = tk.Frame(frame_code, bg="#333333")
code_frame.pack()

# Canvas para los números de línea
line_numbers = tk.Canvas(code_frame, width=30, bg="#2d2d2d", highlightthickness=0)
line_numbers.pack(side=tk.LEFT, fill=tk.Y)

# Caja de texto para código
code_text = tk.Text(code_frame, height=20, width=60, bg="#2d2d2d", fg="grey", font=("Courier", 12), wrap=tk.WORD, insertbackground="white", yscrollcommand=lambda *args: [scrollbar.set(*args), update_line_numbers()])
placeholder = "Ingresa tu código Dart aquí..."
code_text.insert(tk.END, placeholder)
code_text.pack(side=tk.LEFT)

# Scrollbar vertical
scrollbar = tk.Scrollbar(code_frame, orient="vertical", command=lambda *args: [code_text.yview(*args), update_line_numbers()])
scrollbar.pack(side=tk.RIGHT, fill="y")

# Función para actualizar números de línea
def update_line_numbers(event=None):
    line_numbers.delete("all")
    i = code_text.index("@0,0")
    while True:
        dline = code_text.dlineinfo(i)
        if dline is None:
            break
        y = dline[1]
        line_number = str(i).split(".")[0]
        line_numbers.create_text(2, y, anchor="nw", text=line_number, fill="gray", font=("Courier", 12))
        i = code_text.index(f"{i}+1line")

# Enlaces para actualizar los números de línea en distintos eventos
code_text.bind("<KeyRelease>", update_line_numbers)
code_text.bind("<MouseWheel>", update_line_numbers)
code_text.bind("<Button-1>", update_line_numbers)
code_text.bind("<Configure>", update_line_numbers)
code_text.bind("<FocusIn>", update_line_numbers)

def clear_placeholder(event):
    current = code_text.get("1.0", tk.END).strip()
    if current == placeholder:
        code_text.delete("1.0", tk.END)
        code_text.config(fg="white")

def restore_placeholder(event):
    current = code_text.get("1.0", tk.END).strip()
    if current == "":
        code_text.insert("1.0", placeholder)
        code_text.config(fg="grey")

code_text.bind("<FocusIn>", clear_placeholder)
code_text.bind("<FocusOut>", restore_placeholder)


# Botón de ejecutar
def on_execute():
    code = code_text.get(1.0, tk.END).strip()  # Obtener el código ingresado
    process_code(code)  # Procesar el código ingresado

# Botones
frame_buttons = tk.Frame(root, bg="#1c1c1c")
frame_buttons.pack(pady=10)

# Botón de ejecutar
run_button = tk.Button(frame_buttons, text="Ejecutar", font=("Helvetica", 12), fg="white", bg="#4caf50", command=on_execute)
run_button.pack(side=tk.LEFT, padx=10)

# Ejecutar la ventana principal
root.mainloop()
