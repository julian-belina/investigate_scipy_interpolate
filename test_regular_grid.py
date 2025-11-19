#  %%
import pathlib

import numpy as np
import pandas as pd

from scipy.interpolate import RegularGridInterpolator
from matplotlib import pyplot

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

# linear_interpolator = LinearNDInterpolator(
#     list(zip(point_1_T_.loc[selected_slice], point_2_RH_.loc[selected_slice])),
#     total_electricity.loc[selected_slice],
# )
# linear_interpolator_output = linear_interpolator(
#     surface_air_temperature[selected_slice, :], relative_humidity[selected_slice, :]
# )

combined_data_set = pd.DataFrame(
    data=[point_1_T_, point_2_RH_, total_electricity]
).transpose()
sorted_df = combined_data_set.sort_values(by=["T", "RH"])


x_unique = np.sort(combined_data_set["T"].unique())
y_unique = np.sort(combined_data_set["RH"].unique())

# 2. Pivot to 2D grid
Z = (
    combined_data_set.pivot(index="T", columns="RH", values="totalElectricity")
    .reindex(index=x_unique, columns=y_unique)
    .values
)

# 3. Build interpolator
f = RegularGridInterpolator((x_unique, y_unique), Z)


regular_interpolator_output = f(
    (
        surface_air_temperature[selected_slice, :],
        relative_humidity[selected_slice, :],
    )
)
# pass
# regular_grid_inerpolator.[
#     surface_air_temperature[selected_slice, :],
#     relative_humidity[selected_slice, :],
# ]
# points sind (x,y) punkte
# Values sind f(x,y)
# xi sind die stellen wo interpoliert wird
# Compare interpolation data
elec_test_array = np.genfromtxt(fname=current_dir.joinpath("elec.csv"), delimiter=",")
#  %%

fig, axs = pyplot.subplots(nrows=1, ncols=1)


# np.testing.assert_allclose(actual=regular_interpolator_output, desired=elec_test_array)


axs.plot(
    regular_interpolator_output,
    "k--",
)
axs.plot(elec_test_array, "b")


fig.show()

pass

# %%
