import matplotlib.pyplot as plt
import numpy as np


def plot_growth(values, y_lab, title):
    x = np.array([i / 12 for i in range(len(values))])

    if len(values) <= 24:
        x *= 12
        x_lab = 'Month'
    else:
        x_lab = 'Year'

    pos_val = values.copy()
    neg_val = values.copy()

    pos_val[pos_val <= 0] = np.nan
    neg_val[neg_val > 0] = np.nan

    plt.figure()
    plt.plot(x, pos_val, color='g')
    plt.plot(x, neg_val, color='r')
    plt.grid()

    plt.title(title)
    plt.xlabel(x_lab)
    plt.ylabel(y_lab)
