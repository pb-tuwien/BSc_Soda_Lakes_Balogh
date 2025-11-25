#%% Imports
import TEM_tools as te
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime

root_path = Path(__file__).parents[2]
data_path: Path = root_path / 'data' / '20241008'
lambda_data_path: Path = data_path / 'lambda_comparison_20241008.csv'
results_path: Path = data_path / 'comparison_results_20241008.txt'

#%% Manual optimal lambda
if __name__ == '__main__':
    manual_lambdas_1008: dict = {
        'M001': np.nan, 'M003': 8, 'M004': np.nan, 'M005': np.nan, 
        'M006': np.nan, 'M007': 9, 'M008': 11, 
        'M011': 45, 'M012': 13, 'M013': np.nan, 'M014': 11, 'M015': 9, 
        'M016': 45, 'M017': 28, 'M018': np.nan, 'M019': np.nan, 'M020': 33, 
        'M021': np.nan, 'M022': np.nan, 'M023': 11, 'M025': np.nan, 
        'M026': np.nan, 'M027': 13, 'M028': 11, 'M029': 11, 'M030': 11, 
        'M031': np.nan, 'M032': 9, 'M033': 9, 'M034': 13, 'M035': 8, 
        'M036': 18, 'M037': 9, 'M038': 11, 'M039': np.nan, 'M040': 15,
        'M041': 13, 'M042': 9, 'M043': 11, 'M044': 13, 'M045': 21, 
        'M046': np.nan, 'M047': 11, 'M048': np.nan, 'M049': np.nan, 'M050': 13,
        'M051': np.nan, 'M052': 11, 'M053': np.nan, 'M054': 11, 'M055': 11, 
        'M056': 33,
        'M062': 18, 
        'M066': 11
    }

if __name__ == '__main__':
    comparison_df: pd.DataFrame = pd.DataFrame(
        manual_lambdas_1008.items(), 
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
    from filtering_20241008 import tem_data, tem_coords, rename_points_1008
    from filtering_20241008 import parsing_coords_1008
    # Preprocessing
    survey_1008 = te.SurveyTEM(
        data_path
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

    found_lambda_dict: dict = {}

    for sounding in manual_lambdas_1008.keys():
        found_lambdas = survey_1008.lambda_analysis_comparison(
            sounding=sounding,
            layer_type='dict',
            layers={0:1, 5:1.5},
            max_depth=20,
            test_range=(5, 100, 20),
            filter_times=(8, 110),
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

    # Modes:
    mode_manual = noNaN_df['manual'].mode()[0]
    mode_grad = noNaN_df['gradient'].mode()[0]
    mode_cub = noNaN_df['cubic'].mode()[0]
    mode_gold = noNaN_df['golden'].mode()[0]

    # Write results to file:
    with open(results_path, mode) as file:
        now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        file.write(f'Date:\t{now}\n')
        file.write(f'Mode of manual lambdas:\t{mode_manual:.3f}\n')
        file.write(f'Manual precision:\t{100*manual_working:.3f} %\n\n')
        file.write(f'Comparing search algorithms with evalution\n')
        file.write(f'Threshold for hit:\t{100*threshold:.3f} %\n\n')
        file.write(f'Gradient based search:\n')
        file.write(f'Mode of lambdas:\t{mode_grad:.3f}\n')
        file.write(f'Acurracy:\t{100*gradient_working:.3f} %\n')
        file.write(f'Mean relative deviation:\t{100*gradient_mean_deviation:.3f} %\n\n')
        file.write(f'Cubic spline based search:\n')
        file.write(f'Mode of lambdas:\t{mode_cub:.3f}\n')
        file.write(f'Acurracy:\t{100*cubic_working:.3f} %\n')
        file.write(f'Mean relative deviation:\t{100*cubic_mean_deviation:.3f} %\n\n')
        file.write(f'Golden section search:\n')
        file.write(f'Mode of lambdas:\t{mode_gold:.3f}\n')
        file.write(f'Acurracy:\t{100*golden_working:.3f} %\n')
        file.write(f'Mean relative deviation:\t{100*golden_mean_deviation:.3f} %\n')
        file.write('============================================\n\n')


if __name__ == '__main__':
    analyse_results(comparison_df, 0.1, 'w')
    analyse_results(comparison_df, 0.15, 'a')
    analyse_results(comparison_df, 0.2, 'a')





    