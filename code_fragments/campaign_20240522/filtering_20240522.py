#%%
import TEM_tools as te
from pathlib import Path

root_path = Path(__file__).parents[2]
tem_data = root_path / 'data/20240522/20240522_tem_martenhofer_data.tem'
tem_coords = root_path / 'data/20240522/20240522_tem_martenhofer_coords.csv'

rename_points_0522 = {
    'M11': 'M011', 'M12': 'M012', 'M13': 'M013', 'M14': 'M014',
    'M15z': 'M015', 'M16': 'M016', 'M17': 'M017', 'M18': 'M018',
    'M19': 'M019', 'M20': 'M020', 'M21': 'M021', 'M22': 'M022',
    'M23': 'M023', 'M24': 'M024', 'M25': 'M025', 'M26': 'M026',
    'M27': 'M027', 'M28': 'M028', 'M29': 'M029', 'M30': 'M030',
    'M31': 'M031', 'M32': 'M032', 'M33': 'M033', 'M34': 'M034',
    'M35': 'M035', 'M36': 'M036', 'M37': 'M037', 'M38': 'M038',
    'M39': 'M039', 'M40': 'M040', 'M41': 'M041', 'M42': 'M042',
    'M43': 'M043', 'M44': 'M044', 'M45': 'M045', 'TEM_test': 'Mtest'
}
parsing_coords_0522 = {
    'T001': 'Mtest', 'T002': 'Mtest'
}

# Bad soundings
erroneous_soundings_0522 = [
    14, 43, 44
]

if __name__ == '__main__':
    # Preprocessing
    survey_0522 = te.tem.SurveyTEM(
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

    # First look
    survey_0522.plot_raw_filtered(
        filter_times=(8, 210),
        legend=False,
        fname='20240522_all_soundings.png',
        subset=[f'M{i:03d}' for i in range(1, 46)],
        limits_rhoa=(5, 35)
    )
    survey_0522.plot_raw_filtered(
        filter_times=(8, 210),
        legend=False,
        fname='20240522_good_soundings.png',
        subset=[f'M{i:03d}' for i in range(1, 46) if i not in erroneous_soundings_0522],
        limits_rhoa=(5, 35)
    )
    survey_0522.plot_raw_filtered(
        filter_times=(8, 210),
        legend=True,
        fname='20240522_err_soundings.png',
        subset=[f'M{i:03d}' for i in erroneous_soundings_0522],
        limits_rhoa=(5, 35)
    )