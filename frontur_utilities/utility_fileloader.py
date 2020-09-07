"""Utility to load and save dataframes easily
"""

import pandas
from chardet.universaldetector import UniversalDetector
from datetime import datetime
import frontur_utilities.constants as const
import frontur_utilities.utility_functions as uf


def load_agenda(
        file_path: str,
        date_format: str = const.DF_DATAFRAME_DAY_FORMAT
        ) -> pandas.DataFrame:
    """Loads a pandas Dataframe given a file
    checking if the extension is supported

    Args:
        file_path (str): Source file path
        date_format (str, optional): Format used on the dates.

    Raises:
        AttributeError: If the extension isn't supported

    Returns:
        pandas.DataFrame: Loaded DataFrame
    """
    extension = file_path.split('.')[-1]

    if extension not in const.SUPPORTED_EXTENSIONS:
        raise AttributeError(f'The file extention {extension} of file {file_path} is not supported.')

    def date_parser(x): pandas.datetime.strptime(x, date_format)

    data_frame = None
    if extension in const.SUPPORTED_EXCEL:
        data_frame = pandas.read_excel(file_path, date_parser=date_parser)
    elif extension in const.SUPPORTED_CSV:
        try:
            data_frame = pandas.read_csv(file_path, date_parser=date_parser)
        except UnicodeDecodeError:
            guessed_encoding = guess_encoding(open(file_path, 'rb'))
            uf.eprint("Decoding error using: utf-8\nAutomatic guess:", guessed_encoding)
            data_frame = pandas.read_csv(file_path, date_parser=date_parser, encoding=guessed_encoding)

    return data_frame


def save_agenda(
        file_path: str,
        data_frame: pandas.DataFrame,
        date_format: str = const.DF_DATAFRAME_DAY_FORMAT
        ):
    """Loads a pandas DataFrame object given a file
    and checking if its extension is supported

    Args:
        file_path (str): Target file path
        data_frame (pandas.DataFrame): Source DataFrame
        date_format (str, optional): Format used on the dates.

    Raises:
        AttributeError: If the file extension is not supported
    """
    extention = file_path.split('.')[-1]

    if extention not in const.SUPPORTED_EXTENSIONS:
        raise AttributeError(f'The file extension {extention} of file {file_path} is not supported.')

    data_frame = data_frame.applymap(lambda x: x.strftime(date_format) if isinstance(x, datetime) else x)

    if extention in const.SUPPORTED_EXCEL:
        data_frame.to_excel(file_path, index=False)
    elif extention in const.SUPPORTED_CSV:
        data_frame.to_csv(file_path, date_format=date_format, index=False, encoding='utf-16')


def guess_encoding(file_bytes: bytes) -> str:
    """Guesses the encoding as a string using the
    Universal Encoding Detector library incrementally
    calling its feed method repeatedly with each block of text

    Args:
        file_bytes (bytes): raw bytes

    Returns:
        str: Type of the encoding
    """
    detector = UniversalDetector()
    for line in file_bytes.readlines():
        detector.feed(line)
        if detector.done:
            break
    detector.close()
    return detector.result['encoding']
