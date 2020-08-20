import click
import df_utilities

if __name__ == "__main__":
    click.CommandCollection(sources=[df_utilities.commands.cli])()