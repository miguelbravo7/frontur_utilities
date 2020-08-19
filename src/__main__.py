import click

import sys
sys.path.append(r'E:\DocumentosHDD\GitHub\df_utilities\src')

import df_utilities

if __name__ == "__main__":
    click.CommandCollection(sources=[df_utilities.commands.cli])()