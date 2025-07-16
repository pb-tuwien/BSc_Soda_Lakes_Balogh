#%% 
import TEM_tools as te
from pathlib import Path
from filtering_20241008 import root_path, tem_data, tem_coords, rename_points_1008
from filtering_20241008 import parsing_coords_1008, erroneous_soundings_1008

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

#%% Example sounding: M006
    # Testing max depth for inversion
    optimal_lam_m06 = survey_1008.analyse_inversion_gradient_curvature(
        sounding='M006',
        layer_type='dict',
        layers={0:1, 5:1.5},
        max_depth=20,
        test_range=(10, 1000, 20),
        filter_times=(12, 80),
        noise_floor=0.08,
        fname=False
    )

    survey_1008.plot_inversion(
        subset=['M006'],
        layer_type='dict',
        layers={0:1, 5:1.5},
        lam= optimal_lam_m06,
        max_depth=10,
        filter_times=(12, 80),
        limits_rho=(8, 45),
        limits_depth=(0, 20),
        limits_rhoa=(10, 20),
        fname=f'M006_max_depth_10m.png'
    )

    survey_1008.plot_inversion(
        subset=['M006'],
        layer_type='dict',
        layers={0:1, 5:1.5},
        lam= optimal_lam_m06,
        max_depth=20,
        filter_times=(12, 80),
        limits_rho=(8, 45),
        limits_depth=(0, 20),
        limits_rhoa=(10, 20),
        fname=f'M006_max_depth_20m.png'
    )

    #%% Testing noise floor
    optimal_lam_m60 = survey_1008.analyse_inversion_gradient_curvature(
        sounding='M060',
        layer_type='dict',
        layers={0:1, 5:1.5},
        max_depth=20,
        test_range=(10, 1000, 20),
        filter_times=(12, 80),
        noise_floor=0.08,
        fname=False
    )

    survey_1008.plot_inversion(
        subset=['M060'],
        layer_type='dict',
        layers={0:1, 5:1.5},
        lam= optimal_lam_m60,
        max_depth=20,
        filter_times=(12, 80),
        limits_rho=(8, 60),
        limits_depth=(0, 20),
        limits_rhoa=(10, 48),
        fname=f'M060_noise_floor_0.025.png'
    )

    survey_1008.plot_inversion(
        subset=['M060'],
        layer_type='dict',
        layers={0:1, 5:1.5},
        lam= optimal_lam_m60,
        max_depth=20,
        filter_times=(12, 80),
        limits_rho=(8, 60),
        limits_depth=(0, 20),
        limits_rhoa=(10, 48),
        noise_floor=0.05,
        fname=f'M060_noise_floor_0.05.png'
    )

    survey_1008.plot_inversion(
        subset=['M060'],
        layer_type='dict',
        layers={0:1, 5:1.5},
        lam= optimal_lam_m60,
        max_depth=30,
        filter_times=(12, 80),
        limits_rho=(8, 60),
        limits_depth=(0, 20),
        limits_rhoa=(10, 48),
        noise_floor=0.08,
        fname=f'M060_noise_floor_0.08.png'
    )

    #%% Inversion of all soundings
    for sounding in [f'M{i:03d}' for i in range(1, 67) if i not in erroneous_soundings_1008]:
        opt_lam = survey_1008.analyse_inversion_gradient_curvature(
            sounding=sounding,
            layer_type='dict',
            layers={0:1, 5:1.5},
            max_depth=20,
            test_range=(10, 1000, 20),
            filter_times=(12, 80),
            noise_floor=0.08,
            fname=False
        )

        survey_1008.optimised_inversion_plot(
            sounding=sounding,
            layer_type='dict',
            layers={0:1, 5:1.5},
            lam= opt_lam,
            max_depth=20,
            filter_times=(12, 80),
            noise_floor=0.08,
            test_range=(10, 1000, 20),
            limits_rho=(0, 80),
            limits_depth=(0, 20),
            limits_rhoa=(0, 50),
            fname=f'optimised_{sounding}.png'
        )

    for sounding in [f'M{i:03d}' for i in erroneous_soundings_1008]:
        opt_lam = survey_1008.analyse_inversion_gradient_curvature(
            sounding=sounding,
            layer_type='dict',
            layers={0:1, 5:1.5},
            max_depth=20,
            test_range=(10, 1000, 20),
            filter_times=(12, 80),
            noise_floor=0.08,
            fname=False
        )

        survey_1008.optimised_inversion_plot(
            sounding=sounding,
            layer_type='dict',
            layers={0:1, 5:1.5},
            lam= opt_lam,
            max_depth=20,
            filter_times=(12, 80),
            noise_floor=0.08,
            test_range=(10, 1000, 20),
            limits_rho=(0, 80),
            limits_depth=(0, 20),
            limits_rhoa=(0, 100),
            fname=f'optimised_{sounding}_err.png'
        )
    
    # # Inversion of M047: Elliptic curve
    # survey_1008.optimised_inversion_plot(
    #     sounding='M047',
    #     layer_type='dict',
    #     layers={0: 1, 5: 1.5, 15: 2},
    #     max_depth=30,
    #     test_range=(10, 1000, 20),
    #     filter_times=(12, 80),
    #     lam=113,
    #     fname='inversion_ellipse_curve_visual_20241008.png'
    # )

    # # Inversion of M040: Sharp curve
    # survey_1008.optimised_inversion_plot(
    #     sounding='M040',
    #     layer_type='dict',
    #     layers={0: 1, 5: 1.5, 15: 2},
    #     max_depth=30,
    #     test_range=(10, 1000, 20),
    #     filter_times=(12, 80),
    #     lam=298,
    #     fname='inversion_sharp_curve_grad_20241008.png'
    # )
    # survey_1008.optimised_inversion_plot(
    #     sounding='M040',
    #     layer_type='dict',
    #     layers={0: 1, 5: 1.5, 15: 2},
    #     max_depth=30,
    #     test_range=(10, 1000, 20),
    #     filter_times=(12, 80),
    #     lam=627,
    #     fname='inversion_sharp_curve_golden_20241008.png'
    # )

    # for sounding in [f'M{i:03d}' for i in range(1, 67) if i not in erroneous_soundings_1008]:
    #     survey_1008.optimised_inversion_plot(
    #         sounding=sounding,
    #         layer_type='dict',
    #         layers={0: 1, 5: 1.5, 15: 2},
    #         max_depth=30,
    #         test_range=(10, 1000, 20),
    #         filter_times=(12, 80),
    #         lam=113,
    #         fname=f'inversion_{sounding}_113_20241008.png'
    #     )

    # for sounding in [f'M{i:03d}' for i in erroneous_soundings_1008]:
    #     survey_1008.optimised_inversion_plot(
    #         sounding=sounding,
    #         layer_type='dict',
    #         layers={0: 1, 5: 1.5, 15: 2},
    #         max_depth=30,
    #         test_range=(10, 1000, 20),
    #         filter_times=(12, 80),
    #         lam=113,
    #         fname=f'inversion_{sounding}_113_20241008_err.png'
    #     )