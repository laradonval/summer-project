from glob import glob

import matplotlib.pyplot as plt
import numpy as np
from astropy.timeseries import LombScargle

columns = ("time", "magnitude", "magnitude_uncertainty", "dont worry about it")
needed_columns = columns[:3]

for data_file in glob("./*.dat"):
    t = []
    m = []
    dm = []
    with open(data_file, "r") as f:
        for line in f.read().split("\n"):
            if len(line) > 0:
                time, magnitude, uncertainty, _ = line.split(" ")
                t.append(float(time))
                m.append(float(magnitude))
                dm.append(float(uncertainty))

    ls = LombScargle(t, m, dm)
    frequency, power = ls.autopower()
    plt.plot(frequency, power)
    plt.title(data_file)
    plt.xlabel("frequency")
    plt.ylabel("power")
    plt.show()

    best_frequency = frequency[np.argmax(power)]
    t_fit = np.linspace(0, 1)
    y_fit = ls.model(t_fit, best_frequency)
    plt.plot(t_fit, y_fit)
    plt.title(data_file)
    plt.xlabel("time")
    plt.ylabel("magnitude")
    plt.show()
