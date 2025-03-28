#%% 
import TEM_tools.tem.survey_tem as st
from pathlib import Path
from campaign_20240522.filtering_20240522 import root_path, tem_data, tem_coords, rename_points_0522, parsing_coords_0522, erroneous_soundings_0522

#%%

if __name__ is '__main__':
    # Preprocessing
    survey_0522 = st.SurveyTEM(
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

    # L-curve
    for sounding in [f'M{i:03d}' for i in range(1, 46) if i not in erroneous_soundings_0522]:
        _ = survey_0522.l_curve_plot(
            sounding=sounding,
            layer_type='dict',
            layers={0:1, 5:1.5, 15:2},
            max_depth=30,
            test_range=(10, 1000, 20),
            filter_times=(8, 150),
            fname=f'l_curve_{sounding}.png'
        )

    for sounding in [f'M{i:03d}' for i in erroneous_soundings_0522]:
        _ = survey_0522.l_curve_plot(
            sounding=sounding,
            layer_type='dict',
            layers={0: 1, 5: 1.5, 15: 2},
            max_depth=30,
            test_range=(10, 1000, 20),
            filter_times=(8, 150),
            fname=f'l_curve_{sounding}_err.png'
        )
