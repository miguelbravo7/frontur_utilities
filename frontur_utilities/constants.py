"""Loads the variables the default values that are going to be used
by the package modules
"""

import json
import os

data = {}
abs_path = os.path.dirname(os.path.realpath(__file__))

with open(abs_path + '/data/config.json', 'r') as f:
    data = json.load(f)

locals().update(**data)

SUPPORTED_EXTENSIONS = SUPPORTED_CSV + SUPPORTED_EXCEL

if PLANES_DATA_FILE_PATH == '':
    PLANES_DATA_FILE_PATH = abs_path + '/data/aviones.csv'
if SUBSTITUTIONS_FILE_PATH == '':
    SUBSTITUTIONS_FILE_PATH = abs_path + '/data/loc_substitutions.json'
if REQ_INTERVIEWS_FILE_PATH == '':
    REQ_INTERVIEWS_FILE_PATH = abs_path + '/data/interviews.json'
if DAYS_FILE_PATH == '':
    DAYS_FILE_PATH = abs_path + '/data/days.json'
