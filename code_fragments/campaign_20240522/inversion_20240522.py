#%%
import TEM_tools as te
import pandas as pd
from pathlib import Path
from filtering_20240522 import root_path, tem_data, tem_coords, rename_points_0522
from filtering_20240522 import parsing_coords_0522, erroneous_soundings_0522
from algorithm_comparison_20240522 import lambda_data_path

lambda_df = pd.read_csv(lambda_data_path, sep=',')

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

    #%% Inversion of all soundings

    for sounding in lambda_df[lambda_df['manual'].notna()]['name']:
        opt_lam = lambda_df[lambda_df['name'] == sounding]['manual'].values[0]

        survey_0522.optimised_inversion_plot(
            sounding=sounding,
            layer_type='dict',
            layers={0:1, 5:1.5},
            lam= opt_lam,
            max_depth=20,
            filter_times=(8, 210),
            test_range=(5, 100, 20),
            noise_floor=0.015,
            constant_error=True,
            limits_rho=(0, 55),
            limits_depth=(0, 20),
            limits_rhoa=(5, 38),
            fname=f'optimised_{sounding}.png'
        )
