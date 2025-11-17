#%% Imports
import TEM_tools as te
from pathlib import Path
import pandas as pd

from campaign_20240522.filtering_20240522 import root_path, tem_data, tem_coords, rename_points_0522
from campaign_20240522.filtering_20240522 import parsing_coords_0522
from campaign_20240522.algorithm_comparison_20240522 import lambda_data_path as lambdas_0522

from campaign_20241008.filtering_20241008 import root_path, tem_data, tem_coords, rename_points_1008
from campaign_20241008.filtering_20241008 import parsing_coords_1008
from campaign_20241008.algorithm_comparison_20241008 import lambda_data_path as lambdas_1008

if __name__ == '__main__':

    lambda_df_0522 = pd.read_csv(lambdas_0522, sep=',')
    lambda_df_1008 = pd.read_csv(lambdas_1008, sep=',')

    optimal_m28_0522 = lambda_df_0522[lambda_df_0522['name'] == 'M028']['manual'].values[0]
    optimal_m52_1008 = lambda_df_1008[lambda_df_1008['name'] == 'M052']['manual'].values[0]

    testing_dir = root_path / 'data' / 'parameter_testing'
    testing_dir.mkdir(parents=True, exist_ok=True)


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

#%% Testing different maximal depths

if __name__ == "__main__":
    
    survey_0522.plot_inversion(
        subset=['M028'],
        layer_type='dict',
        layers={0:1, 5:1.5},
        lam= optimal_m28_0522,
        max_depth=10,
        noise_floor=0.015,
        constant_error=True,
        filter_times=(8, 210),
        limits_rho=(5, 40),
        limits_depth=(0, 20),
        limits_rhoa=(5, 35),
        fname=testing_dir / 'M028_max_depth_10m.png'
    )

    survey_0522.plot_inversion(
        subset=['M028'],
        layer_type='dict',
        layers={0:1, 5:1.5},
        lam= optimal_m28_0522,
        max_depth=20,
        noise_floor=0.015,
        constant_error=True,
        filter_times=(8, 210),
        limits_rho=(5, 40),
        limits_depth=(0, 20),
        limits_rhoa=(5, 35),
        fname=testing_dir / 'M028_max_depth_20m.png'
    )

    survey_1008.plot_inversion(
        subset=['M052'],
        layer_type='dict',
        layers={0:1, 5:1.5},
        lam= optimal_m52_1008,
        max_depth=10,
        noise_floor=0.015,
        constant_error=True,
        filter_times=(8, 110),
        limits_rho=(5, 50),
        limits_depth=(0, 20),
        limits_rhoa=(5, 35),
        fname=testing_dir / 'M052_max_depth_10m.png'
    )

    survey_1008.plot_inversion(
        subset=['M052'],
        layer_type='dict',
        layers={0:1, 5:1.5},
        lam= optimal_m52_1008,
        max_depth=20,
        noise_floor=0.015,
        constant_error=True,
        filter_times=(8, 110),
        limits_rho=(5, 50),
        limits_depth=(0, 20),
        limits_rhoa=(5, 35),
        fname=testing_dir / 'M052_max_depth_20m.png'
    )



#%% Testing range for L-curve

if __name__ == "__main__":
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
            fname=testing_dir / 'M028_lambda_range_10_1000.png'
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
            fname=testing_dir / 'M028_lambda_range_5_100.png'
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
            fname=testing_dir / 'M028_lambda_range_5_50.png'
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
                fname=testing_dir / 'M052_lambda_range_5_100.png'
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
            fname=testing_dir / 'M052_lambda_range_5_50.png'
        )

#%% Testing Normalisation

if __name__ == '__main__':
    survey_0522.lambda_analysis_comparison(
        sounding='M028',
        layer_type='dict',
        layers={0:1, 5:1.5},
        max_depth=20,
        test_range=(5, 100, 20),
        filter_times=(8, 210),
        noise_floor=0.015,
        constant_error=True,
        fname=testing_dir / 'M028_normalization_true.png'
    )

    survey_0522.lambda_analysis_comparison(
        sounding='M028',
        layer_type='dict',
        layers={0:1, 5:1.5},
        max_depth=20,
        test_range=(5, 100, 20),
        filter_times=(8, 210),
        normalize=False,
        noise_floor=0.015,
        constant_error=True,
        fname=testing_dir /'M028_normalization_false.png'
    )