#%%
import TEM_tools as te
from pathlib import Path
import shutil
from campaign_20240522.filtering_20240522 import root_path
from campaign_20240522.algorithm_comparison_20240522 import data_path as data_path_0522

from campaign_20241008.algorithm_comparison_20241008 import data_path as data_path_1008

# if __name__ == '__main__':
#     # Preprocessing
#     survey_0522 = te.SurveyTEM(
#         root_path / 'data/20240522'
#     )
#     if Path(tem_coords).exists():
#         survey_0522.coords_read(
#             coords=tem_coords,
#             sep=','
#         )
#         survey_0522.coords_rename_points(
#             rename_dict=rename_points_0522
#         )
#         survey_0522.coords_sort_points()
#         survey_0522.coords_reproject()
#         survey_0522.coords_extract_save()
#     else:
#         survey_0522.coords_read()

#     if Path(tem_data).exists():
#         survey_0522.data_read(
#             data=tem_data
#         )
#     else:
#         survey_0522.data_read()
#     survey_0522.data_preprocess(
#         parsing_dict=parsing_coords_0522
#     )

#     survey_1008 = te.SurveyTEM(
#         root_path / 'data/20241008'
#     )
#     if Path(tem_coords).exists():
#         survey_1008.coords_read(
#             coords=tem_coords,
#             sep=','
#         )
#         survey_1008.coords_rename_points(
#             rename_dict=rename_points_1008
#         )
#         survey_1008.coords_sort_points()
#         survey_1008.coords_reproject()
#         survey_1008.coords_extract_save()
#     else:
#         survey_1008.coords_read()

#     if Path(tem_data).exists():
#         survey_1008.data_read(
#             data=tem_data
#         )
#     else:
#         survey_1008.data_read()
#     survey_1008.data_preprocess(
#         parsing_dict=parsing_coords_1008
#     )



#     # Location 2
#     opt_lam_2_0522 = survey_0522.analyse_inversion_gradient_curvature(
#         sounding='M028',
#         layer_type='dict',
#         layers={0:1, 5:1.5},
#         max_depth=20,
#         test_range=(10, 1000, 20),
#         filter_times=(8, 210),
#         fname=False
#     )

#     survey_0522.optimised_inversion_plot(
#         sounding='M028',
#         layer_type='dict',
#         layers={0:1, 5:1.5},
#         lam= opt_lam_2_0522,
#         max_depth=20,
#         filter_times=(8, 210),
#         test_range=(10, 1000, 20),
#         limits_rho=(8, 42),
#         limits_depth=(0, 20),
#         limits_rhoa=(5, 35),
#         fname=f'location_2_12.5_M028.png'
#         )
    
#     opt_lam_2_1008 = survey_1008.analyse_inversion_gradient_curvature(
#         sounding='M052',
#         layer_type='dict',
#         layers={0:1, 5:1.5},
#         max_depth=20,
#         test_range=(10, 1000, 20),
#         filter_times=(12, 80),
#         noise_floor=0.08,
#         fname=False
#     )

#     survey_1008.optimised_inversion_plot(
#         sounding='M052',
#         layer_type='dict',
#         layers={0:1, 5:1.5},
#         lam= opt_lam_2_1008,
#         max_depth=20,
#         filter_times=(12, 80),
#         noise_floor=0.08,
#         test_range=(10, 1000, 20),
#         limits_rho=(8, 42),
#         limits_depth=(0, 20),
#         limits_rhoa=(5, 35),
#         fname=f'location_2_6.25_M052.png'
#     )

#     opt_lam_improved_1008 = survey_1008.analyse_inversion_golden_section(
#         sounding='M052',
#         layer_type='dict',
#         layers={0:1, 5:1.5},
#         max_depth=20,
#         test_range=(10, 1000),
#         filter_times=(7, 110),
#         constant_error=True,
#         noise_floor=0.02,
#         fname=False
#     )

#     survey_1008.optimised_inversion_plot(
#         sounding='M052',
#         layer_type='dict',
#         layers={0:1, 5:1.5},
#         lam= opt_lam_improved_1008,
#         max_depth=20,
#         filter_times=(7, 110),
#         noise_floor=0.02,
#         constant_error=True,
#         test_range=(5, 50, 20),
#         limits_rho=(8, 42),
#         limits_depth=(0, 20),
#         limits_rhoa=(5, 35),
#         fname=f'improved_filter_time_6.25_M052.png'
#     )

#     opt_lam_improved_2_1008 = survey_1008.analyse_inversion_golden_section(
#         sounding='M052',
#         layer_type='dict',
#         layers={0:1, 5:1.5},
#         max_depth=20,
#         test_range=(5, 50),
#         filter_times=(7, 110),
#         constant_error=True,
#         noise_floor=0.02,
#         fname=False
#     )

#     survey_1008.optimised_inversion_plot(
#         sounding='M052',
#         layer_type='dict',
#         layers={0:1, 5:1.5},
#         lam= opt_lam_improved_2_1008,
#         max_depth=20,
#         filter_times=(7, 110),
#         noise_floor=0.02,
#         constant_error=True,
#         test_range=(5, 50, 20),
#         limits_rho=(8, 42),
#         limits_depth=(0, 20),
#         limits_rhoa=(5, 35),
#         fname=f'improved_ranges_6.25_M052.png'
#     )
# # %%
