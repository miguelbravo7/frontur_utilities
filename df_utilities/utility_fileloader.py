import pandas
from chardet.universaldetector import UniversalDetector
from datetime import datetime
import df_utilities.constants as const
import df_utilities.utility_functions as uf


def load_agenda(file_path: str,
                date_format: str = const.DF_DATAFRAME_DAY_FORMAT) -> pandas.DataFrame:
    """Loads a pandas Dataframe given a file 
    and checking if the extension is supported

    Args:
        file_path (str): [description]
        date_format (str, optional): [description]. Defaults to const.DF_DATAFRAME_DAY_FORMAT.

    Raises:
        AttributeError: [description]

    Returns:
        pandas.DataFrame: [description]
    """
    extention = file_path.split('.')[-1]

    if extention not in const.SUPPORTED_EXTENSIONS:
        raise AttributeError(f'The file extention {extention} of file {file_path} is not supported.')

    date_parser = lambda x: pandas.datetime.strptime(x, date_format)

    data_frame = None
    if extention in const.SUPPORTED_EXCEL:
        data_frame = pandas.read_excel(file_path, date_parser=date_parser)
    elif extention in const.SUPPORTED_CSV:
        try:
            data_frame = pandas.read_csv(file_path, date_parser=date_parser)
        except UnicodeDecodeError:
            guessed_encoding = guess_encoding(open(file_path, 'rb'))
            uf.eprint("Decoding error using: utf-8\nAutomatic guess:", guessed_encoding)
            data_frame = pandas.read_csv(file_path, date_parser=date_parser, encoding=guessed_encoding)

    return data_frame


def dump_agenda(
                file_path: str,
                data_frame: pandas.DataFrame,
                date_format: str = const.DF_DATAFRAME_DAY_FORMAT
                ) -> pandas.DataFrame:
    """Loads a pandas DataFrame object given a file
    and checking if its extension is supported

    Args:
        file_path (str): [description]
        data_frame (pandas.DataFrame): [description]
        date_format (str, optional): [description]. Defaults to const.DF_DATAFRAME_DAY_FORMAT.

    Raises:
        AttributeError: [description]

    Returns:
        pandas.DataFrame: [description]
    """
    extention = file_path.split('.')[-1]

    if extention not in const.SUPPORTED_EXTENSIONS:
        raise AttributeError(f'The file extention {extention} of file {file_path} is not supported.')

    data_frame = data_frame.applymap(lambda x: x.strftime(const.DF_DATAFRAME_DAY_FORMAT) if isinstance(x, datetime) else x)

    if extention in const.SUPPORTED_EXCEL:
        data_frame.to_excel(file_path, index=False)
    elif extention in const.SUPPORTED_CSV:
        data_frame.to_csv(file_path, date_format=date_format, index=False, encoding='utf-16')


def guess_encoding(file_bytes: bin) -> str:
    """Guesses the encoding as a string using the
    Universal Encoding Detector library incrementally
    calling its feed method repeatedly with each block of text

    Args:
        file_bytes (bin): bytes without any decoding

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
