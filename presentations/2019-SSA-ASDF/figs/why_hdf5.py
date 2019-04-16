import io
import h5py

with h5py.File("asdf_test.h5", "r") as h5:
    events = h5["QuakeML"][:]
