#%%
import TEM_tools as te
from pathlib import Path

from campaign_20240522.filtering_20240522 import root_path, tem_data, tem_coords, rename_points_0522
from campaign_20240522.filtering_20240522 import parsing_coords_0522

from campaign_20241008.filtering_20241008 import root_path, tem_data, tem_coords, rename_points_1008
from campaign_20241008.filtering_20241008 import parsing_coords_1008

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

    # Testing range for L-curve
    # Large range: 10 - 1000
    _ = survey_0522.l_curve_plot(
            sounding='M028',
            layer_type='dict',
            layers={0:1, 5:1.5},
            max_depth=20,
            test_range=(10, 1000, 20),
            filter_times=(8, 210),
            noise_floor=0.015,
            constant_error=True,
            fname=f'l_curve_test_10_1000_M028.png'
        )
    
    # Medium range: 5 - 100 (Aigner et al. 2024 in the centre: 50)
    _ = survey_0522.l_curve_plot(
            sounding='M028',
            layer_type='dict',
            layers={0:1, 5:1.5},
            max_depth=20,
            test_range=(5, 100, 20),
            noise_floor=0.015,
            constant_error=True,
            filter_times=(8, 210),
            fname=f'l_curve_test_5_100_M028.png'
        )

    # Small range: 5 - 50 (Aigner et al. 2024 in the uppper bound)
    _ = survey_0522.l_curve_plot(
            sounding='M028',
            layer_type='dict',
            layers={0:1, 5:1.5},
            max_depth=20,
            test_range=(5, 50, 20),
            filter_times=(8, 210),
            noise_floor=0.015,
            constant_error=True,
            fname=f'l_curve_test_5_50_M028.png'
        )
    
    # Second Survey: Medium range
    _ = survey_1008.l_curve_plot(
                sounding='M052',
                layer_type='dict',
                layers={0:1, 5:1.5},
                max_depth=20,
                test_range=(5, 100, 20),
                noise_floor=0.015,
                constant_error=True,
                filter_times=(8, 110),
                fname=f'l_curve_test_5_100_M052.png'
            )
    
    # Second Survey: Small range
    _ = survey_1008.l_curve_plot(
            sounding='M052',
            layer_type='dict',
            layers={0:1, 5:1.5},
            max_depth=20,
            test_range=(5, 50, 20),
            filter_times=(8, 110),
            noise_floor=0.015,
            constant_error=True,
            fname=f'l_curve_test_5_50_M052.png'
        )