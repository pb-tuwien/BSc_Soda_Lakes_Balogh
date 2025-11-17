#%% Imports
import TEM_tools as te
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime

root_path = root_path = Path(__file__).parents[2]
data_path: Path = root_path / 'data' / '20240522'
lambda_data_path: Path = data_path / 'lambda_comparison_20240522.csv'
results_path: Path = data_path / 'comparison_results_20240522.txt'

#%% Manual optimal lambda
manual_lambdas_0522: dict = {
    'M001': 13, 'M002': 13, 'M003': 18, 'M004': 28, 'M005': 24, 
    'M006': 45, 'M007': 13, 'M008': 39, 'M009': np.nan, 'M010': 15, 
    'M011': np.nan, 'M012': 21, 'M013': 13, 'M015': np.nan, 
    'M016': 15, 'M017': 28, 'M018': 13, 'M019': 15, 'M020': 15, 
    'M021': 24, 'M022': 62, 'M023': 33, 'M024': 28, 'M025': 53, 
    'M026': np.nan, 'M027': 18, 'M028': 13, 'M029': 53, 'M030': 15, 
    'M031': np.nan, 'M032': 28, 'M033': 15, 'M034': 18, 'M035': 15, 
    'M036': 24, 'M037': np.nan, 'M038': 33, 'M039': 39, 'M040': 13,
    'M041': 11, 'M042': 18, 'M045': np.nan
}

if __name__ == '__main__':
    comparison_df: pd.DataFrame = pd.DataFrame(
        manual_lambdas_0522.items(), 
        columns=['name', 'manual']
        )

    if lambda_data_path.exists():
        read_df: pd.DataFrame = pd.read_csv(lambda_data_path, sep=',')
        comparison_df = comparison_df.merge(
            read_df,
            on='name',
            how='left',
            suffixes=[None, '_drop']
        )
        comparison_df.drop(
            columns=[i for i in comparison_df.columns if i.endswith('_drop')],
            inplace=True
        )
    
    comparison_df.to_csv(lambda_data_path, sep=',', index=False)

#%% Find automated lambdas
if __name__ == '__main__':
    from filtering_20240522 import tem_data, tem_coords, rename_points_0522
    from filtering_20240522 import parsing_coords_0522
    # Preprocessing
    survey_0522 = te.SurveyTEM(
        data_path
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

    found_lambda_dict: dict = {}

    for sounding in manual_lambdas_0522.keys():
        found_lambdas = survey_0522.lambda_analysis_comparison(
            sounding=sounding,
            layer_type='dict',
            layers={0:1, 5:1.5},
            max_depth=20,
            test_range=(5, 100, 20),
            filter_times=(8, 210),
            noise_floor=0.015,
            constant_error=True,
            fname=False
        )
        found_lambda_dict[sounding] = found_lambdas
    
    found_lambda_df: pd.DataFrame = pd.DataFrame(
        found_lambda_dict.items(),
        columns=['name', 'temp']
    )

    found_lambda_df[['gradient', 'cubic', 'golden']] = pd.DataFrame(found_lambda_df['temp'].tolist(), index=found_lambda_df.index)
    found_lambda_df.drop(columns=['temp'], inplace=True)

    comparison_df = comparison_df.merge(
        found_lambda_df,
        on='name',
        how='left',
        suffixes=['_drop', None]
    )

    comparison_df.drop(
            columns=[i for i in comparison_df.columns if i.endswith('_drop')],
            inplace=True
        )
    
    comparison_df.to_csv(lambda_data_path, sep=',', index=False)

#%% Analyse DataFrame
def analyse_results(df:pd.DataFrame, threshold:float, mode:str = 'w'):
    # Set to NaN where manual is NaN
    df[df['manual'].isna()] = np.nan

    # How often manual worked
    manual_working: float = df['manual'].notna().sum() / df.shape[0]
    noNaN_df = df.dropna()

    # Analysing gradient:
    grad_diff = (noNaN_df['manual'] - noNaN_df['gradient']).abs()
    grad_rel_diff = grad_diff / noNaN_df['manual']
    grad_hit_mask = grad_rel_diff <= threshold
    gradient_working: float = grad_hit_mask.sum() / noNaN_df.shape[0]
    gradient_mean_deviation: float = grad_rel_diff.mean()

    # Analysing cubic spline:
    cub_diff = (noNaN_df['manual'] - noNaN_df['cubic']).abs()
    cub_rel_diff = cub_diff / noNaN_df['manual']
    cub_hit_mask = cub_rel_diff <= threshold
    cubic_working: float = cub_hit_mask.sum() / noNaN_df.shape[0]
    cubic_mean_deviation: float = cub_rel_diff.mean()

    # Analysing golden section:
    gold_diff = (noNaN_df['manual'] - noNaN_df['golden']).abs()
    gold_rel_diff = gold_diff / noNaN_df['manual']
    gold_hit_mask = gold_rel_diff <= threshold
    golden_working: float = gold_hit_mask.sum() / noNaN_df.shape[0]
    golden_mean_deviation: float = gold_rel_diff.mean()

    # Write results to file:
    with open(results_path, mode) as file:
        now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        file.write(f'Date:\t{now}\n')
        file.write(f'Manual precision:\t{100*manual_working:.3f} %\n\n')
        file.write(f'Comparing search algorithms with evalution\n')
        file.write(f'Threshold for hit:\t{100*threshold:.3f} %\n\n')
        file.write(f'Gradient based search:\n')
        file.write(f'Acurracy:\t{100*gradient_working:.3f} %\n')
        file.write(f'Mean relative deviation:\t{100*gradient_mean_deviation:.3f} %\n\n')
        file.write(f'Cubic spline based search:\n')
        file.write(f'Acurracy:\t{100*cubic_working:.3f} %\n')
        file.write(f'Mean relative deviation:\t{100*cubic_mean_deviation:.3f} %\n\n')
        file.write(f'Golden section search:\n')
        file.write(f'Acurracy:\t{100*golden_working:.3f} %\n')
        file.write(f'Mean relative deviation:\t{100*golden_mean_deviation:.3f} %\n')
        file.write('============================================\n\n')


if __name__ == '__main__':
    analyse_results(comparison_df, 0.1, 'w')
    analyse_results(comparison_df, 0.15, 'a')
    analyse_results(comparison_df, 0.2, 'a')





    