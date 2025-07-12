# Palabras reservadas utilizadas en los algoritmos de prueba
# Basado en el análisis de algoritmo_carlos.dart, algoritmo_melissa.dart, algoritmo_noelia.dart

control_flow_keywords = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'return': 'RETURN',
}

declaration_keywords = {
    'var': 'VAR',
    'final': 'FINAL',
    'void': 'VOID',
    'int': 'INT_TYPE',
    'bool': 'BOOL_TYPE',
    'double': 'DOUBLE_TYPE',
    'String': 'STRING_TYPE',
    'class': 'CLASS',
    'static': 'STATIC',
    'List': 'LIST',
    'Map': 'MAP',
    'Set': 'SET',
    'print': 'PRINT',
}

libraries_reserved = {
    'stdin': 'STDIN',
    'readLineSync': 'READLINESYNC',
}

other_reserved = {
    'null': 'NULL',
    'true': 'TRUE',
    'false': 'FALSE',
    'this': 'THIS',
    'new': 'NEW',
    'in': 'IN',
}

# Combinando las palabras clave utilizadas
reserved = {**control_flow_keywords,
            **declaration_keywords,
            **libraries_reserved,
            **other_reserved}