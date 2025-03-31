#%% 
import TEM_tools.tem.survey_tem as st
from pathlib import Path
from filtering_20240522 import root_path, tem_data, tem_coords, rename_points_0522, parsing_coords_0522

#%%

if __name__ is '__main__':
    # Preprocessing
    survey_0522 = st.SurveyTEM(
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

    # Good curvature: M020
    survey_0522.lambda_analysis_comparison(
        sounding='M020',
        layer_type='dict',
        layers={0:1, 5:1.5, 15:2},
        max_depth=30,
        test_range=(10, 1000, 20),
        filter_times=(8, 150),
        fname='lambda_analysis_good_curve_20240522.png'
    )
    # Medium curvature: M010
    survey_0522.lambda_analysis_comparison(
        sounding='M010',
        layer_type='dict',
        layers={0: 1, 5: 1.5, 15: 2},
        max_depth=30,
        test_range=(10, 1000, 20),
        filter_times=(8, 150),
        fname='lambda_analysis_medium_curve_20240522.png'
    )
    # Small curvature: M025
    survey_0522.lambda_analysis_comparison(
        sounding='M025',
        layer_type='dict',
        layers={0: 1, 5: 1.5, 15: 2},
        max_depth=30,
        test_range=(10, 1000, 20),
        filter_times=(8, 150),
        fname='lambda_analysis_light_curve_20240522.png'
    )
    # No L-Curve: M017
    survey_0522.lambda_analysis_comparison(
        sounding='M017',
        layer_type='dict',
        layers={0: 1, 5: 1.5, 15: 2},
        max_depth=30,
        test_range=(10, 1000, 20),
        filter_times=(8, 150),
        fname='lambda_analysis_bad_curve_20240522.png'
    )

    # Sharp corner: M011
    survey_0522.lambda_analysis_comparison(
        sounding='M011',
        layer_type='dict',
        layers={0: 1, 5: 1.5, 15: 2},
        max_depth=30,
        test_range=(10, 1000, 20),
        filter_times=(8, 150),
        fname='lambda_analysis_sharp_curve_20240522.png'
    )

    # Sharp corner with noise: M001
    survey_0522.lambda_analysis_comparison(
        sounding='M001',
        layer_type='dict',
        layers={0: 1, 5: 1.5, 15: 2},
        max_depth=30,
        test_range=(10, 1000, 20),
        filter_times=(8, 150),
        fname='lambda_analysis_sharp_noisy_curve_20240522.png'
    )