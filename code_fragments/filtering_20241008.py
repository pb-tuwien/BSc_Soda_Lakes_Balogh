#%% Add to sys path
from pathlib import Path
import sys

# Path to module
module_path = str(Path.cwd().parents[0] / 'Bsc_TEM_tools')

if module_path not in sys.path:
    sys.path.append(module_path)

import src.tem.survey_tem as st
from pathlib import Path

#%%

tem_data = 'data/20241008/20241008_tem_martenhofer_data.tem'
tem_coords = 'data/20241008/20241008_tem_martenhofer_coords.csv'

rename_points_1008 = {'M_': 'M'}
parsing_coords_1008 = {'TEST001': 'Mtest', 'TEST002': 'Mtest', 'TEST003': 'Mtest', 'TEST004': 'Mtest'}

# Bad soundings
erroneous_soundings_1008 = []

if __name__ is '__main__':
    # Preprocessing
    survey_1008 = st.SurveyTEM('data/20241008')
    if Path(tem_coords).exists():
        survey_1008.coords_read(coords=tem_coords, sep=',')
        survey_1008.coords_rename_points(rename_dict=rename_points_1008)
        survey_1008.coords_sort_points()
        survey_1008.coords_reproject()
        survey_1008.coords_extract_save()
    else:
        survey_1008.coords_read()

    if Path(tem_data).exists():
        survey_1008.data_read(data=tem_data)
    else:
        survey_1008.data_read()
    survey_1008.data_preprocess(parsing_dict=parsing_coords_1008)

    # First look
    survey_1008.plot_raw_filtered(filter_times=(8, 150), legend=False, fname='20241008_all_soundings.png')
    # survey_1008.plot_raw_filtered(filter_times=(8, 150), legend=False, fname='20241008_good_soundings.png',
    #                               subset=[f'M{i:03d}' for i in range(1, 46) if i not in erroneous_soundings_1008])