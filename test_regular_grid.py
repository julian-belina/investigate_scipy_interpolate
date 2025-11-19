#  %%
import pathlib
import numpy as np
import pandas as pd
from scipy.interpolate import RegularGridInterpolator
#from matplotlib import pyplot

current_dir = pathlib.Path(__file__).parent

# get data
dac_data = pd.read_csv(current_dir.joinpath("dac_data.csv"), index_col=0)
point_1_T_ = dac_data.loc[:, "T"]
point_2_RH_ = dac_data.loc[:, "RH"]
total_electricity = dac_data.loc[:, "totalElectricity"]
relative_humidity = np.genfromtxt(
    fname=current_dir.joinpath("relative_humidity.csv"), delimiter=","
)

surface_air_temperature = np.genfromtxt(
    current_dir.joinpath("surface_air_temperature.csv"), delimiter=","
)

#2nd dac dataset:
dac_data2 = pd.read_csv(current_dir.joinpath("LT_sendi.csv"), index_col=0)


# %% 
# Define interpolation

#For RegularGridInterpolator, the data needs unique x/y vectors with a corresponding z matrix
dac_data_pivot = dac_data.pivot_table(values='totalElectricity', index='T', columns='RH')

#RGI:
values = dac_data_pivot.values
points = dac_data_pivot.index.values, dac_data_pivot.columns.values.astype('float64')
RGI = RegularGridInterpolator(points=points, values=values)
RGI_output = RGI((
    surface_air_temperature,
    relative_humidity,
))

#Load testdata (from old, griddata() interpolation)
elec_test_array = np.genfromtxt(fname=current_dir.joinpath("elec.csv"), delimiter=",")

#Load new testdata with RGI:
elec_RGI_test_array = np.genfromtxt(fname=current_dir.joinpath("elec_RGI.csv"), delimiter=",")

#  %% Plotting 
# fig, axs = pyplot.subplots(nrows=1, ncols=1)


# axs.plot(
#     RGI_output,
#     "k--",
# )
# axs.plot(elec_test_array, "b", linewidth=0.5)


# fig.show()

# perc_deviation = (elec_test_array - RGI_output) / elec_test_array * 100
# perc_deviation.mean() #-0.015562724915809874%
# perc_deviation.max() #0.6990781200055962%

# %% Testing

np.testing.assert_allclose(actual=RGI_output, desired=elec_RGI_test_array)

