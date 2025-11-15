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
        'M021': np.nan, 'M022': np.nan, 'M023': 11, 'M025': np.nan, 
        'M026': np.nan, 'M027': 13, 'M028': 11, 'M029': 11, 'M030': 11, 
        'M031': np.nan, 'M032': 9, 'M033': 9, 'M034': 13, 'M035': 8, 
        'M036': 18, 'M037': 9, 'M038': 11, 'M039': np.nan, 'M040': 15,
        'M041': 13, 'M042': 9, 'M043': 11, 'M044': 13, 'M045': 21, 
        'M046': np.nan, 'M047': 11, 'M048': np.nan, 'M049': np.nan, 'M050': 13,
        'M051': np.nan, 'M052': 11, 'M053': np.nan, 'M054': 11, 'M055': 11, 
        'M056': 33,
        'M062': 18, 
        'M066': 11
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