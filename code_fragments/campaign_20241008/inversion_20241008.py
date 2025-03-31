#%% 
import TEM_tools.tem.survey_tem as st
from pathlib import Path
from filtering_20241008 import root_path, tem_data, tem_coords, rename_points_1008, parsing_coords_1008, erroneous_soundings_1008

#%%

if __name__ is '__main__':
    # Preprocessing
    survey_1008 = st.SurveyTEM(
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

    # Inversion of M047: Elliptic curve
    survey_1008.optimised_inversion_plot(
        sounding='M047',
        layer_type='dict',
        layers={0: 1, 5: 1.5, 15: 2},
        max_depth=30,
        test_range=(10, 1000, 20),
        filter_times=(12, 80),
        lam=113,
        fname='inversion_ellipse_curve_visual_20241008.png'
    )

    # Inversion of M040: Sharp curve
    survey_1008.optimised_inversion_plot(
        sounding='M040',
        layer_type='dict',
        layers={0: 1, 5: 1.5, 15: 2},
        max_depth=30,
        test_range=(10, 1000, 20),
        filter_times=(12, 80),
        lam=298,
        fname='inversion_sharp_curve_grad_20241008.png'
    )
    survey_1008.optimised_inversion_plot(
        sounding='M040',
        layer_type='dict',
        layers={0: 1, 5: 1.5, 15: 2},
        max_depth=30,
        test_range=(10, 1000, 20),
        filter_times=(12, 80),
        lam=627,
        fname='inversion_sharp_curve_golden_20241008.png'
    )

    for sounding in [f'M{i:03d}' for i in range(1, 67) if i not in erroneous_soundings_1008]:
        survey_1008.optimised_inversion_plot(
            sounding=sounding,
            layer_type='dict',
            layers={0: 1, 5: 1.5, 15: 2},
            max_depth=30,
            test_range=(10, 1000, 20),
            filter_times=(12, 80),
            lam=113,
            fname=f'inversion_{sounding}_113_20241008.png'
        )

    for sounding in [f'M{i:03d}' for i in erroneous_soundings_1008]:
        survey_1008.optimised_inversion_plot(
            sounding=sounding,
            layer_type='dict',
            layers={0: 1, 5: 1.5, 15: 2},
            max_depth=30,
            test_range=(10, 1000, 20),
            filter_times=(12, 80),
            lam=113,
            fname=f'inversion_{sounding}_113_20241008_err.png'
        )