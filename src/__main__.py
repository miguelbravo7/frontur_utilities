import click

import os
os.environ["KCFG_KIVY_LOG_LEVEL"] = "warning"

import sys
sys.path.append(r'E:\DocumentosHDD\GitHub\TFG-Seleccion_de_Vuelos\src\TFG_Seleccion_de_Vuelos')

import df_utilities
import interface

if __name__ == "__main__":
    click.CommandCollection(sources=[df_utilities.commands.cli, interface.commands.cli])()