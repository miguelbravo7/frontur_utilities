import click
import frontur_utilities

if __name__ == "__main__":
    click.CommandCollection(sources=[frontur_utilities.commands.cli])()