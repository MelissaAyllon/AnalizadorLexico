# Analizador Léxico y Sintáctico para Dart

Este proyecto implementa un analizador léxico y sintáctico para el lenguaje Dart utilizando Python y la biblioteca PLY.

## Configuración del Entorno Virtual

### 1. Crear el entorno virtual
```bash
python3 -m venv venv
```

### 2. Activar el entorno virtual
```bash
# En macOS/Linux
source venv/bin/activate

# En Windows
venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Desactivar el entorno virtual (cuando termines)
```bash
deactivate
```

## Uso

### Analizador Léxico
```bash
python src/lexer/lexer.py
```

### Analizador Sintáctico
```bash
python src/lexer/parser.py
```

## Estructura del Proyecto

```
AnalizadorLexico/
├── src/
│   └── lexer/
│       ├── lexer.py      # Analizador léxico
│       ├── parser.py     # Analizador sintáctico
│       ├── logger.py     # Funciones de logging
│       └── reserved.py   # Palabras reservadas
├── tests/
│   ├── dart_examples/    # Archivos de prueba Dart
│   └── logs/            # Archivos de log generados
├── requirements.txt     # Dependencias del proyecto
└── README.md           # Este archivo
```

## Características Implementadas

### Analizador Léxico
- Reconocimiento de tokens básicos (identificadores, números, strings)
- Palabras reservadas de Dart
- Operadores y símbolos especiales
- Comentarios (línea única y múltiples líneas)

### Analizador Sintáctico
- Declaraciones de variables (var, final, String)
- Expresiones aritméticas y booleanas
- Estructuras de control (if, while, for)
- Declaraciones de funciones y clases
- Listas, Maps y Sets
- Tipos de datos (int, double, bool, String)

## Contribuciones

- **Carlos Salazar**: Funciones básicas del lexer y parser
- **Melissa Ayllon**: Operadores y estructuras de control
- **Noelia Pasaca**: For loops, Maps, Sets, Double y procesamiento de archivos

## Logs

Los archivos de log se generan automáticamente en `tests/logs/` con el formato:
- Léxico: `lexico-{username}-{timestamp}-{filename}.txt`
- Sintáctico: `sintactico-{username}-{timestamp}-{filename}.txt`
