"""Collection of methods that are used as command line scripts
"""

import click
import os
import frontur_utilities.utility_fileloader as df_fileloader
import frontur_utilities.constants as const
import frontur_utilities.extract_methods as em


@click.group()
def cli():
    """Method that can be called my other modules to use the commands on this file"""
    pass


@cli.command('cli', short_help='command line interface', context_settings={"ignore_unknown_options": True})
@click.option('-i', '--infile', prompt='FronTur file', type=click.Path(exists=True), help='Path to file with FronTur flights.')
@click.option('-o', '--outfile', type=click.Path(), help='Output path with parsed FronTur flights.')
@click.option('-d', '--days', prompt='Days json file', type=click.Path(exists=True), help='Path to json file with correct parameters.')
@click.option('-a', '--airport', prompt='Select airport', type=click.STRING, help='Target airport string identifier code.')
@click.option('-s', '--substitutions', default='.', type=click.Path(exists=True), help='Optional json file with value conversions.')
def command(infile: str, days: str, airport: str, substitutions: str, outfile: str):
    """
    ·______   ______     ______     __   __     ______   __  __     ______   
    /\  ___\ /\  == \   /\  __ \   /\ "-.\ \   /\__  _\ /\ \/\ \   /\  == \  
    \ \  __\ \ \  __<   \ \ \/\ \  \ \ \-.  \  \/_/\ \/ \ \ \_\ \  \ \  __<  
    ·\ \_\    \ \_\ \_\  \ \_____\  \ \_\\\\"\_\    \ \_\  \ \_____\  \ \_\ \_\\
    ··\/_/     \/_/ /_/   \/_____/   \/_/ \/_/     \/_/   \/_____/   \/_/ /_/


    Program that processes various information from files
    giving a dataframe with concrete information about flights.
    \f
    Args:
        infile (str): Path to file with FronTur flights
        days (str): Path to json file with correct parameters of the assigned interview days
        airport (str): Target airport string identifier code
        substitutions (str): Optional json file with value conversions
        outfile (str): Output path with parsed FronTur flights
    """
    data_frame = df_fileloader.load_agenda(infile)
    data_frame = em.select_airport(data_frame, airport)

    if substitutions != '.':
        em.substitute_values(data_frame, substitutions)

    data_frame = em.add_plane_data(data_frame, const.PLANES_DATA_FILE_PATH)
    data_frame = em.format_dates(data_frame)
    data_frame = em.select_days(data_frame, days)

    print(
        data_frame,
        '\n-------------\n',
        data_frame.groupby(['Destino']).sum(),
        '\n-------------\n',
        data_frame.groupby(['Pais']).sum()
    )

    if outfile:
        df_fileloader.dump_agenda(outfile, data_frame)


@cli.command('edit_conf', short_help='cofiguration file edition shortcut')
@click.option('-e', '--editor', type=click.STRING, default='', help='Alternative file editor.')
def edit_conf(editor: str):
    abs_path = os.path.dirname(os.path.realpath(__file__))
    if editor == '':
        os.startfile(abs_path + '/data/config.json')
    else:
        os.system(editor + ' ' + abs_path + '/data/config.json')
