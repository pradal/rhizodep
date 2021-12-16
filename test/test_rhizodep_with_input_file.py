# -*- coding: latin-1 -*-
import numpy as np
from rhizodep.simulation import *

# outputs directory path
OUTPUTS_DIRPATH = 'outputs'

# desired outputs filenames
DESIRED_RESULTS_FILENAME = 'desired_simulation_results.csv'

# actual outputs filenames
ACTUAL_RESULTS_FILENAME = 'actual_simulation_results.csv'

PRECISION = 6
RELATIVE_TOLERANCE = 10 ** -PRECISION
ABSOLUTE_TOLERANCE = RELATIVE_TOLERANCE


def compare_actual_to_desired(data_dirpath, desired_data_filename, actual_data_filename, overwrite_desired_data=False):
    """
    Function that compares the actual simulation results to desired simulation results.
    An exception is raised if the actual results do not matched the desired ones.

    :param str data_dirpath: The directory path were the simulation results are stored.
    :param str desired_data_filename: The filename of the desired simulation results.
    :param str actual_data_filename: The filename of the actual simulation results.
    :param bool overwrite_desired_data: If True, the desired simulation results are overwritten by the actual simulation results.
    """
    # read desired results
    desired_data_filepath = os.path.join(data_dirpath, desired_data_filename)
    desired_data_df = pd.read_csv(desired_data_filepath)

    # read actual results
    actual_data_filepath = os.path.join(data_dirpath, actual_data_filename)
    actual_data_df = pd.read_csv(actual_data_filepath)

    if overwrite_desired_data:
        # in case we want to update the desired data when the model was changed on purpose
        desired_data_filepath = os.path.join(data_dirpath, desired_data_filename)
        actual_data_df.to_csv(desired_data_filepath, na_rep='NA', index=False)
    else:
        # keep only numerical data
        for column in ([]):
            if column in desired_data_df.columns:
                assert desired_data_df[column].equals(actual_data_df[column])
                del desired_data_df[column]
                del actual_data_df[column]

    # compare to the desired data
    np.testing.assert_allclose(actual_data_df.values, desired_data_df.values, RELATIVE_TOLERANCE, ABSOLUTE_TOLERANCE)


def run_ref_simulation_with_input_file():
    # We initiate the properties of the MTG "g":
    g = model.initiate_mtg(random=True)

    # We launch the main simulation program:
    print("Simulation starts ...")
    main_simulation(g, simulation_period_in_days=20., time_step_in_days=1. / 24., radial_growth="Possible",
                    ArchiSimple=False,
                    # property="net_hexose_exudation_rate_per_day_per_cm", vmin=1e-9, vmax=1e-6, log_scale=True, cmap='jet',
                    property="C_hexose_root", vmin=1e-4, vmax=1e-1, log_scale=True, cmap='jet',
                    # property="C_sucrose_root", vmin=1e-4, vmax=1e2, log_scale=True, cmap='brg',
                    # property="C_hexose_reserve", vmin=1e-4, vmax=1e4, log_scale=True, cmap='brg',
                    input_file=os.path.join("inputs", "sucrose_input_0047.csv"),
                    constant_sucrose_input_rate=5e-9,
                    constant_soil_temperature_in_Celsius=20,
                    nodules=False,
                    simulation_results_file=os.path.join(OUTPUTS_DIRPATH, ACTUAL_RESULTS_FILENAME),
                    x_center=0, y_center=0, z_center=-1, z_cam=-2,
                    camera_distance=4, step_back_coefficient=0., camera_rotation=False, n_rotation_points=12 * 10,
                    z_classification=False, z_min=0.00, z_max=1., z_interval=0.05,
                    recording_images=True,
                    printing_sum=False,
                    recording_sum=True,
                    printing_warnings=False,
                    recording_g=True,
                    recording_g_properties=False,
                    random=True)


def test_run(overwrite_desired_data=False):
    """
    Run a test that compare the results of a reference simulation of RhizoDep that uses an input file, to desired simulation results.
    An exception is raised if the actual results do not matched the desired ones.

    :param bool overwrite_desired_data: If True, the desired simulation results are overwritten by the actual simulation results.
    """
    # run the reference simulation
    run_ref_simulation_with_input_file()

    # compare actual to desired outputs (an exception is raised if the test failed)
    print('Compare {} to {}'.format(ACTUAL_RESULTS_FILENAME, DESIRED_RESULTS_FILENAME))
    compare_actual_to_desired(OUTPUTS_DIRPATH, DESIRED_RESULTS_FILENAME, ACTUAL_RESULTS_FILENAME, overwrite_desired_data)
    print('{} OK!'.format(ACTUAL_RESULTS_FILENAME))


if __name__ == '__main__':
    test_run(overwrite_desired_data=False)
