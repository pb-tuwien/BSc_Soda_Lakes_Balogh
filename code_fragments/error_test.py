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

    # Big Loop big current
    survey_0522.plot_inversion(
        subset=['M028'],
        layer_type='dict',
        layers={0:1, 5:1.5},
        lam=16,
        max_depth=20,
        filter_times=(8, 210),
        limits_rho=(8, 42),
        limits_depth=(0, 20),
        limits_rhoa=(5, 35),
        noise_floor=0.02,
        fname=f'location_2_12.5_0.02_M028.png'
    )

    # Small Loop big current
    survey_1008.plot_inversion(
        subset=['M052'],
        layer_type='dict',
        layers={0:1, 5:1.5},
        lam= 16,
        max_depth=20,
        filter_times=(12, 80),
        noise_floor=0.02,
        constant_error=True,
        limits_rho=(8, 42),
        limits_depth=(0, 20),
        limits_rhoa=(5, 35),
        fname='location_2_6.25_0.02_12-80_M052.png'
    )

    survey_1008.plot_inversion(
        subset=['M052'],
        layer_type='dict',
        layers={0:1, 5:1.5},
        lam= 16,
        max_depth=20,
        filter_times=(7, 110),
        noise_floor=0.02,
        constant_error=True,
        limits_rho=(8, 42),
        limits_depth=(0, 20),
        limits_rhoa=(5, 35),
        fname='location_2_6.25_0.02_7-110_M052.png'
    )

    # Big Loop small current
    survey_0522.plot_inversion(
        subset=['M002'],
        layer_type='dict',
        layers={0:1, 5:1.5},
        lam=16,
        max_depth=20,
        filter_times=(8, 210),
        limits_rho=(8, 42),
        limits_depth=(0, 20),
        limits_rhoa=(5, 35),
        noise_floor=0.02,
        fname=f'test_lambda_16_M002.png'
    )
