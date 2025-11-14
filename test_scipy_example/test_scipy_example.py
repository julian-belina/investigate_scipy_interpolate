import pathlib

import numpy as np
from scipy.interpolate import griddata

test_data_path = pathlib.Path(__file__).parent


def func(x, y):
    return x * (1 - x) * np.cos(4 * np.pi * x) * np.sin(4 * np.pi * y**2) ** 2


grid_x, grid_y = np.mgrid[0:1:100j, 0:1:200j]
rng = np.random.default_rng()
points = rng.random((1000, 2))
values = func(points[:, 0], points[:, 1])


grid_z0 = griddata(points, values, (grid_x, grid_y), method="nearest")
grid_z1 = griddata(points, values, (grid_x, grid_y), method="linear")
grid_z2 = griddata(points, values, (grid_x, grid_y), method="cubic")

np.savetxt(fname=test_data_path.joinpath("grid_z0.csv"), X=grid_z0, delimiter=",")
np.savetxt(fname=test_data_path.joinpath("grid_z1.csv"), X=grid_z1, delimiter=",")
np.savetxt(fname=test_data_path.joinpath("grid_z2.csv"), X=grid_z2, delimiter=",")

grid_z0_test = np.genfromtxt(
    fname=test_data_path.joinpath("grid_z0.csv"), delimiter=","
)
grid_z1_test = np.genfromtxt(
    fname=test_data_path.joinpath("grid_z1.csv"), delimiter=","
)
grid_z2_test = np.genfromtxt(
    fname=test_data_path.joinpath("grid_z2.csv"), delimiter=","
)

np.testing.assert_allclose(actual=grid_z0, desired=grid_z0_test)
np.testing.assert_allclose(actual=grid_z1, desired=grid_z1_test)
np.testing.assert_allclose(actual=grid_z2, desired=grid_z2_test)
