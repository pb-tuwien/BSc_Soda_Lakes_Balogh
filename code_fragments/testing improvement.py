#%% Imports
import TEM_tools as te
from pathlib import Path
import pandas as pd

from campaign_20241008.filtering_20241008 import root_path, tem_data, tem_coords, rename_points_1008
from campaign_20241008.filtering_20241008 import parsing_coords_1008
from campaign_20241008.algorithm_comparison_20241008 import lambda_data_path as lambdas_1008

if __name__ == '__main__':
    lambda_df_1008 = pd.read_csv(lambdas_1008, sep=',')

    location_dir = root_path / 'data' / 'lambda_improvement'
    location_dir.mkdir(parents=True, exist_ok=True)


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

if __name__ == '__main__':
    opt_lam_1008 = lambda_df_1008[lambda_df_1008['name'] == 'M050']['manual'].values[0]
    mode_lam_1008 = lambda_df_1008['manual'].mode()[0]
    test_lam_1008 = 50.0

    survey_1008.optimised_inversion_plot(
        sounding='M050',
        layer_type='dict',
        layers={0:1, 5:1.5},
        lam= opt_lam_1008,
        max_depth=20,
        filter_times=(8, 110),
        noise_floor=0.015,
        constant_error=True,
        test_range=(5, 100, 20),
        limits_rho=(5, 42),
        limits_depth=(0, 20),
        limits_rhoa=(5, 35),
        fname=location_dir / 'optimal_lambda_M050.png'
    )

    survey_1008.optimised_inversion_plot(
        sounding='M050',
        layer_type='dict',
        layers={0:1, 5:1.5},
        lam= mode_lam_1008,
        max_depth=20,
        filter_times=(8, 110),
        noise_floor=0.015,
        constant_error=True,
        test_range=(5, 100, 20),
        limits_rho=(5, 42),
        limits_depth=(0, 20),
        limits_rhoa=(5, 35),
        fname=location_dir / 'mode_lambda_M050.png'
    )

    survey_1008.optimised_inversion_plot(
        sounding='M050',
        layer_type='dict',
        layers={0:1, 5:1.5},
        lam= test_lam_1008,
        max_depth=20,
        filter_times=(8, 110),
        noise_floor=0.015,
        constant_error=True,
        test_range=(5, 100, 20),
        limits_rho=(5, 42),
        limits_depth=(0, 20),
        limits_rhoa=(5, 35),
        fname=location_dir / 'test_lambda_50_M050.png'
    )