from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
from werkzeug.utils import secure_filename
import os
from flask_socketio import SocketIO, emit
import json
from datetime import datetime
import re
import time
import asyncio
import threading
import pickle
from functools import reduce
from evaluador import Evaluador

app = Flask(__name__)
app.secret_key = 'upse_secret_key_123'  # Cambia esto por una clave secreta única
socketio = SocketIO(app)

def escapejs_filter(value):
    return str(value).replace("'", "\\'").replace('"', '\\"')
app.jinja_env.filters['escapejs'] = escapejs_filter


app.config['UPLOAD_FOLDER'] = 'static/fotos'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Función para verificar extensiones de archivo
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Inicialización de la base de datos
def init_db():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        
        # Tabla de usuarios (la que ya tenías)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            cedula TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            nivel INTEGER DEFAULT 1,
            foto TEXT DEFAULT 'default.jpg',
            descripcion TEXT DEFAULT '',
            año_nacimiento INTEGER DEFAULT 2000,
            carrera TEXT DEFAULT '',
            año_carrera INTEGER DEFAULT 1,
            lenguajes TEXT DEFAULT '',
            registro_completo BOOLEAN DEFAULT FALSE
        )
        """)

        # NUEVA TABLA DE MENSAJES (esto es lo que agregamos)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS mensajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            remitente_id INTEGER NOT NULL,
            destinatario_id INTEGER NOT NULL,
            mensaje TEXT NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (remitente_id) REFERENCES users(id),
            FOREIGN KEY (destinatario_id) REFERENCES users(id)
        )
        """)


# Preguntas del cuestionario inicial - Ahora con 20 niveles
preguntas = [
    {"pregunta": "¿Qué tipo de dato es: 5?", "respuesta": "int"},
    {"pregunta": "¿Qué palabra se usa para condicionales en Python?", "respuesta": "if"},
    {"pregunta": "¿Cómo se llama la estructura que usa []?", "respuesta": "lista"},
    {"pregunta": "¿Cómo defines una función? Escribe la palabra clave", "respuesta": "def"},
    {"pregunta": "¿Qué palabra clave se usa para importar módulos?", "respuesta": "import"},
    {"pregunta": "¿Qué función usas para abrir un archivo?", "respuesta": "open"},
    {"pregunta": "¿Cómo se llama el método que inicializa una clase?", "respuesta": "__init__"},
    {"pregunta": "¿Qué palabra se usa para manejar errores?", "respuesta": "try"},
    {"pregunta": "¿Cómo defines una función anónima?", "respuesta": "lambda"},
    {"pregunta": "¿Qué palabra se usa para crear generadores?", "respuesta": "yield"},
    {"pregunta": "¿Qué símbolo se usa para decoradores?", "respuesta": "@"},
    {"pregunta": "¿Qué módulo maneja fechas?", "respuesta": "datetime"},
    {"pregunta": "¿Qué módulo maneja expresiones regulares?", "respuesta": "re"},
    {"pregunta": "¿Qué módulo se usa para hilos?", "respuesta": "threading"},
    {"pregunta": "¿Qué palabra clave se usa para funciones async?", "respuesta": "async"},
    {"pregunta": "¿Qué módulo convierte datos a JSON?", "respuesta": "json"},
    {"pregunta": "¿Qué módulo conecta a SQLite?", "respuesta": "sqlite3"},
    {"pregunta": "¿Qué módulo se usa para pruebas unitarias?", "respuesta": "unittest"},
    {"pregunta": "¿Qué defines con 'class'?", "respuesta": "clase"},
    {"pregunta": "¿Qué módulo se usa para perfilamiento?", "respuesta": "cprofile"}
]







# Diccionario completo con las 20 lecciones
LECCIONES = {
    1: {
        "titulo": "Fundamentos de Python",
        "contenido": {
            "explicacion": "Python es un lenguaje que usa indentación para bloques de código."
            "mucho texto..."
            "........."
            "........."
            ".........",
            "ejercicios_practica": [
                "Haz un programa que imprima 'Hello, world!'",
                "Escribe un programa que guarde tu nombre en una variable y lo imprima",
                "Crea un programa que sume dos números enteros y muestre el resultado",
                "Haz un programa que divida dos números decimales y muestre el resultado",
                "Escribe un programa que muestre el tipo de un valor (por ejemplo, int, float o str)"
            ],
            "ejercicios_evaluacion": [
                "Crea un programa que convierta un número entero en un número decimal",
                "Haz un programa que guarde un valor booleano y lo imprima",
                "Escribe un programa que pida al usuario un número entero y lo multiplique por 10",
                "Crea un programa que compare dos números y muestre si son iguales",
                "Haz un programa que combine un texto y un número en un solo mensaje e imprímelo",
                "Escribe un programa que calcule el módulo (resto) de dos números",
                "Haz un programa que evalúe si un número es mayor que otro y muestre el resultado",
                "Escribe un programa que use operadores lógicos para verificar si un número es positivo y menor que 100"
            ]
        }
    },
    2: {
        "titulo": "Control de Flujo",
        "contenido": {
            "explicacion": "Los condicionales permiten decidir qué código ejecutar...",
            "ejercicios_practica": [
                "Escribe un programa que pida un número y diga si es positivo",
                "Haz un programa que pida un número y muestre si es par o impar",
                "Crea un programa que pida un número y diga si es mayor, menor o igual a 10",
                "Haz un programa que muestre los números del 1 al 5 usando un bucle for",
                "Escribe un programa que muestre los números del 1 al 5 usando un bucle while"
            ],
            "ejercicios_evaluacion": [
                "Haz un programa que sume los números del 1 al 10 usando un bucle for",
                "Escribe un programa que pida números al usuario hasta que introduzca un cero",
                "Crea un programa que muestre los números del 1 al 10, pero que se salte el 5 usando continue",
                "Haz un programa que muestre los números del 1 al 10 y que se detenga al llegar al 7 usando break",
                "Escribe un programa que use pass dentro de una estructura condicional",
                "Haz un programa que pida un número y diga si está entre 1 y 100",
                "Escribe un programa que muestre los números pares entre 1 y 20",
                "Crea un programa que pida números al usuario y muestre la suma total cuando introduzca un número negativo"
            ]
        }
    },
    

    3: {
        "titulo": "Estructuras de Datos Básicas",
        "contenido": {
            "explicacion": "Las estructuras de datos permiten organizar y almacenar información de manera eficiente...",
            "ejercicios_practica": [
                "Crea un programa que guarde una lista de tres frutas y la imprima",
                "Haz un programa que guarde una tupla con tres números y los muestre",
                "Escribe un programa que imprima el primer y último elemento de una lista",
                "Crea un programa que agregue un elemento al final de una lista y la imprima",
                "Haz un programa que elimine un elemento específico de una lista y la imprima"
            ],
            "ejercicios_evaluacion": [
                "Escribe un programa que cuente cuántas veces aparece un valor en una lista",
                "Haz un programa que ordene una lista de números y la imprima",
                "Crea un programa que muestre las claves de un diccionario",
                "Haz un programa que guarde un diccionario con datos de una persona (nombre, edad) y los muestre",
                "Escribe un programa que busque un valor en un diccionario y diga si existe",
                "Crea un programa que agregue un elemento a un conjunto y lo muestre",
                "Haz un programa que elimine un elemento de un conjunto y lo muestre",
                "Escribe un programa que muestre la unión de dos conjuntos"
            ]
        }
    },
    4: {
        "titulo": "Funciones",
        "contenido": {
            "explicacion": "Las funciones son bloques de código reutilizables que realizan tareas específicas...",
            "ejercicios_practica": [
                "Define una función que imprima un saludo",
                "Crea una función que reciba un nombre y lo imprima",
                "Escribe una función que sume dos números y devuelva el resultado",
                "Crea una función que devuelva el mayor de dos números",
                "Haz una función que reciba una lista y devuelva su longitud"
            ],
            "ejercicios_evaluacion": [
                "Escribe una función con un parámetro por defecto",
                "Crea una función que acepte cualquier número de argumentos y los sume",
                "Haz una función que reciba argumentos nombrados y los muestre",
                "Escribe una función que devuelva varios valores (por ejemplo, suma y producto)",
                "Crea una función dentro de otra y llama a la función interna",
                "Haz una función que modifique una variable global",
                "Crea una función recursiva que calcule el factorial de un número",
                "Escribe una función que reciba una lista de funciones y las ejecute todas"
            ]
        }
    },
    5: {
        "titulo": "Módulos y Paquetes",
        "contenido": {
            "explicacion": "Los módulos permiten organizar el código en archivos separados y reutilizables...",
            "ejercicios_practica": [
                "Importa el módulo math y muestra el valor de pi",
                "Usa from math import sqrt y calcula la raíz de un número",
                "Importa un módulo hecho por ti y llama una función",
                "Crea un archivo con una función y úsalo como módulo",
                "Crea un paquete con un módulo y úsalo en otro archivo"
            ],
            "ejercicios_evaluacion": [
                "Importa un módulo con un alias y úsalo",
                "Importa varias funciones de un módulo y úsalas",
                "Haz un módulo con varias funciones y pruébalas en otro archivo",
                "Crea un paquete que tenga subpaquetes",
                "Usa __init__.py para importar algo automáticamente al importar el paquente",
                "Haz un módulo que lea un archivo y lo importe desde otro",
                "Crea un paquete que use módulos de otros paquetes",
                "Haz un paquete y súbelo a un repositorio (ejercicio conceptual)"
            ]
        }
    },
    6: {
        "titulo": "Manejo de Archivos",
        "contenido": {
            "explicacion": "Python permite trabajar con diferentes tipos de archivos para almacenar y recuperar datos...",
            "ejercicios_practica": [
                "Crea un archivo .txt y escribe un mensaje",
                "Abre un archivo .txt y muestra su contenido",
                "Escribe varias líneas en un archivo",
                "Lee un archivo línea por línea",
                "Escribe un archivo sin borrar su contenido previo"
            ],
            "ejercicios_evaluacion": [
                "Lee un archivo y cuenta cuántas líneas tiene",
                "Escribe un archivo .csv con tres filas de datos",
                "Lee un archivo .csv y muestra los datos",
                "Escribe un archivo .json con un diccionario",
                "Lee un archivo .json y muestra los valores",
                "Copia el contenido de un archivo a otro",
                "Lee un archivo y busca una palabra específica",
                "Escribe un archivo donde el usuario ingrese los datos"
            ]
        }
    },
    7: {
        "titulo": "Programación Orientada a Objetos (POO)",
        "contenido": {
            "explicacion": "La POO permite modelar objetos del mundo real con clases que contienen atributos y métodos...",
            "ejercicios_practica": [
                "Define una clase Animal con un método que diga 'soy un animal'",
                "Crea un objeto de la clase Animal y llama al método",
                "Define una clase Persona con nombre y edad",
                "Agrega un método a Persona que imprima sus datos",
                "Haz una clase que herede de Persona y agregue un atributo"
            ],
            "ejercicios_evaluacion": [
                "Crea un método __str__ que muestre los datos de un objeto",
                "Haz una clase con un atributo privado",
                "Define un método que cambie el valor de un atributo privado",
                "Crea dos clases distintas con un método que tenga el mismo nombre y diferente comportamiento",
                "Crea una clase con un método que devuelva su longitud (con __len__)",
                "Haz una clase que cree una lista de objetos",
                "Crea una jerarquía de clases con herencia múltiple",
                "Implementa un ejemplo de polimorfismo con varias clases"
            ]
        }
    },
    8: {
        "titulo": "Excepciones",
        "contenido": {
            "explicacion": "El manejo de excepciones permite controlar errores y mantener el programa funcionando...",
            "ejercicios_practica": [
                "Haz un programa que divida dos números y capture si el divisor es cero",
                "Intenta convertir un texto en número y captura el error si falla",
                "Usa finally para imprimir un mensaje al final del intento",
                "Lanza un error si un número es negativo usando raise",
                "Haz un try-except con varios tipos de errores distintos"
            ],
            "ejercicios_evaluacion": [
                "Escribe un programa que intente abrir un archivo y capture si no existe",
                "Crea una función que use try-except y retorne un valor por defecto si hay error",
                "Anida un try dentro de otro try",
                "Usa else en un bloque de excepciones",
                "Captura errores en la lectura de un archivo .json inválido",
                "Lanza un error personalizado con un mensaje",
                "Haz un programa que capture excepciones dentro de un bucle",
                "Combina try, except, else y finally en un solo ejemplo"
            ]
        }
    },
    9: {
        "titulo": "Expresiones Lambda y Funciones de Orden Superior",
        "contenido": {
            "explicacion": "Las lambdas son funciones anónimas y las funciones de orden superior trabajan con otras funciones...",
            "ejercicios_practica": [
                "Haz una función lambda que sume dos números",
                "Usa lambda para elevar un número al cubo",
                "Usa map para convertir una lista de números en sus cuadrados",
                "Usa filter para sacar los números pares de una lista",
                "Usa reduce para multiplicar todos los elementos de una lista"
            ],
            "ejercicios_evaluacion": [
                "Haz una función que reciba una lista y una función y aplique map",
                "Combina filter y map en una lista de números",
                "Usa lambda con sorted para ordenar una lista de tuplas por el segundo elemento",
                "Usa reduce para sumar los elementos de una lista",
                "Usa lambda para filtrar una lista de cadenas con más de 3 letras",
                "Haz un map que convierta números a cadenas",
                "Haz un filter que elimine los elementos None de una lista",
                "Haz un reduce que construya una cadena concatenando una lista de palabras"
            ]
        }
    },
    10: {
        "titulo": "Generadores e Iteradores",
        "contenido": {
            "explicacion": "Los generadores producen valores uno a uno, ahorrando memoria...",
            "ejercicios_practica": [
                "Crea un generador que devuelva números del 1 al 5",
                "Haz un generador que devuelva los cuadrados de los números",
                "Haz un generador que devuelva letras de una palabra",
                "Haz un generador infinito que devuelva números empezando en 1",
                "Haz un iterador que devuelva los números de una lista uno a uno"
            ],
            "ejercicios_evaluacion": [
                "Haz un generador que devuelva los números pares hasta un límite",
                "Haz un generador que devuelva una secuencia Fibonacci hasta un límite",
                "Haz un iterador que devuelva caracteres de una cadena en orden inverso",
                "Haz un generador que devuelva solo los números primos hasta un límite",
                "Haz un generador que devuelva números en orden descendente",
                "Haz un iterador que devuelva el doble de cada número en una lista",
                "Haz un generador que devuelva combinaciones de dos listas",
                "Haz un iterador que devuelva letras mayúsculas de una palabra"
            ]
        }
    },
    11: {
        "titulo": "Decoradores",
        "contenido": {
            "explicacion": "Los decoradores modifican o extienden el comportamiento de funciones sin cambiar su código...",
            "ejercicios_practica": [
                "Haz un decorador que imprima 'Inicio' antes de llamar a la función",
                "Crea un decorador que muestre el tiempo de ejecución de una función",
                "Haz un decorador que imprima el nombre de la función que se llama",
                "Haz un decorador que ejecute una función dos veces",
                "Crea un decorador que cuente cuántas veces se ha llamado la función"
            ],
            "ejercicios_evaluacion": [
                "Haz un decorador que agregue un texto antes y después de la función",
                "Haz un decorador con parámetros",
                "Combina dos decoradores en una función",
                "Haz un decorador que capture excepciones dentro de la función",
                "Haz un decorador que modifique el valor retornado por la función",
                "Haz un decorador que registre en un archivo cada llamada a la función",
                "Haz un decorador que cambie los argumentos de la función antes de llamarla",
                "Haz un decorador que solo permita ejecutar la función un número limitado de veces"
            ]
        }
    },
    12: {
        "titulo": "Manejo de Fechas y Tiempo",
        "contenido": {
            "explicacion": "Python ofrece módulos para trabajar con fechas, horas y medir tiempos de ejecución...",
            "ejercicios_practica": [
                "Muestra la fecha y hora actual",
                "Convierte una fecha en string a un objeto datetime",
                "Calcula la diferencia entre dos fechas",
                "Muestra solo la hora actual",
                "Muestra la fecha de mañana"
            ],
            "ejercicios_evaluacion": [
                "Muestra el día de la semana actual",
                "Convierte una fecha a otro formato de string",
                "Calcula cuántos días faltan para una fecha dada",
                "Mide el tiempo que tarda en ejecutarse una operación",
                "Muestra la hora en formato de 12 horas",
                "Agrega 5 días a una fecha dada",
                "Resta 2 horas a una fecha dada",
                "Crea un programa que muestre la fecha en un formato personalizado"
            ]
        }
    },
    13: {
        "titulo": "Expresiones Regulares",
        "contenido": {
            "explicacion": "Las expresiones regulares permiten buscar y manipular textos con patrones complejos...",
            "ejercicios_practica": [
                "Busca un número en un texto",
                "Encuentra todas las palabras en un texto",
                "Busca un email en un texto",
                "Reemplaza los números de un texto por #",
                "Encuentra palabras que empiecen con mayúscula"
            ],
            "ejercicios_evaluacion": [
                "Valida si un texto es un número entero",
                "Busca fechas en formato dd/mm/yyyy",
                "Encuentra palabras que terminen en ar",
                "Separa un texto en palabras",
                "Busca códigos postales de 5 dígitos en un texto",
                "Reemplaza todos los espacios dobles por uno solo",
                "Busca palabras con más de 5 letras",
                "Valida un número de teléfono con un formato específico"
            ]
        }
    },
    14: {
        "titulo": "Programación Concurrente",
        "contenido": {
            "explicacion": "La programación concurrente permite ejecutar múltiples tareas simultáneamente...",
            "ejercicios_practica": [
                "Crea un hilo que imprima un mensaje",
                "Crea dos hilos que impriman mensajes distintos",
                "Mide el tiempo de ejecución de dos hilos",
                "Crea un proceso que calcule la suma de una lista",
                "Crea varios procesos que hagan distintas tareas"
            ],
            "ejercicios_evaluacion": [
                "Usa threading para imprimir números en paralelo",
                "Crea un proceso que escriba en un archivo",
                "Crea hilos que sumen distintas partes de una lista",
                "Crea un proceso que espere un segundo antes de imprimir",
                "Lanza 10 hilos y espera a que terminen",
                "Haz un proceso que devuelva un resultado al proceso principal",
                "Combina hilos y procesos en el mismo programa",
                "Haz un programa que use un lock para evitar que dos hilos escriban a la vez"
            ]
        }
    },
    15: {
        "titulo": "Programación Asíncrona",
        "contenido": {
            "explicacion": "La programación asíncrona permite manejar operaciones de E/S sin bloquear el programa...",
            "ejercicios_practica": [
                "Crea una función asíncrona que imprima un mensaje",
                "Llama dos funciones asíncronas y haz que se ejecuten al mismo tiempo",
                "Haz que una función espere un segundo antes de continuar",
                "Usa await para esperar el resultado de otra función",
                "Haz un programa asíncrono que simule una descarga"
            ],
            "ejercicios_evaluacion": [
                "Crea varias tareas asíncronas y ejecútalas juntas",
                "Usa asyncio.gather para ejecutar varias funciones a la vez",
                "Mide el tiempo de ejecución de funciones asíncronas",
                "Haz una función asíncrona que devuelva un valor",
                "Usa asyncio.sleep para pausar una función",
                "Haz un bucle que llame funciones asíncronas repetidamente",
                "Haz un programa que use asyncio.run para iniciar",
                "Combina funciones normales y asíncronas en un mismo programa"
            ]
        }
    },
    16: {
        "titulo": "Serialización de Datos",
        "contenido": {
            "explicacion": "La serialización convierte objetos en formatos almacenables o transmitibles...",
            "ejercicios_practica": [
                "Serializa un diccionario usando json y guárdalo en un archivo",
                "Deserializa un archivo json y muestra su contenido",
                "Serializa una lista con pickle",
                "Deserializa un archivo pickle y úsalo en el programa",
                "Serializa un diccionario con listas como valores usando json"
            ],
            "ejercicios_evaluacion": [
                "Guarda un objeto complejo (por ejemplo, un diccionario con listas y otros diccionarios) en pickle",
                "Convierte un objeto de Python a json y muestra la cadena resultante",
                "Lee una cadena en json y conviértela a un diccionario",
                "Serializa datos usando json y envíalos por consola",
                "Lee un archivo json, modifica un valor y vuelve a guardarlo",
                "Serializa un conjunto usando pickle",
                "Deserializa un archivo binario y muestra un atributo de un objeto",
                "Haz un programa que detecte si un archivo serializado existe y lo cargue o lo cree"
            ]
        }
    },
    17: {
        "titulo": "Bases de Datos",
        "contenido": {
            "explicacion": "Las bases de datos permiten almacenar y consultar información de manera estructurada...",
            "ejercicios_practica": [
                "Conéctate a una base de datos SQLite",
                "Crea una tabla llamada usuarios con columnas id y nombre",
                "Inserta un usuario en la tabla",
                "Consulta todos los usuarios de la tabla y muéstralos",
                "Actualiza el nombre de un usuario"
            ],
            "ejercicios_evaluacion": [
                "Elimina un usuario de la tabla",
                "Haz una consulta con un filtro (por ejemplo, nombre = 'Ana')",
                "Crea una base de datos en memoria (sin archivo)",
                "Usa un try-except para capturar errores de la base de datos",
                "Crea un modelo de usuario con SQLAlchemy",
                "Inserta datos en la base de datos usando un modelo",
                "Consulta con SQLAlchemy y muestra los resultados",
                "Haz una relación entre dos tablas con SQLAlchemy (usuarios y direcciones)"
            ]
        }
    },
    18: {
        "titulo": "Pruebas y Debugging",
        "contenido": {
            "explicacion": "Las pruebas automatizadas y el debugging son esenciales para desarrollar software robusto...",
            "ejercicios_practica": [
                "Haz un test para comprobar que una función suma bien",
                "Escribe una prueba que falle y corrige el error",
                "Usa unittest para comprobar que una lista contiene un valor",
                "Haz una prueba que compruebe que una cadena empieza con cierta letra",
                "Escribe una prueba con varios casos de entrada"
            ],
            "ejercicios_evaluacion": [
                "Haz un test que verifique que un diccionario tiene cierta clave",
                "Usa pytest para probar una función que devuelve un valor booleano",
                "Usa pdb para depurar una función que no devuelve lo esperado",
                "Coloca un punto de interrupción y examina el valor de una variable",
                "Haz una prueba que capture una excepción esperada",
                "Combina varias pruebas en un solo archivo de unittest",
                "Haz una prueba que verifique el tipo de un valor",
                "Usa pdb para recorrer paso a paso un bucle"
            ]
        }
    },
    19: {
        "titulo": "Metaprogramación",
        "contenido": {
            "explicacion": "La metaprogramación permite crear o modificar código durante la ejecución del programa...",
            "ejercicios_practica": [
                "Crea una clase usando type dinámicamente",
                "Haz una metaclase que imprima un mensaje al crear una clase",
                "Usa getattr para obtener un atributo de un objeto dinámicamente",
                "Usa setattr para crear un nuevo atributo en un objeto",
                "Haz una función que recorra los atributos de un objeto y los imprima"
            ],
            "ejercicios_evaluacion": [
                "Crea un método dinámicamente y asígnalo a una clase",
                "Haz un decorador que modifique el nombre de una función",
                "Usa hasattr para comprobar si un objeto tiene un atributo",
                "Haz una metaclase que agregue un método a las clases que crea",
                "Usa dir para listar todos los atributos de un objeto",
                "Crea un decorador que agregue un atributo a una función",
                "Haz una función que cree clases dinámicamente con diferentes atributos",
                "Haz un programa que cambie un método de una clase en tiempo de ejecución"
            ]
        }
    },





    20: {
        "titulo": "Optimización y C Extensions",
        "contenido": {
            "explicacion": "Puedes medir y mejorar el rendimiento de un programa...",
            "ejercicios_practica": [
                "Usa timeit para medir el tiempo de una operación simple",
                "Usa cProfile para medir el tiempo de ejecución de una función",
                "Compara el tiempo de una lista por comprensión y un bucle for",
                "Mide cuánto tarda en ejecutarse una suma de una lista grande",
                "Haz un programa que optimice una operación lenta"
            ],
            "ejercicios_evaluacion": [
                "Escribe un módulo con Cython (conceptual si no tienes entorno C)",
                "Llama a una función escrita en C usando ctypes",
                "Haz un programa que muestre qué función tarda más usando cProfile",
                "Optimiza una función cambiando un bucle por una expresión generadora",
                "Haz un test para comparar dos formas de hacer lo mismo y medir cuál es más rápida",
                "Llama a una función de una biblioteca C estándar con ctypes",
                "Usa timeit para comparar el tiempo de ejecución de map y un bucle",
                "Haz un perfilado de un programa con varias funciones"
            ]
        }
    }
}








# Rutas principales
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('perfil'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT username FROM users 
                WHERE username = ? AND password = ?
            """, (username, password))
            
            if cursor.fetchone():
                session['username'] = username
                return redirect(url_for('perfil'))
            else:
                flash("Usuario o contraseña incorrectos")
                return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        cedula = request.form.get('cedula')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash("Las contraseñas no coinciden")
            return redirect(url_for('register'))

        try:
            with sqlite3.connect('database.db') as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO users (username, cedula, password)
                    VALUES (?, ?, ?)
                """, (username, cedula, password))
                conn.commit()

            session['temp_username'] = username
            return redirect(url_for('cuestionario_inicial', username=username))

        except sqlite3.IntegrityError:
            flash("El usuario o cédula ya están registrados")
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/cuestionario_inicial/<username>', methods=['GET', 'POST'])
def cuestionario_inicial(username):
    # Verificar que el usuario temporal coincide
    if 'temp_username' not in session or session['temp_username'] != username:
        return redirect(url_for('register'))

    if request.method == 'POST':
        nivel_actual = int(request.form.get('nivel', 1))
        respuesta_usuario = request.form.get('respuesta', '').strip().lower()
        respuesta_correcta = preguntas[nivel_actual-1]["respuesta"]

        if respuesta_usuario == respuesta_correcta:
            if nivel_actual == len(preguntas):
                # Completó todas las preguntas
                with sqlite3.connect('database.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE users 
                        SET nivel = ?, registro_completo = TRUE 
                        WHERE username = ?
                    """, (nivel_actual, username))
                    conn.commit()

                session['username'] = username
                session.pop('temp_username', None)
                return redirect(url_for('perfil'))
            else:
                # Pasar a la siguiente pregunta
                return render_template('cuestionario.html',
                                    pregunta=preguntas[nivel_actual]["pregunta"],
                                    nivel=nivel_actual+1,
                                    total_preguntas=len(preguntas))
        else:
            # Respuesta incorrecta - guardar progreso
            with sqlite3.connect('database.db') as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE users 
                    SET nivel = ? 
                    WHERE username = ?
                """, (nivel_actual-1, username))
                conn.commit()

            return render_template('final_cuestionario.html',
                                nivel=nivel_actual-1,
                                mensaje="¡Buen intento! Ahora puedes iniciar sesión")

    # Primera pregunta
    return render_template('cuestionario.html',
                         pregunta=preguntas[0]["pregunta"],
                         nivel=1,
                         total_preguntas=len(preguntas))

@app.route('/perfil')
def perfil():
    if 'username' not in session:
        return redirect(url_for('login'))

    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT username, nivel, foto, descripcion, 
                   año_nacimiento, carrera, año_carrera, lenguajes 
            FROM users 
            WHERE username = ?
        """, (session['username'],))
        user_data = cursor.fetchone()

    if not user_data:
        session.clear()
        return redirect(url_for('login'))

    return render_template('perfil.html',
                         username=user_data[0],
                         nivel=user_data[1],
                         foto=user_data[2],
                         descripcion=user_data[3],
                         año_nacimiento=user_data[4],
                         carrera=user_data[5],
                         año_carrera=user_data[6],
                         lenguajes=user_data[7])




@app.route('/actualizar_perfil', methods=['POST'])
def actualizar_perfil():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Obtener datos del formulario
    username = request.form.get('username')
    descripcion = request.form.get('descripcion', '')
    año_nacimiento = request.form.get('año_nacimiento', '')
    carrera = request.form.get('carrera', '')
    año_carrera = request.form.get('año_carrera', 1)
    lenguajes = request.form.get('lenguajes', '')
    
    # Manejar la foto
    foto = None
    if 'foto' in request.files:
        file = request.files['foto']
        if file.filename != '' and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            extension = filename.rsplit('.', 1)[1].lower()
            new_filename = f"{session['username']}.{extension}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
            foto = new_filename

    # Actualizar en la base de datos
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        if foto:
            cursor.execute("""
                UPDATE users SET
                username = ?,
                descripcion = ?,
                año_nacimiento = ?,
                carrera = ?,
                año_carrera = ?,
                lenguajes = ?,
                foto = ?
                WHERE username = ?
            """, (username, descripcion, año_nacimiento, carrera, año_carrera, lenguajes, foto, session['username']))
        else:
            cursor.execute("""
                UPDATE users SET
                username = ?,
                descripcion = ?,
                año_nacimiento = ?,
                carrera = ?,
                año_carrera = ?,
                lenguajes = ?
                WHERE username = ?
            """, (username, descripcion, año_nacimiento, carrera, año_carrera, lenguajes, session['username']))
        conn.commit()

    session['username'] = username
    return redirect(url_for('perfil'))




@app.route('/editar_perfil', methods=['GET', 'POST'])
def editar_perfil():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Procesar actualización del perfil
        username = request.form.get('username')
        descripcion = request.form.get('descripcion', '')
        año_nacimiento = request.form.get('año_nacimiento', '')
        carrera = request.form.get('carrera', '')
        año_carrera = request.form.get('año_carrera', 1)
        lenguajes = request.form.get('lenguajes', '')
        
        # Manejar la foto de perfil
        foto = None
        if 'foto' in request.files:
            file = request.files['foto']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                extension = filename.rsplit('.', 1)[1].lower()
                new_filename = f"{session['username']}.{extension}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
                foto = new_filename

        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            if foto:
                cursor.execute("""
                    UPDATE users SET
                    username = ?,
                    descripcion = ?,
                    año_nacimiento = ?,
                    carrera = ?,
                    año_carrera = ?,
                    lenguajes = ?,
                    foto = ?
                    WHERE username = ?
                """, (username, descripcion, año_nacimiento, carrera, 
                      año_carrera, lenguajes, foto, session['username']))
            else:
                cursor.execute("""
                    UPDATE users SET
                    username = ?,
                    descripcion = ?,
                    año_nacimiento = ?,
                    carrera = ?,
                    año_carrera = ?,
                    lenguajes = ?
                    WHERE username = ?
                """, (username, descripcion, año_nacimiento, carrera,
                      año_carrera, lenguajes, session['username']))
            conn.commit()

        session['username'] = username
        return redirect(url_for('perfil'))

    # Mostrar formulario de edición
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT username, foto, descripcion, año_nacimiento, 
                   carrera, año_carrera, lenguajes 
            FROM users 
            WHERE username = ?
        """, (session['username'],))
        user_data = cursor.fetchone()

    return render_template('editar_perfil.html',
                         username=user_data[0],
                         foto=user_data[1],
                         descripcion=user_data[2],
                         año_nacimiento=user_data[3],
                         carrera=user_data[4],
                         año_carrera=user_data[5],
                         lenguajes=user_data[6])

@app.route('/amigos')
def amigos():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Obtener ID del usuario actual
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ?", (session['username'],))
        user_id = cursor.fetchone()[0]
        session['user_id'] = user_id  # Guardamos el ID en la sesión

        # Obtener lista de todos los usuarios (excepto yo)
        cursor.execute("SELECT id, username FROM users WHERE id != ?", (user_id,))
        usuarios = [{'id': row[0], 'username': row[1]} for row in cursor.fetchall()]

    return render_template('amigos.html', usuarios=usuarios)

@app.route('/obtener_mensajes')
def obtener_mensajes():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    destinatario_id = request.args.get('destinatario_id')
    
    with sqlite3.connect('database.db') as conn:
        conn.row_factory = sqlite3.Row  # Para acceder a las columnas por nombre
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT m.*, u.username 
            FROM mensajes m
            JOIN users u ON m.remitente_id = u.id
            WHERE (m.remitente_id = ? AND m.destinatario_id = ?)
               OR (m.remitente_id = ? AND m.destinatario_id = ?)
            ORDER BY m.fecha
        """, (session['user_id'], destinatario_id, destinatario_id, session['user_id']))
        
        mensajes = []
        for row in cursor.fetchall():
            mensajes.append({
                'remitente_id': row['remitente_id'],
                'mensaje': row['mensaje'],
                'username': row['username']
            })

    return jsonify(mensajes)

@app.route('/enviar_mensaje', methods=['POST'])
def enviar_mensaje():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    data = request.get_json()  # Cambiado a get_json() para mejor manejo
    
    if not data or 'destinatario_id' not in data or 'mensaje' not in data:
        return jsonify({'success': False, 'error': 'Datos inválidos'}), 400

    try:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO mensajes (remitente_id, destinatario_id, mensaje)
                VALUES (?, ?, ?)
            """, (session['user_id'], data['destinatario_id'], data['mensaje']))
            conn.commit()

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500





@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))



@app.route('/estudiar')
def estudiar():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT nivel FROM users WHERE username = ?", (session['username'],))
        nivel_actual = cursor.fetchone()[0]
    
    return render_template('estudiar.html', nivel_actual=nivel_actual, lecciones=LECCIONES)

@app.route('/leccion/<int:nivel>')
def leccion(nivel):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT nivel FROM users WHERE username = ?", (session['username'],))
        nivel_actual = cursor.fetchone()[0]
    
    if nivel > nivel_actual + 1:
        flash("Debes completar el nivel anterior primero")
        return redirect(url_for('estudiar'))
    
    if nivel not in LECCIONES:
        flash("Lección no disponible")
        return redirect(url_for('estudiar'))
    
    return render_template('leccion.html', 
                         leccion=LECCIONES[nivel],
                         nivel=nivel,
                         nivel_actual=nivel_actual)

@app.route('/completar_leccion/<int:nivel>', methods=['POST'])
def completar_leccion(nivel):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    respuestas_correctas = 0
    total_ejercicios = 8  # Ajusta según tus necesidades
    
    for i in range(1, total_ejercicios + 1):
        respuesta = request.form.get(f'respuesta_{i}', '').strip()
        if Evaluador.evaluar(nivel, i, respuesta):
            respuestas_correctas += 1
    
    if respuestas_correctas >= 6:  # Umbral para aprobar
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET nivel = ? WHERE username = ?", 
                         (nivel, session['username']))
            conn.commit()
        flash(f"✅ ¡Aprobado! ({respuestas_correctas}/{total_ejercicios} correctos)", 'success')
    else:
        flash(f"❌ Reprueba ({respuestas_correctas}/{total_ejercicios} correctos)", 'error')
    
    return redirect(url_for('estudiar'))



# Añade estas rutas nuevas
@app.route('/leccion/<int:nivel>/teoria')
def teoria(nivel):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT nivel FROM users WHERE username = ?", (session['username'],))
        nivel_actual = cursor.fetchone()[0]
    
    if nivel > nivel_actual + 1:
        flash("Debes completar el nivel anterior primero")
        return redirect(url_for('estudiar'))
    
    return render_template('teoria.html', 
                         leccion=LECCIONES[nivel],
                         nivel=nivel,
                         nivel_actual=nivel_actual)

@app.route('/leccion/<int:nivel>/practica', methods=['GET', 'POST'])
def practica(nivel):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Lógica para verificar respuestas de práctica
        ejercicios_correctos = 0
        for i in range(1, 6):  # 5 ejercicios de práctica
            respuesta = request.form.get(f'ejercicio_{i}', '')
            if Evaluador.evaluar_practica(nivel, i, respuesta):
                ejercicios_correctos += 1
        
        if ejercicios_correctos == 5:
            return redirect(url_for('evaluacion', nivel=nivel))
        else:
            flash(f"Tienes {ejercicios_correctos}/5 correctos. ¡Inténtalo de nuevo!")
            return redirect(url_for('practica', nivel=nivel))
    
    return render_template('practica.html',
                         leccion=LECCIONES[nivel],
                         nivel=nivel)

@app.route('/leccion/<int:nivel>/evaluacion', methods=['GET', 'POST'])
def evaluacion(nivel):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        respuestas_correctas = 0
        for i in range(1, 9):  # 8 ejercicios de evaluación
            respuesta = request.form.get(f'ejercicio_{i}', '')
            if Evaluador.evaluar_ejercicio(nivel, i, respuesta):
                respuestas_correctas += 1
        
        if respuestas_correctas >= 6:
            with sqlite3.connect('database.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET nivel = ? WHERE username = ?", 
                             (nivel + 1, session['username']))
                conn.commit()
            flash(f"¡Felicidades! Pasaste al nivel {nivel + 1} ({respuestas_correctas}/8 correctos)")
            return redirect(url_for('estudiar'))
        else:
            flash(f"Necesitas al menos 6/8 correctos. Tienes {respuestas_correctas}/8")
            return redirect(url_for('evaluacion', nivel=nivel))
    
    return render_template('evaluacion.html',
                         leccion=LECCIONES[nivel],
                         nivel=nivel)



# Manejo de conexiones WebSocket
@socketio.on('connect')
def handle_connect():
    if 'username' in session:
        emit('online', {'username': session['username']}, broadcast=True)

@socketio.on('nuevo_mensaje')
def handle_message(data):
    # Guardar en BD (opcional)
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO mensajes (remitente_id, destinatario_id, mensaje)
            VALUES (?, ?, ?)
        """, (session['user_id'], data['destinatario_id'], data['mensaje']))
        conn.commit()
    
    # Enviar a los usuarios afectados
    emit('recibir_mensaje', {
        'remitente_id': session['user_id'],
        'destinatario_id': data['destinatario_id'],
        'mensaje': data['mensaje'],
        'username': session['username']
    }, broadcast=True)




if __name__ == '__main__':
    init_db()
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    socketio.run(app, host='0.0.0.0', debug=True)