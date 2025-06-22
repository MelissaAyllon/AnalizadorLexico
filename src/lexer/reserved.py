control_flow_keywords = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'do': 'DO',
    'switch': 'SWITCH',
    'case': 'CASE',
    'default': 'DEFAULT',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN',
    'try': 'TRY',
    'catch': 'CATCH',
    'finally': 'FINALLY',
    'throw': 'THROW',
    'rethrow': 'RETHROW',
    'yield': 'YIELD',
}

declaration_keywords = {
    'var': 'VAR',
    'final': 'FINAL',
    'const': 'CONST',
    'dynamic': 'DYNAMIC',
    'void': 'VOID',
    'int': 'INT',
    'bool': 'BOOL',
    'double': 'DOUBLE',
    'String': 'STRING',
    'typedef': 'TYPEDEF',
    'class': 'CLASS',
    'enum': 'ENUM',
    'abstract': 'ABSTRACT',
    'interface': 'INTERFACE',
    'mixin': 'MIXIN',
    'extends': 'EXTENDS',
    'implements': 'IMPLEMENTS',
    'operator': 'OPERATOR',
    'static': 'STATIC',
    'covariant': 'COVARIANT',
    'List': 'LIST',
    'print': 'PRINT',
}

functions_reserved = {
    'async': 'ASYNC',
    'await': 'AWAIT',
    'sync': 'SYNC',
    'factory': 'FACTORY',
    'get': 'GET',
    'set': 'SET',
    'function': 'FUNCTION',
}

libraries_reserved = {
    'import': 'IMPORT',
    'export': 'EXPORT',
    'library': 'LIBRARY',
    'part': 'PART',
    'deferred': 'DEFERRED',
    'show': 'SHOW',
    'hide': 'HIDE',
    'stdin': 'STDIN',
    'stdout': 'STDOUT',
    'stderr': 'STDERR',
    'readLineSync': 'READLINESYNC',
}

other_reserved = {
    'null': 'NULL',
    'true': 'TRUE',
    'false': 'FALSE',
    'this': 'THIS',
    'super': 'SUPER',
    'as': 'AS',
    'is': 'IS',
    'in': 'IN',
    'new': 'NEW',
    'default': 'DEFAULT',
}

# Combinando las palabras clave de todos los diccionarios
reserved = {**control_flow_keywords,
            **declaration_keywords,
            **functions_reserved,
            **libraries_reserved,
            **other_reserved}