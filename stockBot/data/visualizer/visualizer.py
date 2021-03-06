#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Wednesday, 19 March 2020
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

def plot_test_prediction(real_data, test_data, mse=False):
    """
        Plot predicted data above true data and compute the mean squared error.

            Parameters:
                real_data (pandas.Series) : True data
                test_data (pandas.Series) : Predicted data
                mse       (bool)          : Compute the mse or not
    """
    assert isinstance(real_data, pd.Series) and isinstance(test_data, pd.Series)

    plt.title("Predicted data above true data.")
    plt.xlabel('Date')
    plt.ylabel('Prices [$]')
    if mse:
        intersect = test_data.index.intersection(real_data.index)
        if len(intersect) > 0:
            df_intersect = real_data.loc[intersect]
            total_mse = mean_squared_error(df_intersect.values,test_data.values)
            plt.plot([],[],linestyle=' ',label="MSE : %.2f"%(total_mse))
    p0, = plt.plot(real_data.index, real_data.values, color='purple', linestyle='-', label='Real data')
    p1, = plt.plot(test_data.index, test_data.values, color='red', linestyle='--', label='Predicted data')
    return [p0, p1]

def plot_fourier(data):
    """
        Plot the fourier transform with differents numbers of components.

            Parameters:
                data (pandas.Series) : Data to fit with fourier transforms.
    """
    assert isinstance(data, pd.Series)

    plt.title('Fourier transform of stock prices.')
    plt.xlabel('Date')
    plt.ylabel('Price [$]')
    FFT = np.fft.fft(np.asarray(data.values.tolist())) # Get the fast fourier transform
    plots = []
    for num in [3, 6, 9, 15]:
        fft = np.copy(FFT)
        fft[num:-num] = 0
        ifft = np.fft.ifft(fft)
        p = plt.plot(pd.to_datetime(np.linspace(pd.Timestamp(data.index.values[0]).value,pd.Timestamp(data.index.values[-1]).value,len(ifft))), np.real(ifft), linestyle='--', label='Fourier transform with %d components'%num)
        plots.append(p)
    p = plt.plot(data.index,data.values, color='purple', ls='-', label='Real')
    plots.append(p)
    return plots


if __name__=='__main__':
    import yfinance as yf
    SPCE = yf.Ticker('SPCE')
    hist = SPCE.history(period='max')
    plt.figure()
    plot_fourier(hist['Close'])
    plt.legend()
    plt.show()
