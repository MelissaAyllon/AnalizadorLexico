import tkinter as tk

# Crear la ventana principal
root = tk.Tk()
root.title("DART EDITOR")

# Configurar el tamaño de la ventana
root.geometry("1200x800")
root.config(bg="#1c1c1c")

# Título
title_label = tk.Label(root, text="DART EDITOR", font=("Helvetica", 24, "bold"), fg="white", bg="#1c1c1c")
title_label.pack(pady=20)

# Frame para los Tokens
frame_tokens = tk.Frame(root, bg="#1c1c1c")
frame_tokens.pack(side=tk.LEFT, padx=20)

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
frame_errors.pack(side=tk.LEFT, padx=20)

# Título Errores
errors_title = tk.Label(frame_errors, text="Errores", font=("Helvetica", 14, "bold"), fg="white", bg="#1c1c1c")
errors_title.pack(pady=10)

# Caja de texto para Errores
errors_text = tk.Text(frame_errors, height=10, width=30, bg="#2d2d2d", fg="white", font=("Courier", 12))
errors_text.insert(tk.END, "Error léxico: Token inválido en la línea 3.\n"
                           "Error sintáctico: Se esperaba un paréntesis en la línea 4.\n"
                           "Error semántico: No se puede realizar una operación en la línea 5.")
errors_text.config(state=tk.DISABLED)  # Hacer el campo solo lectura
errors_text.pack()

# Frame para el editor de código
frame_editor = tk.Frame(root, bg="#333333")
frame_editor.pack(pady=20)

# Título del editor
editor_title = tk.Label(frame_editor, text="Código de entrada", font=("Helvetica", 14, "bold"), fg="white", bg="#333333")
editor_title.pack(pady=5)

# Frame para el editor con números de línea
code_frame = tk.Frame(frame_editor, bg="#333333")
code_frame.pack()

# Canvas para los números de línea
line_numbers_canvas = tk.Canvas(code_frame, width=30, bg="#2d2d2d", bd=0, highlightthickness=0)
line_numbers_canvas.pack(side=tk.LEFT, fill=tk.Y)

# Función para actualizar los números de línea
def update_line_numbers(event=None):
    line_numbers_canvas.delete("all")
    num_lines = int(code_text.index('end-1c').split('.')[0])
    for i in range(1, num_lines + 1):
        line_numbers_canvas.create_text(2, 20 * i, anchor="nw", text=str(i), font=("Courier", 12), fill="white")

# Caja de texto para código
code_text = tk.Text(code_frame, height=20, width=60, bg="#2d2d2d", fg="white", font=("Courier", 12), wrap=tk.WORD)
code_text.insert(tk.END, "Ingresa tu código Dart aquí...")
code_text.pack(side=tk.LEFT)

# Actualizar números de línea cuando el texto cambia
code_text.bind("<KeyRelease>", update_line_numbers)
update_line_numbers()  # Inicializar los números de línea al inicio

# Botones
frame_buttons = tk.Frame(root, bg="#1c1c1c")
frame_buttons.pack(pady=10)

# Botón de borrar
clear_button = tk.Button(frame_buttons, text="Borrar", font=("Helvetica", 12), fg="white", bg="#ff4c4c", command=lambda: code_text.delete(1.0, tk.END))
clear_button.pack(side=tk.LEFT, padx=10)

# Botón de ejecutar
run_button = tk.Button(frame_buttons, text="Ejecutar", font=("Helvetica", 12), fg="white", bg="#4caf50")
run_button.pack(side=tk.LEFT, padx=10)

# Ejecutar la ventana principal
root.mainloop()
