import os
import sys  # Import sin usar que Ruff debería marcar


def mi_funcion_fea(variable_uno, variable_dos):
    print("hola")
    x = 5  # Variable sin usar


""" Codigo con errores de formato y variables sin usar para que Ruff los marque y black los corrija. 
import os
import sys  # Import sin usar que Ruff debería marcar


def mi_funcion_fea(   variable_uno,variable_dos   ):
      print(  "hola" )
      x = 5 # Variable sin usar """
