#%%
import TEM_tools as te
from pathlib import Path
from filtering_20241008 import root_path, tem_data, tem_coords, rename_points_1008
from filtering_20241008 import parsing_coords_1008, erroneous_soundings_1008

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

    for sounding in [f'M{i:03d}' for i in range(1, 67) if i not in erroneous_soundings_1008]:
        _ = survey_1008.lambda_analysis_comparison(
            sounding=sounding,
            layer_type='dict',
            layers={0:1, 5:1.5},
            max_depth=20,
            test_range=(5, 100, 20),
            filter_times=(8, 110),
            noise_floor=0.015,
            constant_error=True,
            fname=f'comparison_{sounding}.png'
        )

    # for sounding in [f'M{i:03d}' for i in erroneous_soundings_1008]:
    #     _ = survey_1008.lambda_analysis_comparison(
    #         sounding=sounding,
    #         layer_type='dict',
    #         layers={0: 1, 5: 1.5},
    #         max_depth=20,
    #         test_range=(10, 1000, 20),
    #         filter_times=(12, 80),
    #         noise_floor=0.08,
    #         fname=f'comparison_{sounding}_err.png'
    #     )
    
    # _ = survey_1008.lambda_analysis_comparison(
    #         sounding='M052',
    #         layer_type='dict',
    #         layers={0:1, 5:1.5},
    #         max_depth=20,
    #         test_range=(10, 1000, 20),
    #         filter_times=(7, 110),
    #         constant_error=True,
    #         noise_floor=0.02,
    #         fname=f'improved_comparison_M052.png'
    #     )
    
    # _ = survey_1008.lambda_analysis_comparison(
    #         sounding='M052',
    #         layer_type='dict',
    #         layers={0:1, 5:1.5},
    #         max_depth=20,
    #         test_range=(5, 50, 20),
    #         filter_times=(7, 110),
    #         constant_error=True,
    #         noise_floor=0.02,
    #         fname=f'improved_test_range_comparison_M052.png'
    #     )
