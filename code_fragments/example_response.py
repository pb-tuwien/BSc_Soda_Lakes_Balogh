#%% Add to sys path
import TEM_tools.tem.survey_tem as st
from pathlib import Path
from campaign_20240522.filtering_20240522 import root_path, tem_data, tem_coords, rename_points_0522, parsing_coords_0522
import numpy as np

#%%

depth_vector = np.arange(
    0,
    31,
    step=5
)
start_model = np.array(
    [
        100, 100, 100, 10, 10, 50, 50
    ]
)

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

    # Forward Model: Sounding
    survey_0522.plot_forward_model(
        subset=['M001'],
        max_depth=30,
        layers=depth_vector,
        layer_type='custom',
        start_model=start_model,
        fname='example_response.png'
    )
