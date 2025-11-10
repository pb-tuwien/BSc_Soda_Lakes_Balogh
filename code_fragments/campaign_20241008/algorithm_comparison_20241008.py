#%% Imports
import TEM_tools as te
from pathlib import Path
import pandas as pd
import numpy as np
from filtering_20241008 import root_path, tem_data, tem_coords, rename_points_1008
from filtering_20241008 import parsing_coords_1008, erroneous_soundings_1008

#%% Manual optimal lambda
if __name__ == '__main__':
    manual_lambdas_20241008: dict = {
        'M001': np.nan, 'M003': 8, 'M004': np.nan, 'M005': np.nan, 
        'M006': np.nan, 'M007': 9, 'M008': 11, 
        'M011': 45, 'M012': 13, 'M013': np.nan, 'M014': 11, 'M015': 9, 
        'M016': 45, 'M017': 28, 'M018': np.nan, 'M019': np.nan, 'M020': 33, 
        'M021': np.nan, 'M022': np.nan, 'M023': 1, 'M025': 1, 
        'M026': 1, 'M027': 1, 'M028': 1, 'M029': 1, 'M030': 1, 
        'M031': 1, 'M032': 1, 'M033': 1, 'M034': 1, 'M035': 1, 
        'M036': 1, 'M037': 1, 'M038': 1, 'M039': 1, 'M040': 1,
        'M041': 1, 'M042': 1, 'M043': 1, 'M044': 1, 'M045': 1, 
        'M046': 1, 'M047': 1, 'M048': 1, 'M049': 1, 'M050': 1,
        'M051': 1, 'M052': 1, 'M053': 1, 'M054': 1, 'M055': 1, 
        'M056': 1,
        'M062': 1, 
        'M066': 1
    }

#%% Find automated lambdas
if __name__ == '__main__':
    # Preprocessing
    survey_1008 = te.SurveyTEM(
        root_path / 'data/20241008'
    )
    if Path(tem_coords).exists():
        survey_1008.coords_read(
            coords=tem_coords,
            sep=','
        )
        survey_1008.coords_rename_points(
            rename_dict=rename_points_1008
        )
        survey_1008.coords_sort_points()
        survey_1008.coords_reproject()
        survey_1008.coords_extract_save()
    else:
        survey_1008.coords_read()

    if Path(tem_data).exists():
        survey_1008.data_read(
            data=tem_data
        )
    else:
        survey_1008.data_read()
    survey_1008.data_preprocess(
        parsing_dict=parsing_coords_1008
    )