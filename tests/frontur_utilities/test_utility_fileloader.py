import pytest
from fixtures import df
from unittest import mock
from frontur_utilities import utility_fileloader, const


@pytest.mark.parametrize('ext', const.SUPPORTED_EXCEL)
@mock.patch(
    'frontur_utilities.utility_fileloader.pandas.read_excel',
    return_value='excel',
    autospec=True)
def test_load_excel_agenda(mock_method, ext, tmpdir):
    file = tmpdir.join('filename.' + ext)
    actual = utility_fileloader.load_agenda(file.strpath)

    assert actual == 'excel'


@pytest.mark.parametrize('ext', const.SUPPORTED_CSV)
@mock.patch(
    'frontur_utilities.utility_fileloader.pandas.read_csv',
    return_value='csv',
    autospec=True)
def test_load_csv_agenda(mock_method, ext, tmpdir):
    file = tmpdir.join('filename.' + ext)
    actual = utility_fileloader.load_agenda(file.strpath)

    assert actual == 'csv'


@pytest.mark.parametrize('ext', const.SUPPORTED_EXCEL)
@mock.patch('frontur_utilities.utility_fileloader.pandas.DataFrame.to_excel')
def test_save_excel_agenda(mock_method, ext, df, tmpdir):
    file = tmpdir.join('filename.' + ext)
    utility_fileloader.save_agenda(file.strpath, df)
    mock_method.assert_called_once_with(file.strpath, index=False)


@pytest.mark.parametrize('ext', const.SUPPORTED_CSV)
@mock.patch('frontur_utilities.utility_fileloader.pandas.DataFrame.to_csv')
def test_save_csv_agenda(mock_method, ext, df, tmpdir):
    file = tmpdir.join('filename.' + ext)
    date_format = ''
    utility_fileloader.save_agenda(file.strpath, df, date_format=date_format)
    mock_method.assert_called_once_with(file.strpath, date_format=date_format, index=False, encoding='utf-16')
