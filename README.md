# Analizador Léxico, Sintáctico y Semántico para Dart

Este proyecto implementa un analizador completo (léxico, sintáctico y semántico) para el lenguaje Dart utilizando Python y la biblioteca PLY.

## 📋 Requisitos del Sistema

- **Python 3.7 o superior**
- **Git** (para obtener el nombre de usuario en los logs)

## 📦 Dependencias

### Librerías/Bibliotecas Requeridas

```bash
# Instalar dependencias principales
pip install ply
pip install pytest

# O usar el archivo requirements.txt
pip install -r requirements.txt
```

### Dependencias del Sistema
- **Tkinter**: Incluido con Python (no requiere instalación adicional)
- **subprocess**: Módulo estándar de Python
- **os, time, io, sys**: Módulos estándar de Python

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

## 🚀 Uso

### Interfaz Gráfica (Recomendado)
```bash
python src/ui.py
```

### Analizador Léxico
```bash
python src/lexer/lexer.py
```

### Analizador Sintáctico y Semántico
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

## ✨ Características Implementadas

### 🔍 Analizador Léxico
- ✅ Reconocimiento de tokens básicos (identificadores, números, strings)
- ✅ Palabras reservadas de Dart (solo las utilizadas en algoritmos de prueba)
- ✅ Operadores y símbolos especiales
- ✅ Comentarios (línea única y múltiples líneas)
- ✅ Detección de errores léxicos con mensajes detallados

### 📝 Analizador Sintáctico
- ✅ Declaraciones de variables (var, final, tipos específicos)
- ✅ Expresiones aritméticas y booleanas
- ✅ Estructuras de control (if, while, for tradicional y for-in)
- ✅ Declaraciones de funciones y clases
- ✅ Estructuras de datos (List, Map, Set)
- ✅ Tipos de datos (int, double, bool, String)
- ✅ **2 tipos de errores sintácticos**: Errores de tokens inesperados y errores de fin de entrada

### 🧠 Analizador Semántico
- ✅ **Carlos Salazar**: 2 reglas semánticas para estructuras de datos
  - Validación de tipos homogéneos en listas
  - Validación de tipos de claves en maps
- ✅ **Melissa Ayllon**: 2 reglas semánticas para estructuras de control
  - Validación de condiciones booleanas en bucles
  - Validación de condiciones booleanas en if
- ✅ **Noelia Pasaca**: 2 reglas semánticas para funciones
  - Validación de tipos de retorno en funciones
  - Validación de tipos de parámetros

### 🖥️ Interfaz Gráfica
- ✅ Editor de código con números de línea
- ✅ Visualización de tokens en tiempo real
- ✅ Panel de errores (léxicos, sintácticos, semánticos)
- ✅ Tema oscuro moderno
- ✅ Botón de ejecución
- ✅ **Resultados visibles en la interfaz cuando se detectan errores**

## 👥 Contribuciones por Integrante

### Carlos Salazar
- **Estructuras de datos**: List, Map, Set
- **Reglas semánticas**: Validación de tipos homogéneos en listas y maps
- **Algoritmo de prueba**: `algoritmo_carlos.dart` - Gestión de productos con estructuras de datos

### Melissa Ayllon
- **Estructuras de control**: if, while, for loops
- **Reglas semánticas**: Validación de condiciones booleanas en bucles e if
- **Algoritmo de prueba**: `algoritmo_melissa.dart` - Gestión de tareas con bucles

### Noelia Pasaca
- **Funciones y validaciones**: Declaración y validación de funciones
- **Reglas semánticas**: Validación de tipos de retorno y parámetros
- **Algoritmo de prueba**: `algoritmo_noelia.dart` - Calculadora con funciones y validaciones

## 📊 Algoritmos de Prueba

Cada integrante posee su algoritmo de prueba específico:

### `algoritmo_carlos.dart`
- **Enfoque**: Estructuras de datos (List, Map, Set)
- **Funcionalidad**: Gestión de productos con precios y categorías
- **Características**: Declaración de clases, listas tipadas, maps, sets

### `algoritmo_melissa.dart`
- **Enfoque**: Estructuras de control (for, if)
- **Funcionalidad**: Gestión de tareas con estados
- **Características**: Bucles for tradicional y for-in, condicionales

### `algoritmo_noelia.dart`
- **Enfoque**: Funciones y validaciones
- **Funcionalidad**: Calculadora con validaciones matemáticas
- **Características**: Funciones estáticas, validaciones de parámetros

## 📝 Logs

Los archivos de log se generan automáticamente en `tests/logs/` con el formato:
- **Léxico**: `lexico-{username}-{timestamp}-{filename}.txt`
- **Sintáctico**: `sintactico-{username}-{timestamp}-{filename}.txt`

## 🧪 Testing

Para ejecutar las pruebas:
```bash
# Probar todos los algoritmos
python src/lexer/parser.py

# Probar solo el lexer
python src/lexer/lexer.py
```
