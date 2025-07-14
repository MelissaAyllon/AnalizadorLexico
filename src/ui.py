import tkinter as tk
from lexer.lexer import lexer_errors
from lexer.lexer import get_tokens  
from lexer.parser import parser  
from lexer.parser import parser_errors
from lexer.parser import semantic_errors 

# Create the main window
root = tk.Tk()
root.title("DART EDITOR")

# Set the window size
root.geometry("800x600")
root.config(bg="#1c1c1c")

# Qualification
title_label = tk.Label(root, text="DART EDITOR", font=("Helvetica", 24, "bold"), fg="white", bg="#1c1c1c")
title_label.pack(pady=20)

# Frame for Tokens
frame_tokens = tk.Frame(root, bg="#1c1c1c")
frame_tokens.pack(side=tk.LEFT, padx=20, fill="y", expand=True)

# Title Tokens
tokens_title = tk.Label(frame_tokens, text="Tokens", font=("Helvetica", 14, "bold"), fg="white", bg="#1c1c1c")
tokens_title.pack(pady=10)

# Text box for Tokens
tokens_text = tk.Text(frame_tokens, height=10, width=30, bg="#2d2d2d", fg="white", font=("Courier", 12))
tokens_text.insert(tk.END, "Tokens aparecerán aquí...")
tokens_text.config(state=tk.DISABLED)  # Make the field read-only
tokens_text.pack()

# Frame for Errors
frame_errors = tk.Frame(root, bg="#1c1c1c")
frame_errors.pack(side=tk.LEFT, padx=20, fill="y", expand=True)

# Title Errors
errors_title = tk.Label(frame_errors, text="Errores", font=("Helvetica", 14, "bold"), fg="white", bg="#1c1c1c")
errors_title.pack(pady=10)

# Text box for Errors
errors_text = tk.Text(frame_errors, height=10, width=30, bg="#2d2d2d", fg="white", font=("Courier", 12))
errors_text.insert(tk.END, "Errores aparecerán aquí...")
errors_text.config(state=tk.DISABLED)  # Make the field read-only
errors_text.pack()

def update_tokens(tokens_list):
    tokens_text.config(state=tk.NORMAL)  # Make the field temporarily editable
    tokens_text.delete(1.0, tk.END)  # Clear the text box

    # Insert the tokens into the text area
    tokens_text.insert(tk.END, "Tokens encontrados:\n")
    tokens_text.insert(tk.END, "\n".join(tokens_list) + "\n")
    
    tokens_text.config(state=tk.DISABLED)  # Return to read-only mode


def update_errors():
    errors_text.config(state=tk.NORMAL)  # Change the state to normal to allow changes
    errors_text.delete(1.0, tk.END)  # Clear the text box
    
    # Configure tags
    errors_text.tag_configure("error", foreground="red")
    errors_text.tag_configure("info", foreground="white")
    
    # Show lexical errors
    if lexer_errors:
        errors_text.insert(tk.END, "Errores léxicos:\n", "error")
        errors_text.insert(tk.END, "\n".join(lexer_errors) + "\n", "error")
    else:
        errors_text.insert(tk.END, "No hay errores léxicos.\n", "info")
    
    # Show syntactical errors
    if parser_errors:
        errors_text.insert(tk.END, "Errores sintácticos:\n", "error")
        errors_text.insert(tk.END, "\n".join(parser_errors) + "\n", "error")
    else:
        errors_text.insert(tk.END, "No hay errores sintácticos.\n", "info")
    
    # Show semantic errors
    if semantic_errors:
        errors_text.insert(tk.END, "Errores semánticos:\n", "error")
        errors_text.insert(tk.END, "\n".join(semantic_errors) + "\n", "error")
    else:
        errors_text.insert(tk.END, "No hay errores semánticos.\n", "info")
    
    errors_text.config(state=tk.DISABLED)  # Return to read-only mode



def process_code(data):
    lexer_errors.clear()  # Clean up previous errors
    parser_errors.clear()  # Clean up previous errors
    semantic_errors.clear()  # Clean up previous semantic errors
    
    import lexer.parser as parser_module
    parser_module.current_line = 1
    

    # Step 1: Tokenization (Lexer)
    tokens_list = get_tokens(data)  # Your lexer is called to get the tokens
    print(f"Tokens encontrados: {tokens_list}")  # This is to verify the tokens

    # Step 2: Display the tokens in the UI
    update_tokens(tokens_list)  # This function is called to update the UI with the tokens

    # Step 3: Parsing
    try:
        result = parser.parse(data)  # The parser is called to process the tokens
    except Exception as e:
        print(f"Error en el parser: {e}")
    
    # Step 4: Update errors in the UI
    update_errors()  # This function is called to update the UI with errors


# Create code area
frame_code = tk.Frame(root, bg="#333333")
frame_code.pack(pady=20, fill="both", expand=True)

# Publisher Title
editor_title = tk.Label(frame_code, text="Código de entrada", font=("Helvetica", 14, "bold"), fg="white", bg="#333333")
editor_title.pack(pady=5)

# Frame for the editor with line numbers
code_frame = tk.Frame(frame_code, bg="#333333")
code_frame.pack()

# Canvas for line numbers
line_numbers = tk.Canvas(code_frame, width=30, bg="#2d2d2d", highlightthickness=0)
line_numbers.pack(side=tk.LEFT, fill=tk.Y)

# Text box for code
code_text = tk.Text(code_frame, height=20, width=60, bg="#2d2d2d", fg="grey", font=("Courier", 12), wrap=tk.WORD, insertbackground="white", yscrollcommand=lambda *args: [scrollbar.set(*args), update_line_numbers()])
placeholder = "Ingresa tu código Dart aquí..."
code_text.insert(tk.END, placeholder)
code_text.pack(side=tk.LEFT)

# Vertical scrollbar
scrollbar = tk.Scrollbar(code_frame, orient="vertical", command=lambda *args: [code_text.yview(*args), update_line_numbers()])
scrollbar.pack(side=tk.RIGHT, fill="y")

# Function to update line numbers
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

# Links to update line numbers in different events
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


# Run button
def on_execute():
    code = code_text.get(1.0, tk.END).strip()  # Get the entered code
    process_code(code)  # Process the entered code

# Buttons
frame_buttons = tk.Frame(root, bg="#1c1c1c")
frame_buttons.pack(pady=10)

# Run button
run_button = tk.Button(frame_buttons, text="Ejecutar", font=("Helvetica", 12), fg="white", bg="#4caf50", command=on_execute)
run_button.pack(side=tk.LEFT, padx=10)

# Run the main window
root.mainloop()
