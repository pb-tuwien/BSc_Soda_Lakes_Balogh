#%% Imports
import TEM_tools as te
from pathlib import Path
import pandas as pd
import numpy as np
from filtering_20240522 import root_path, tem_data, tem_coords, rename_points_0522
from filtering_20240522 import parsing_coords_0522, erroneous_soundings_0522

#%% Manual optimal lambda
if __name__ == '__main__':
    manual_lambdas_20240522: dict = {
        'M001': 13, 'M002': 13, 'M003': 18, 'M004': 28, 'M005': 24, 
        'M006': 45, 'M007': 13, 'M008': 39, 'M009': np.nan, 'M010': 15, 
        'M011': np.nan, 'M012': 21, 'M013': 13, 'M015': np.nan, 
        'M016': 15, 'M017': 28, 'M018': 13, 'M019': 15, 'M020': 15, 
        'M021': 24, 'M022': 62, 'M023': 33, 'M024': 28, 'M025': 53, 
        'M026': np.nan, 'M027': 18, 'M028': 13, 'M029': 53, 'M030': 15, 
        'M031': np.nan, 'M032': 28, 'M033': 15, 'M034': 18, 'M035': 15, 
        'M036': 24, 'M037': np.nan, 'M038': 33, 'M039': 39, 'M040': 13,
        'M041': 11, 'M042': 18, 'M045': np.nan
    }

    # manual_lambdas_20240522: dict = {
    #     'M001': 1, 'M002': 1, 'M003': 1, 'M004': 1, 'M005': 1, 
    #     'M006': 1, 'M007': 1, 'M008': 1, 'M009': 1, 'M010': 1, 
    #     'M011': 1, 'M012': 1, 'M013': 1, 'M014': 1, 'M015': 1, 
    #     'M016': 1, 'M017': 1, 'M018': 1, 'M019': 1, 'M020': 1, 
    #     'M021': 1, 'M022': 1, 'M023': 1, 'M024': 1, 'M025': 1, 
    #     'M026': 1, 'M027': 1, 'M028': 1, 'M029': 1, 'M030': 1, 
    #     'M031': 1, 'M032': 1, 'M033': 1, 'M034': 1, 'M035': 1, 
    #     'M036': 1, 'M037': 1, 'M038': 1, 'M039': 1, 'M040': 1,
    #     'M041': 1, 'M042': 1, 'M043': 1, 'M044': 1, 'M045': 1
    # }

#%% Find automated lambdas
if __name__ == '__main__':
    # Preprocessing
    survey_0522 = te.SurveyTEM(
        root_path / 'data/20240522'
    )
    if Path(tem_coords).exists():
        survey_0522.coords_read(
            coords=tem_coords,
            sep=','
        )
        survey_0522.coords_rename_points(
            rename_dict=rename_points_0522
        )
        survey_0522.coords_sort_points()
        survey_0522.coords_reproject()
        survey_0522.coords_extract_save()
    else:
        survey_0522.coords_read()

    if Path(tem_data).exists():
        survey_0522.data_read(
            data=tem_data
        )
    else:
        survey_0522.data_read()
    survey_0522.data_preprocess(
        parsing_dict=parsing_coords_0522
    )