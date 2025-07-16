#%%
import TEM_tools as te
from pathlib import Path
from filtering_20240522 import root_path, tem_data, tem_coords, rename_points_0522
from filtering_20240522 import parsing_coords_0522, erroneous_soundings_0522

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

    #%% Example sounding: M024
    # Testing max depth for inversion
    optimal_lam_m24 = survey_0522.analyse_inversion_gradient_curvature(
        sounding='M024',
        layer_type='dict',
        layers={0:1, 5:1.5},
        max_depth=20,
        test_range=(10, 1000, 20),
        filter_times=(8, 210),
        fname=False
    )

    survey_0522.plot_inversion(
        subset=['M024'],
        layer_type='dict',
        layers={0:1, 5:1.5},
        lam= optimal_lam_m24,
        max_depth=10,
        filter_times=(8, 210),
        limits_rho=(8, 42),
        limits_depth=(0, 20),
        limits_rhoa=(5, 35),
        fname=f'M024_max_depth_10m.png'
    )

    survey_0522.plot_inversion(
        subset=['M024'],
        layer_type='dict',
        layers={0:1, 5:1.5},
        lam= optimal_lam_m24,
        max_depth=20,
        filter_times=(8, 210),
        limits_rho=(8, 42),
        limits_depth=(0, 20),
        limits_rhoa=(5, 35),
        fname=f'M024_max_depth_20m.png'
    )

    # Testing noise floor
    survey_0522.plot_inversion(
        subset=['M024'],
        layer_type='dict',
        layers={0:1, 5:1.5},
        lam= optimal_lam_m24,
        max_depth=20,
        filter_times=(8, 210),
        limits_rho=(8, 42),
        limits_depth=(0, 20),
        limits_rhoa=(5, 35),
        fname=f'M024_noise_floor_0.025.png'
    )

    survey_0522.plot_inversion(
        subset=['M024'],
        layer_type='dict',
        layers={0:1, 5:1.5},
        lam= optimal_lam_m24,
        max_depth=20,
        filter_times=(8, 210),
        limits_rho=(8, 42),
        limits_depth=(0, 20),
        limits_rhoa=(5, 35),
        noise_floor=0.05,
        fname=f'M024_noise_floor_0.05.png'
    )

    survey_0522.plot_inversion(
        subset=['M024'],
        layer_type='dict',
        layers={0:1, 5:1.5},
        lam= optimal_lam_m24,
        max_depth=20,
        filter_times=(8, 210),
        limits_rho=(8, 42),
        limits_depth=(0, 20),
        limits_rhoa=(5, 35),
        noise_floor=0.08,
        fname=f'M024_noise_floor_0.08.png'
    )

    # Testing normalization
    survey_0522.lambda_analysis_comparison(
        sounding='M010',
        layer_type='dict',
        layers={0:1, 5:1.5},
        max_depth=20,
        test_range=(10, 1000, 20),
        filter_times=(8, 210),
        fname=f'M010_normalization_true.png'
    )

    survey_0522.lambda_analysis_comparison(
        sounding='M010',
        layer_type='dict',
        layers={0:1, 5:1.5},
        max_depth=20,
        test_range=(10, 1000, 20),
        filter_times=(8, 210),
        normalize=False,
        fname=f'M010_normalization_false.png'
    )

    #%% Inversion of all soundings
    for sounding in [f'M{i:03d}' for i in range(1, 46) if i not in erroneous_soundings_0522]:
        opt_lam = survey_0522.analyse_inversion_gradient_curvature(
            sounding=sounding,
            layer_type='dict',
            layers={0:1, 5:1.5},
            max_depth=20,
            test_range=(10, 1000, 20),
            filter_times=(8, 210),
            fname=False
        )

        survey_0522.optimised_inversion_plot(
            sounding=sounding,
            layer_type='dict',
            layers={0:1, 5:1.5},
            lam= opt_lam,
            max_depth=20,
            filter_times=(8, 210),
            test_range=(10, 1000, 20),
            limits_rho=(8, 42),
            limits_depth=(0, 20),
            limits_rhoa=(5, 35),
            fname=f'optimised_{sounding}.png'
        )

    for sounding in [f'M{i:03d}' for i in erroneous_soundings_0522]:
        opt_lam = survey_0522.analyse_inversion_gradient_curvature(
            sounding=sounding,
            layer_type='dict',
            layers={0:1, 5:1.5},
            max_depth=20,
            test_range=(10, 1000, 20),
            filter_times=(8, 210),
            fname=False
        )

        survey_0522.optimised_inversion_plot(
            sounding=sounding,
            layer_type='dict',
            layers={0:1, 5:1.5},
            lam= opt_lam,
            max_depth=20,
            filter_times=(8, 210),
            test_range=(10, 1000, 20),
            limits_rho=(8, 42),
            limits_depth=(0, 20),
            limits_rhoa=(5, 35),
            fname=f'optimised_{sounding}_err.png'
        )