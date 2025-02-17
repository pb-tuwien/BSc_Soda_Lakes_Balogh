#%% Add to sys path
from pathlib import Path
import sys

# Path to module
module_path = str(Path.cwd().parents[0] / 'Bsc_TEM_tools')

if module_path not in sys.path:
    sys.path.append(module_path)

import src.tem.survey_tem as st

#%% Survey from 22/05/2024

# tem_data = 'data/20240522/20240522_tem_martenhofer_data.tem'
# tem_coords = 'data/20240522/20240522_tem_martenhofer_coords.csv'

# marten_rename_points_0522 = {'M11': 'M011', 'M12': 'M012', 'M13': 'M013', 'M14': 'M014',
#                         'M15z': 'M015', 'M16': 'M016', 'M17': 'M017', 'M18': 'M018',
#                         'M19': 'M019', 'M20': 'M020', 'M21': 'M021', 'M22': 'M022',
#                         'M23': 'M023', 'M24': 'M024', 'M25': 'M025', 'M26': 'M026',
#                         'M27': 'M027', 'M28': 'M028', 'M29': 'M029', 'M30': 'M030',
#                         'M31': 'M031', 'M32': 'M032', 'M33': 'M033', 'M34': 'M034',
#                         'M35': 'M035', 'M36': 'M036', 'M37': 'M037', 'M38': 'M038',
#                         'M39': 'M039', 'M40': 'M040', 'M41': 'M041', 'M42': 'M042',
#                         'M43': 'M043', 'M44': 'M044', 'M45': 'M045'}
marten_parsing_coords_0522 = {'EP1': 'Mtest', 'TEM_test': 'Mtest'}

survey_marten_0522 = st.SurveyTEM('data/20240522')
# survey_marten_0522.coords_read()
# survey_marten_0522.coords_rename_points(rename_dict=marten_rename_points_0522)
# survey_marten_0522.coords_sort_points()
# survey_marten_0522.coords_reproject()
# survey_marten_0522.coords_extract_save()
survey_marten_0522.data_read()
survey_marten_0522.data_preprocess(parsing_dict=marten_parsing_coords_0522)
#%%
# survey_marten_0522.plot_raw_filtered(subset=['M024'], filter_times=(8, 80))
#%%
survey_marten_0522.analyse_inversion2(sounding='M024',
                             layer_type='dict',
                             layers={0:1, 5:1.5, 15:2},
                             max_depth=30,
                             test_range=(10, 5000, 20),
                             filter_times=(8, 80))

#%% Survey from 08/10/2024

# marten_tem_coords = 'data/martenhofer/tem/20241008/20241008_tem_martenhofer_coords.csv'
# marten_tem_data = 'data/martenhofer/tem/20241008/20241008_tem_martenhofer_data.tem'

marten_rename_points_1008 = {'M_': 'M'}
marten_parsing_coords_1008 = {'TEST001': 'Mtest', 'TEST002': 'Mtest', 'TEST003': 'Mtest', 'TEST004': 'Mtest'}

upper_lake = [f'M{i:03d}' for i in range(35, 53)]
lower_lake = [f'M{i:03d}' for i in range(1, 67) if f'M{i:03d}' not in upper_lake]

chosen_soundings = ['M043', 'M061']

survey_marten_1008 = st.SurveyTEM('data/20241008')
survey_marten_1008.coords_read()
# survey_marten_1008.coords_rename_points(rename_dict=marten_rename_points_1008)
# survey_marten_1008.coords_sort_points()
# survey_marten_1008.coords_reproject()
# survey_marten_1008.coords_extract_save()
survey_marten_1008.data_read()
survey_marten_1008.data_preprocess(parsing_dict=marten_parsing_coords_1008)
#%%
survey_marten_1008.plot_raw_filtered(subset=['M043'], filter_times=(10, 80))

#%%
# survey_marten_1008.data_inversion(subset=['M001'], max_depth=30, layers=1, filter_times=(7, 700))
# survey_marten_1008.plot_raw_filtered(subset=['M061'], filter_times=(5, 110))
# survey_marten_1008.plot_raw_filtered(legend=False, filter_times=(10, 700), subset=upper_lake)
# survey_marten_1008.plot_raw_filtered(legend=False, filter_times=(10, 700), subset=lower_lake)
# survey_marten_1008.plot_inversion(max_depth=30, layer_type='dict', layers={0:1, 5:1.5, 15:2},
#                              filter_times=(10, 110), lam=71.2, subset=['M061'])
survey_marten_1008.analyse_inversion2(sounding='M043',
                             layer_type='dict',
                             layers={0:1, 5:1.5, 15:2},
                             max_depth=30,
                             test_range=(10, 5000, 20),
                             filter_times=(12, 90))

# survey_marten_1008.analyse_inversion_plot(sounding='M043',
#                              layer_type='dict',
#                              layers={0:1, 5:1.5, 15:2},
#                              max_depth=30,
#                              test_range=(10, 5000, 20),
#                              filter_times=(12, 80))
# survey_marten_1008.read_data(data=marten_tem_data, coords=marten_tem_coords, preproc=marten_tem_preproc)
# survey_marten_1008.load_data()
# survey_marten_1008.filter_data()
# # survey_peat.plot_raw_filtered(legend=False, filter_times=(7, 700))
# survey_marten_1008.plot_inversion(subset=['M004'], max_depth=30, layer_type='dict', layers={0:0.5, 5:1, 10:2}, filter_times=(7, 700))



