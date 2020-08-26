import json
from os import path

# data = {}
with open(path.dirname(path.realpath(__file__)) + '/../config.json', 'r') as f:
    data = json.load(f)

locals().update(**data)

# SUPPORTED_EXCEL = ['xls', 'xlsx', 'xlsm', 'xlsb',  'odf']
# SUPPORTED_CSV = ['csv']
# SUPPORTED_ALT = ['txt']
# SUPPORTED_EXTENSIONS = SUPPORTED_CSV + SUPPORTED_EXCEL

# DF_DATAFRAME_DAY_FORMAT = "%d/%m/%Y"

# WEEKDAY = {
#     'L': 0,
#     'M': 1,
#     'X': 2,
#     'J': 3,
#     'V': 4,
#     'S': 5,
#     'D': 6
# }

# DATA_FILE_PATH = 'E:/DocumentosHDD/GitHub/TFG-Seleccion_de_Vuelos/data'
# FILES_FILE_PATH = DATA_FILE_PATH + '/files'

# KW_FRONTUR = "frontur"
# FRONTUR_FILE_PATH = FILES_FILE_PATH + '/FronTurFeb2019.xls'
# KW_PLANES = "planes"
# PLANES_DATA_FILE_PATH = FILES_FILE_PATH + '/aviones.csv'
# KW_SUBSTITUTIONS = "aliases"
# SUBSTITUTIONS_FILE_PATH = DATA_FILE_PATH + '/loc_substitutions.json'
# KW_INTERVIEWS = "interviews"
# REQ_INTERVIEWS_FILE_PATH = DATA_FILE_PATH + '/interviews.json'
# KW_DATES = "available_days"
# DAYS_FILE_PATH = DATA_FILE_PATH + '/days.json'

# # const values of dataframe
# DF_WEEKDAY_COL_NAME = 'Dia_semana'
# DF_OPERATION_START_COL_NAME = 'Opera_desde'
# DF_OPERATION_END_COL_NAME = 'Opera_hasta'
# DF_DAY_COL_NAME = 'Day'
# DF_PLANE_COL_NAME = 'Aeronave'
# DF_ORIGIN_COL_NAME = 'Origen'

# # const values of days.json
# KW_COLUMN_DAY_NAME = 'day_column_name'
# KW_AVAILABLE_DAYS = 'days'
# KW_DAY_FORMAT = 'format'

# # const values of loc_substitutions.json
# KW_COL_NAME = 'column_name'
# KW_REF_COL_NAME = 'reference_column_name'
# KW_REF_COL_VALUES = 'reference_column_values'
# KW_REPL_VALUE = 'replace_value'

# # const values of interviews.json
# KW_MIN_SAMPLE = 'minimum_sample'
# KW_PASS_BY_STRATUM = 'passengers_by_stratum'
