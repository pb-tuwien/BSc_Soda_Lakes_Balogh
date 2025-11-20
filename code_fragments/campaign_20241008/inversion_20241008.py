#%% 
import TEM_tools as te
from pathlib import Path
import pandas as pd
from filtering_20241008 import root_path, tem_data, tem_coords, rename_points_1008
from filtering_20241008 import parsing_coords_1008, erroneous_soundings_1008
from algorithm_comparison_20241008 import lambda_data_path

lambda_df = pd.read_csv(lambda_data_path, sep=',')

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

    #%% Inversion of all soundings

    for sounding in lambda_df[lambda_df['manual'].notna()]['name']:
        opt_lam = lambda_df[lambda_df['name'] == sounding]['manual'].values[0]

        survey_1008.optimised_inversion_plot(
            sounding=sounding,
            layer_type='dict',
            layers={0:1, 5:1.5},
            lam= opt_lam,
            max_depth=20,
            filter_times=(8, 110),
            noise_floor=0.015,
            constant_error=True,
            test_range=(5, 100, 20),
            limits_rho=(0, 80),
            limits_depth=(0, 20),
            limits_rhoa=(0, 50),
            fname=f'optimised_{sounding}.png'
        )

    #%%

    opt_lam_mode = lambda_df['manual'].mode()[0]

    for sounding in [f'M{i:03d}' for i in range(1, 67) if i not in erroneous_soundings_1008]:
        survey_1008.optimised_inversion_plot(
            sounding=sounding,
            layer_type='dict',
            layers={0:1, 5:1.5},
            lam= opt_lam_mode,
            max_depth=20,
            filter_times=(8, 110),
            noise_floor=0.015,
            constant_error=True,
            test_range=(5, 100, 20),
            limits_rho=(0, 55),
            limits_depth=(0, 20),
            limits_rhoa=(5, 38),
            fname=f'same_lambda_{sounding}.png'
        )
