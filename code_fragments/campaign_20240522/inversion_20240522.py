#%% Add to sys path
from pathlib import Path
import sys

# Path to module
module_path = str(Path.cwd().parents[0] / 'Bsc_TEM_tools')

if module_path not in sys.path:
    sys.path.append(module_path)

import src.tem.survey_tem as st
from pathlib import Path
from code_fragments.campaign_20240522.filtering_20240522 import (tem_data, tem_coords, rename_points_0522, parsing_coords_0522, erroneous_soundings_0522)

#%%

if __name__ is '__main__':
    # Preprocessing
    survey_0522 = st.SurveyTEM(
        'data/20240522'
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

    # Inversion of M020: Good curve
    survey_0522.optimised_inversion_plot(
        sounding='M020',
        layer_type='dict',
        layers={0: 1, 5: 1.5, 15: 2},
        max_depth=30,
        test_range=(10, 1000, 20),
        filter_times=(8, 150),
        lam=645,
        fname='inversion_good_curve_auto_20240522.png'
    )

    survey_0522.optimised_inversion_plot(
        sounding='M020',
        layer_type='dict',
        layers={0: 1, 5: 1.5, 15: 2},
        max_depth=30,
        test_range=(10, 1000, 20),
        filter_times=(8, 150),
        lam=55,
        fname='inversion_good_curve_visual_20240522.png'
    )

    # Inversion of M010: Medium curve
    survey_0522.optimised_inversion_plot(
        sounding='M010',
        layer_type='dict',
        layers={0: 1, 5: 1.5, 15: 2},
        max_depth=30,
        test_range=(10, 1000, 20),
        filter_times=(8, 150),
        lam=70,
        fname='inversion_medium_curve_visual_20240522.png'
    )

    # Inversion of M011: Sharp curve
    survey_0522.optimised_inversion_plot(
        sounding='M011',
        layer_type='dict',
        layers={0: 1, 5: 1.5, 15: 2},
        max_depth=30,
        test_range=(10, 1000, 20),
        filter_times=(8, 150),
        lam=37,
        fname='inversion_sharp_curve_both_20240522.png'
    )

    # Inversion of M001: Sharp curve, noisy
    survey_0522.optimised_inversion_plot(
        sounding='M001',
        layer_type='dict',
        layers={0: 1, 5: 1.5, 15: 2},
        max_depth=30,
        test_range=(10, 1000, 20),
        filter_times=(8, 150),
        lam=89,
        fname='inversion_sharp_noisy_curve_both_20240522.png'
    )

    for sounding in [f'M{i:03d}' for i in range(1, 46) if i not in erroneous_soundings_0522]:
        survey_0522.optimised_inversion_plot(
            sounding=sounding,
            layer_type='dict',
            layers={0: 1, 5: 1.5, 15: 2},
            max_depth=30,
            test_range=(10, 1000, 20),
            filter_times=(8, 150),
            lam=80,
            fname=f'inversion_{sounding}_80_20240522.png'
        )

    for sounding in [f'M{i:03d}' for i in erroneous_soundings_0522]:
        survey_0522.optimised_inversion_plot(
            sounding=sounding,
            layer_type='dict',
            layers={0: 1, 5: 1.5, 15: 2},
            max_depth=30,
            test_range=(10, 1000, 20),
            filter_times=(8, 150),
            lam=80,
            fname=f'inversion_{sounding}_80_20240522_err.png'
        )