import ast
import re
import subprocess
import tempfile
import os
from functools import lru_cache

class Evaluador:
    @staticmethod
    def limpiar_codigo(codigo):
        """Elimina elementos peligrosos y normaliza el código"""
        # Lista negra de operaciones peligrosas
        peligrosos = [
            'import os', 'import sys', 'subprocess', 'open(', 
            '__import__', 'eval(', 'exec(', 'breakpoint()',
            'while True', 'for _ in iter(int, 1)'
        ]
        
        for peligro in peligrosos:
            if peligro in codigo:
                return None
        
        return re.sub(r'\s+|#.*', '', codigo.lower())

    @staticmethod
    def verificar_sintaxis(codigo):
        """Verifica que el código sea sintácticamente correcto"""
        try:
            ast.parse(codigo)
            return True
        except SyntaxError:
            return False

    @staticmethod
    @lru_cache(maxsize=100)
    def ejecutar_seguro(codigo, entrada=""):
        """Ejecuta código en un entorno seguro con timeout"""
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp:
                tmp.write(codigo)
                tmp_path = tmp.name
            
            resultado = subprocess.run(
                ['python', tmp_path],
                input=entrada,
                capture_output=True,
                text=True,
                timeout=3
            )
            os.unlink(tmp_path)
            return resultado.stdout.strip()
        except:
            return "ERROR"

    @classmethod
    def evaluar_practica(cls, nivel, ejercicio, codigo_usuario):
        """Evaluación para ejercicios de práctica (más permisiva)"""
        from respuestas import RESPUESTAS_PRACTICA
        criterios = RESPUESTAS_PRACTICA[nivel][ejercicio]
        
        # 1. Verificación básica de seguridad y sintaxis
        codigo_limpio = cls.limpiar_codigo(codigo_usuario)
        if not codigo_limpio or not cls.verificar_sintaxis(codigo_usuario):
            return False
        
        # 2. Verificación de patrones clave
        for patron in criterios.get('patrones', []):
            if not re.search(patron, codigo_limpio):
                return False
        
        return True

    @classmethod
    def evaluar_evaluacion(cls, nivel, ejercicio, codigo_usuario):
        """Evaluación estricta para evaluación final"""
        from respuestas import RESPUESTAS_EVALUACION
        criterios = RESPUESTAS_EVALUACION[nivel][ejercicio]
        
        # 1. Verificación de seguridad y sintaxis
        codigo_limpio = cls.limpiar_codigo(codigo_usuario)
        if not codigo_limpio or not cls.verificar_sintaxis(codigo_usuario):
            return False
        
        # 2. Verificación de patrones obligatorios
        for patron in criterios.get('patrones', []):
            if not re.search(patron, codigo_limpio):
                return False
        
        # 3. Verificación de salida exacta
        if 'salida' in criterios:
            salida = cls.ejecutar_seguro(
                codigo_usuario,
                criterios.get('entrada', '')
            )
            return salida == criterios['salida']
        
        return True