import tkinter as tk
from lexer.lexer import lexer_errors
from lexer.lexer import get_tokens  # Asegúrate de que la función get_tokens esté definida en lexer.py
from lexer.parser import parser  # Asegúrate de que tu parser esté definido en parser.py
from lexer.parser import parser_errors

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
tokens_text.insert(tk.END, "int, suma, +\nTIPO: KEYWORD, ID, PLUS\nPosición: (3, 13), (3, 13), (3, 13)")
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

def update_errors():
    errors_text.config(state=tk.NORMAL)  # Cambiar el estado a normal para permitir cambios
    errors_text.delete(1.0, tk.END)  # Limpiar la caja de texto
    
    # Mostrar errores del lexer
    if lexer_errors:
        errors_text.insert(tk.END, "Errores léxicos:\n")
        errors_text.insert(tk.END, "\n".join(lexer_errors) + "\n")
    else:
        errors_text.insert(tk.END, "No hay errores léxicos.\n")
    
    # Mostrar errores del parser
    if parser_errors:
        errors_text.insert(tk.END, "Errores sintácticos:\n")
        errors_text.insert(tk.END, "\n".join(parser_errors) + "\n")
    else:
        errors_text.insert(tk.END, "No hay errores sintácticos.\n")
    
    errors_text.config(state=tk.DISABLED)  # Volver a poner en modo solo lectura


def process_code(data):
    lexer_errors.clear()  # Limpiar errores anteriores
    parser_errors.clear()  # Limpiar errores anteriores

    # Paso 1: Tokenización (Lexer)
    tokens_list = get_tokens(data)  # Llama a tu lexer para obtener los tokens
    print(f"Tokens encontrados: {tokens_list}")  # Esto es para verificar los tokens

    # Paso 2: Parseo (Parser)
    try:
        result = parser.parse(data)  # Llama al parser para procesar los tokens
    except Exception as e:
        print(f"Error en el parser: {e}")
    
    # Paso 3: Actualizar errores en la UI
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

# Caja de texto para código
code_text = tk.Text(code_frame, height=20, width=60, bg="#2d2d2d", fg="white", font=("Courier", 12), wrap=tk.WORD)
code_text.insert(tk.END, "Ingresa tu código Dart aquí...")
code_text.pack(side=tk.LEFT)

# Botón de ejecutar
def on_execute():
    code = code_text.get(1.0, tk.END)  # Obtener el código ingresado
    process_code(code)  # Procesar el código ingresado

# Botones
frame_buttons = tk.Frame(root, bg="#1c1c1c")
frame_buttons.pack(pady=10)

# Botón de ejecutar
run_button = tk.Button(frame_buttons, text="Ejecutar", font=("Helvetica", 12), fg="white", bg="#4caf50", command=on_execute)
run_button.pack(side=tk.LEFT, padx=10)

# Ejecutar la ventana principal
root.mainloop()
