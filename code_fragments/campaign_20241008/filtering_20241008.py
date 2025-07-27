#%%
import TEM_tools as te
from pathlib import Path

root_path = Path(__file__).parents[2]
tem_data = root_path / 'data/20241008/20241008_tem_martenhofer_data.tem'
tem_coords = root_path / 'data/20241008/20241008_tem_martenhofer_coords.csv'

rename_points_1008 = {
    'M_': 'M'
}
parsing_coords_1008 = {
    'TEST001': 'Mtest', 'TEST002': 'Mtest',
    'TEST003': 'Mtest', 'TEST004': 'Mtest'
}

# Bad soundings
erroneous_soundings_1008 = [
    2, 9, 10, 24
]
# 2: far lower apparent resistivities than all other soundings
# 24 far higher apparent resistivities than all other soundings

if __name__ == '__main__':
    # Preprocessing
    survey_1008 = te.tem.SurveyTEM(
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

    # First look
    survey_1008.plot_raw_filtered(
        filter_times=(12, 80),
        legend=False,
        fname='20241008_all_soundings.png',
        subset=[f'M{i:03d}' for i in range(1, 67)],
        limits_rhoa=(0, 50)
    )
    survey_1008.plot_raw_filtered(
        filter_times=(12, 80),
        legend=False,
        fname='20241008_good_soundings.png',
        subset=[f'M{i:03d}' for i in range(1, 67) if i not in erroneous_soundings_1008],
        limits_rhoa=(0, 50)
    )
    survey_1008.plot_raw_filtered(
        filter_times=(12, 80),
        legend=True,
        fname='20241008_err_soundings.png',
        subset=[f'M{i:03d}' for i in erroneous_soundings_1008],
        limits_rhoa=(0, 100)
    )