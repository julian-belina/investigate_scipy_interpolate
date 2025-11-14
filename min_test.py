import pathlib

import numpy as np
import pandas as pd
from scipy.interpolate import griddata

current_dir = pathlib.Path(__file__).parent

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

elec = griddata(
    points=(point_1_T_, point_2_RH_),
    values=total_electricity,
    xi=(
        surface_air_temperature,
        relative_humidity,
    ),
    method="linear",
)

elec_test_array = np.genfromtxt(fname=current_dir.joinpath("elec.csv"), delimiter=",")
np.testing.assert_allclose(actual=elec, desired=elec_test_array)
# assert np.allclose(a=elec, b=elec_test_array)
