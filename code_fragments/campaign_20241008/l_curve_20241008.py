#%% Add to sys path
from pathlib import Path
import sys

# Path to module
module_path = str(Path.cwd().parents[0] / 'Bsc_TEM_tools')

if module_path not in sys.path:
    sys.path.append(module_path)

import src.tem.survey_tem as st
from pathlib import Path
from code_fragments.campaign_20241008.filtering_20241008 import tem_data, tem_coords, rename_points_1008, parsing_coords_1008, erroneous_soundings_1008

#%%

if __name__ is '__main__':
    # Preprocessing
    survey_1008 = st.SurveyTEM(
        'data/20241008'
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

    # L-curve
    for sounding in [f'M{i:03d}' for i in range(1, 67) if i not in erroneous_soundings_1008]:
        _ = survey_1008.l_curve_plot(
            sounding=sounding,
            layer_type='dict',
            layers={0:1, 5:1.5, 15:2},
            max_depth=30,
            test_range=(10, 1000, 20),
            filter_times=(12, 80),
            fname=f'l_curve_{sounding}.png'
        )

    for sounding in [f'M{i:03d}' for i in erroneous_soundings_1008]:
        _ = survey_1008.l_curve_plot(
            sounding=sounding,
            layer_type='dict',
            layers={0: 1, 5: 1.5, 15: 2},
            max_depth=30,
            test_range=(10, 1000, 20),
            filter_times=(12, 80),
            fname=f'l_curve_{sounding}_err.png'
        )
