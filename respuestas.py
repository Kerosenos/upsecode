RESPUESTAS_PRACTICA = {
    # ============================================
    # Nivel 1: Fundamentos de Python (PRÁCTICA)
    # ============================================
    1: {
        1: {'patrones': [r'print\([\'"]hello\s*world[\'"]\)']},
        2: {'patrones': [r'\w+\s*=\s*\d+', r'print\(\w+\s*\+\s*\w+\)']},
        3: {'patrones': [r'type\(.*\)']},
        4: {'patrones': [r'type\(.*\)']},
        5: {'patrones': [r'type\(.*\)']},
        6: {'patrones': [r'type\(.*\)']},
        7: {'patrones': [r'print\(.*\+.*,.*\-.*,.*\*.*,.*\/.*\)']},
        8: {'patrones': [r'print\(\d+\s*>\s*\d+\)']},
        9: {'patrones': [r'print\(.*and.*\)']},
        10: {'patrones': [r'\w+\s*=\s*\d+', r'print\(\w+\s*\+\s*\w+\)']},
        11: {'patrones': [r'print\(\d+\.\d+\s*\+\s*\d+\)']},
        12: {'patrones': [r'print\(.*\+\s*str\(.*\)\)']},
        13: {'patrones': [r'if\s+\w+\s*:']}
    },
    
    # ============================================
    # Nivel 2: Control de Flujo (PRÁCTICA)
    # ============================================
    2: {
        1: {'patrones': [r'if\s+\w+\s*>\s*0\s*:']},
        2: {'patrones': [r'if\s+.*:.*else\s*:']},
        3: {'patrones': [r'if\s+.*:.*elif\s+.*:.*else\s*:']},
        4: {'patrones': [r'for\s+\w+\s+in\s+range\(.*\)\s*:']},
        5: {'patrones': [r'while\s+\w+\s*<=\s*\d+\s*:']},
        6: {'patrones': [r'if\s+\w+\s*==\s*\d+\s*:.*break']},
        7: {'patrones': [r'if\s+\w+\s*==\s*\d+\s*:.*continue']},
        8: {'patrones': [r'if\s+.*:.*pass']},
        9: {'patrones': [r'if\s+.*and\s+.*:']},
        10: {'patrones': [r'while\s+True\s*:.*if\s+.*:.*break']},
        11: {'patrones': [r'for\s+.*:.*else\s*:']},
        12: {'patrones': [r'while\s+.*:.*else\s*:']},
        13: {'patrones': [r'for\s+.*:.*for\s+.*:']}
    },
    
    # ============================================
    # Nivel 3: Estructuras de Datos (PRÁCTICA)
    # ============================================
    3: {
        1: {'patrones': [r'\[\d+,\s*\d+,\s*\d+\]']},
        2: {'patrones': [r'\(\d+,\s*\d+,\s*\d+\)']},
        3: {'patrones': [r'lista\[0\]']},
        4: {'patrones': [r'tupla\[-1\]']},
        5: {'patrones': [r'\.append\(\d+\)']},
        6: {'patrones': [r'\.remove\(\d+\)']},
        7: {'patrones': [r'\{\s*[\'"]\w+[\'"]\s*:\s*\d+\s*,\s*[\'"]\w+[\'"]\s*:\s*\d+\s*\}']},
        8: {'patrones': [r'dic\[[\'"]\w+[\'"]\]\s*=\s*\d+']},
        9: {'patrones': [r'del\s+dic\[[\'"]\w+[\'"]\]']},
        10: {'patrones': [r'\{\d+,\s*\d+,\s*\d+\}']},
        11: {'patrones': [r'\.add\(\d+\)']},
        12: {'patrones': [r'\.discard\(\d+\)']},
        13: {'patrones': [r'for\s+\w+\s+in\s+\w+\s*:']}
    },
    
    # ============================================
    # Nivel 4: Funciones (PRÁCTICA)
    # ============================================
    4: {
        1: {'patrones': [r'def\s+\w+\(\s*\)\s*:.*print\([\'"].*[\'"]\)']},
        2: {'patrones': [r'def\s+\w+\(\w+\)\s*:.*f?[\'"]Hola\s*{?\w+}?[\'"]']},
        3: {'patrones': [r'def\s+\w+\(\w+,\s*\w+\)\s*:.*return\s+\w+\s*\+\s*\w+']},
        4: {'patrones': [r'return\s+\w+\s+if\s+\w+\s*>\s*\w+\s+else\s+\w+']},
        5: {'patrones': [r'def\s+\w+\(\w+\)\s*:.*return\s+len\(\w+\)']},
        6: {'patrones': [r'def\s+\w+\(\w+=[\'"]\w+[\'"]\)\s*:']},
        7: {'patrones': [r'def\s+\w+\(\*args\)\s*:.*sum\(args\)']},
        8: {'patrones': [r'def\s+\w+\(\*\*\w+\)\s*:.*print\(\w+\)']},
        9: {'patrones': [r'return\s+\w+\s*\+\s*\w+\s*,\s*\w+\s*\-\s*\w+']},
        10: {'patrones': [r'def\s+\w+\(\s*\)\s*:.*def\s+\w+\(\s*\)\s*:']},
        11: {'patrones': [r'global\s+\w+', r'\w+\s*\+=\s*1']},
        12: {'patrones': [r'def\s+\w+\(\w+\)\s*:.*if\s+\w+\s*==\s*0\s*:.*return\s+1.*else:.*return\s+\w+\s*\*\s*\w+\(\w+\s*\-\s*1\)']},
        13: {'patrones': [r'def\s+\w+\(\w+\)\s*:.*for\s+\w+\s+in\s+\w+\s*:.*\w+\(\)']}
    }
}

RESPUESTAS_EVALUACION = {
    # ============================================
    # Nivel 1: Fundamentos de Python (EVALUACIÓN)
    # ============================================
    1: {
        1: {
            'patrones': [r'print\([\'"]hello\s*world[\'"]\)'],
            'salida': "Hello World"
        },
        2: {
            'patrones': [r'\w+\s*=\s*\d+', r'print\(\w+\s*\+\s*\w+\)'],
            'salida': "8"
        },
        3: {
            'patrones': [r'type\(.*\)'],
            'salida': "<class 'int'>"
        },
        4: {
            'patrones': [r'type\(.*\)'],
            'salida': "<class 'float'>"
        },
        5: {
            'patrones': [r'type\(.*\)'],
            'salida': "<class 'str'>"
        },
        6: {
            'patrones': [r'type\(.*\)'],
            'salida': "<class 'bool'>"
        },
        7: {
            'patrones': [r'print\(.*\+.*,.*\-.*,.*\*.*,.*\/.*\)'],
            'salida': "7 3 10 2.5"
        },
        8: {
            'patrones': [r'print\(\d+\s*>\s*\d+\)'],
            'salida': "True"
        }
    },
    
    # ============================================
    # Nivel 2: Control de Flujo (EVALUACIÓN)
    # ============================================
    2: {
        1: {
            'patrones': [r'if\s+\w+\s*>\s*0\s*:'],
            'salida': "x es positivo",
            'entrada': "5"
        },
        2: {
            'patrones': [r'if\s+.*:.*else\s*:'],
            'salida': "x es negativo o cero",
            'entrada': "-3"
        },
        3: {
            'patrones': [r'if\s+.*:.*elif\s+.*:.*else\s*:'],
            'salida': "Cero",
            'entrada': "0"
        },
        4: {
            'patrones': [r'for\s+\w+\s+in\s+range\(.*\)\s*:'],
            'salida': "1\n2\n3\n4\n5"
        },
        5: {
            'patrones': [r'while\s+\w+\s*<=\s*\d+\s*:'],
            'salida': "1\n2\n3\n4\n5"
        },
        6: {
            'patrones': [r'if\s+\w+\s*==\s*\d+\s*:.*break'],
            'salida': "0\n1\n2"
        },
        7: {
            'patrones': [r'if\s+\w+\s*==\s*\d+\s*:.*continue'],
            'salida': "0\n1\n3\n4"
        },
        8: {
            'patrones': [r'if\s+.*:.*pass'],
            'salida': ""
        }
    },
    
    # ============================================
    # Nivel 3: Estructuras de Datos (EVALUACIÓN)
    # ============================================
    3: {
        1: {
            'patrones': [r'\[\d+,\s*\d+,\s*\d+\]'],
            'salida': "[1, 2, 3]"
        },
        2: {
            'patrones': [r'\(\d+,\s*\d+,\s*\d+\)'],
            'salida': "(1, 2, 3)"
        },
        3: {
            'patrones': [r'lista\[0\]'],
            'salida': "1"
        },
        4: {
            'patrones': [r'tupla\[-1\]'],
            'salida': "3"
        },
        5: {
            'patrones': [r'\.append\(\d+\)'],
            'salida': "[1, 2, 3, 4]"
        },
        6: {
            'patrones': [r'\.remove\(\d+\)'],
            'salida': "[1, 3]"
        },
        7: {
            'patrones': [r'\{\s*[\'"]\w+[\'"]\s*:\s*\d+\s*,\s*[\'"]\w+[\'"]\s*:\s*\d+\s*\}'],
            'salida': "1"
        },
        8: {
            'patrones': [r'dic\[[\'"]\w+[\'"]\]\s*=\s*\d+'],
            'salida': "{'a': 1, 'b': 2, 'c': 3}"
        }
    },
    
    # ============================================
    # Nivel 4: Funciones (EVALUACIÓN)
    # ============================================
    4: {
        1: {
            'patrones': [r'def\s+\w+\(\s*\)\s*:.*print\([\'"].*[\'"]\)'],
            'salida': "Hola desde una función"
        },
        2: {
            'patrones': [r'def\s+\w+\(\w+\)\s*:.*f?[\'"]Hola\s*{?\w+}?[\'"]'],
            'salida': "Hola Ana",
            'entrada': "Ana"
        },
        3: {
            'patrones': [r'def\s+\w+\(\w+,\s*\w+\)\s*:.*return\s+\w+\s*\+\s*\w+'],
            'salida': "7",
            'entrada': "3,4"
        },
        4: {
            'patrones': [r'return\s+\w+\s+if\s+\w+\s*>\s*\w+\s+else\s+\w+'],
            'salida': "5",
            'entrada': "5,2"
        },
        5: {
            'patrones': [r'def\s+\w+\(\w+\)\s*:.*return\s+len\(\w+\)'],
            'salida': "3",
            'entrada': "[1,2,3]"
        },
        6: {
            'patrones': [r'def\s+\w+\(\w+=[\'"]\w+[\'"]\)\s*:'],
            'salida': "Hola Usuario"
        },
        7: {
            'patrones': [r'def\s+\w+\(\*args\)\s*:.*sum\(args\)'],
            'salida': "6",
            'entrada': "1,2,3"
        },
        8: {
            'patrones': [r'def\s+\w+\(\*\*\w+\)\s*:.*print\(\w+\)'],
            'salida': "{'a': 1, 'b': 2}",
            'entrada': "a=1,b=2"
        }
    }
}