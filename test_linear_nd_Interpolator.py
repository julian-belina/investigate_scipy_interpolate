import pathlib

import numpy as np
import pandas as pd
from scipy.interpolate import LinearNDInterpolator


current_dir = pathlib.Path(__file__).parent

# get data
dac_data = pd.read_csv(current_dir.joinpath("dac_data.csv"))
point_1_T_ = dac_data.loc[:, "T"]
point_2_RH_ = dac_data.loc[:, "RH"]
total_electricity = dac_data.loc[:, "totalElectricity"]
relative_humidity = np.genfromtxt(
    fname=current_dir.joinpath("relative_humidity.csv"), delimiter=","
)
surface_air_temperature = np.genfromtxt(
    current_dir.joinpath("surface_air_temperature.csv"), delimiter=","
)

# Define interpolation
selected_slice = slice(0, 140)

# elec = griddata(
#     points=(point_1_T_.loc[selected_slice], point_2_RH_.loc[selected_slice]),
#     values=total_electricity.loc[selected_slice],
#     xi=(
#         surface_air_temperature[selected_slice, :],
#         relative_humidity[selected_slice, :],
#     ),
#     method="linear",
# )

linear_interpolator = LinearNDInterpolator(
    list(zip(point_1_T_.loc[selected_slice], point_2_RH_.loc[selected_slice])),
    total_electricity.loc[selected_slice],
)
linear_interpolator_output = linear_interpolator(
    surface_air_temperature[selected_slice, :], relative_humidity[selected_slice, :]
)


pass
# regular_grid_inerpolator.[
#     surface_air_temperature[selected_slice, :],
#     relative_humidity[selected_slice, :],
# ]
# points sind (x,y) punkte
# Values sind f(x,y)
# xi sind die stellen wo interpoliert wird
# Compare interpolation data
elec_test_array = np.genfromtxt(fname=current_dir.joinpath("elec.csv"), delimiter=",")
np.testing.assert_allclose(actual=linear_interpolator_output, desired=elec_test_array)

pass
