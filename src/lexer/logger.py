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