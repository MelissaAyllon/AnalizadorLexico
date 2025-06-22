import subprocess
import os
import time

def get_git_username():
    try:
        result = subprocess.run(
            ['git', 'config', '--get', 'user.name'], 
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        
        username = result.stdout.decode('utf-8').strip()
        
        if username:
            return username
        else:
            raise ValueError("Git username no esta especificado, vea git config.")
    
    except Exception as e:
        print(f"Error obteniendo Git username: {e}")
        return None
    
def create_log_file(tokens_list, source_file=None, log_folder="./tests/logs"):
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    current_time = time.strftime("%d-%m-%Y-%Hh%M")
    username = get_git_username()
    
    # Extraer el nombre del archivo fuente si se proporciona
    source_name = os.path.basename(source_file) if source_file else "unknown"
    log_file_name = f"lexico-{username}-{current_time}-{source_name}.txt"

    log_file_path = os.path.join(log_folder, log_file_name)

    with open(log_file_path, "w") as log_file:
        if source_file:
            log_file.write(f"Archivo procesado: {source_file}\n")
            log_file.write("-" * 50 + "\n")
        for token in tokens_list:
            log_file.write(f"{token}\n")

    print(f"Log guardado en {log_file_path}")

# CONTRIBUCION: NOELIA PASACA

def read_dart_file(file_path):
    """Lee un archivo Dart y retorna su contenido"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{file_path}'")
        return None
    except Exception as e:
        print(f"Error al leer el archivo '{file_path}': {e}")
        return None

def process_dart_file_parser(file_path, parser):
    """Procesa un archivo Dart completo con el parser"""
    print(f"\n=== Procesando archivo: {file_path} ===")
    content = read_dart_file(file_path)
    if content is None:
        return []
    
    # Dividir el contenido en líneas para procesar cada declaración
    lines = content.split('\n')
    line_number = 0
    results = []
    
    for line in lines:
        line_number += 1
        line = line.strip()
        
        # Ignorar líneas vacías y comentarios
        if not line or line.startswith('//') or line.startswith('/*'):
            continue
            
        print(f"\n--- Línea {line_number}: {line} ---")
        
        # Capturar la salida de print para detectar mensajes del parser
        import io
        import sys
        from contextlib import redirect_stdout
        
        f = io.StringIO()
        with redirect_stdout(f):
            try:
                result = parser.parse(line)
                output = f.getvalue().strip()
                
                if output:
                    # Si hay salida del parser (mensajes de print), agregarla
                    results.append(f"Línea {line_number}: {output}")
                    print(f"Resultado: {output}")
                elif result is not None:
                    # Si no hay salida pero hay resultado, agregarlo
                    results.append(f"Línea {line_number}: {result}")
                    print(f"Resultado: {result}")
                else:
                    # Si no hay salida ni resultado, agregar un mensaje de procesamiento
                    results.append(f"Línea {line_number}: Procesada sin resultado")
                    print("Procesada sin resultado")
                    
            except Exception as e:
                error_msg = f"Error en línea {line_number}: {e}"
                results.append(error_msg)
                print(error_msg)
    
    print(f"=== Fin del procesamiento de {file_path} ===\n")
    return results

def process_test_directory_parser(parser):
    """Procesa todos los archivos .dart en el directorio de pruebas con el parser"""
    test_dir = "tests/dart_examples"
    
    if not os.path.exists(test_dir):
        print(f"Error: El directorio '{test_dir}' no existe")
        return
    
    dart_files = [f for f in os.listdir(test_dir) if f.endswith('.dart')]
    
    if not dart_files:
        print(f"No se encontraron archivos .dart en '{test_dir}'")
        return
    
    print(f"Archivos Dart encontrados: {dart_files}")
    
    all_results = []
    for file_name in dart_files:
        file_path = os.path.join(test_dir, file_name)
        results = process_dart_file_parser(file_path, parser)
        if results:
            all_results.extend(results)
    
    return all_results

def create_parser_log_file(results_list, source_files=None, log_folder="./tests/logs"):
    """Crea un archivo de log para los resultados del parser"""
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    current_time = time.strftime("%d-%m-%Y-%Hh%M")
    username = get_git_username()
    
    # Extraer el nombre de los archivos fuente si se proporcionan
    if source_files:
        source_names = [os.path.basename(f) for f in source_files]
        source_name = "-".join(source_names)
    else:
        source_name = "parser_results"
    
    log_file_name = f"sintactico-{username}-{current_time}-{source_name}.txt"
    log_file_path = os.path.join(log_folder, log_file_name)

    with open(log_file_path, "w", encoding='utf-8') as log_file:
        log_file.write("=== ANÁLISIS SINTÁCTICO ===\n")
        log_file.write("-" * 50 + "\n")
        if source_files:
            log_file.write(f"Archivos procesados: {', '.join(source_files)}\n")
            log_file.write("-" * 50 + "\n")
        for result in results_list:
            log_file.write(f"{result}\n")

    print(f"Log del parser guardado en {log_file_path}")
    return log_file_path