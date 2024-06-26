# -*- coding: utf-8 -*-
"""
Created on Wed May 29 10:42:05 2024

@author: taylor
"""
from scipy.fft import fft, ifft
from scipy.signal import get_window, windows, filtfilt, butter
#import time
import numpy as np
import matplotlib.pyplot as plt
Background = 'C:\\Users\\taylor\\Desktop\\0625\\3m背景.npy'
Antennagain = 'C:\\Users\\taylor\\Desktop\\0529\\03\\新天线增益.npy'
Target = 'C:\\Users\\taylor\\Desktop\\0625\\3m 25cm目标.npy'
c = 3e8  # 光速，单位为m/s

start_freq = 14e9             # 起始频率，单位为Hz
stop_freq = 16e9             # 终止频率，单位为Hz
points = 401                # 扫描点数
pi=3.1415926535 
frequency = np.linspace(start_freq, stop_freq, points)
frequency_resolution = frequency[1] - frequency[0]
time_duration = 1 / frequency_resolution
time = np.linspace(0, time_duration, points, endpoint=False)
time *= 1e9  # 将时间转换为纳秒
distance = (c * time * 1e-9) / 2  # 将时间转换为距离，单位为米
λ=c/frequency
background_complex_array = np.load(Background)
target_complex_array = np.load(Target)
Gain=np.load(Antennagain)
linear_gain = 10 ** (Gain / 10)
background_retrieved_complex_array = target_complex_array - background_complex_array
#window = get_window(('hann'), len(background_retrieved_complex_array))
#background_retrieved_complex_array = background_retrieved_complex_array * window
s21_amp = np.abs(background_retrieved_complex_array)

time_domain_signal = np.fft.ifft(background_retrieved_complex_array)


start =50  # 例如，感兴趣段落从索引253开始
end = 53
  # 例如，感兴趣段落到索引280结束
suppression_factor = 0.001  # 非目标区域的抑制因子
window_type = 'boxcar'  # 可以选择 'hann', 'hamming', 'blackman', 'gaussian' 等
window_length = end - start
window = get_window(window_type, window_length)
full_window = np.ones_like(time_domain_signal) * suppression_factor
full_window[start:end] = window
windowed_data = time_domain_signal * full_window
frequency_domain_data = fft(windowed_data)

RCS=frequency_domain_data**2 / (linear_gain[2600:3001]**2) / (λ**2) * (4*pi**3) * (2.2**4)

time_domain_signal_amp = np.abs(time_domain_signal)
time_domain_signal_db = 20 * np.log10(time_domain_signal_amp)

windowed_data_amp = np.abs(windowed_data)
windowed_data_db = 20 * np.log10(windowed_data_amp)

frequency_domain_data_amp = np.abs(RCS)
frequency_domain_data_amp_db = 10 * np.log10(frequency_domain_data_amp)

# 将时间转换为距离


# 绘制时域信号
plt.figure(figsize=(10, 6))
plt.rcParams.update({'font.size': 20})
plt.plot(distance[time <= 200], time_domain_signal_db)
plt.title('2m Target')
plt.xlabel('Distance (m)')
plt.ylabel('Amplitude')
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 6))
plt.rcParams.update({'font.size': 20})
plt.plot(distance[time <= 200], windowed_data_db)
plt.title('2m Windowed Data')
plt.xlabel('Distance (m)')
plt.ylabel('Amplitude')
plt.grid(True)
plt.show()



plt.figure(figsize=(10, 6))
plt.rcParams.update({'font.size': 20})
plt.plot(frequency, frequency_domain_data_amp_db)
#plt.xticks([0.25e10, 0.5e10, 0.75e10, 1.0e10,1.25e10,1.5e10,1.75e10], ['2.5', '5', '7.5', '10','12.5','15','17.5'])
plt.title('5m Windowed Data In Frequency Domain')
plt.xlabel('Frequency (GHz)')
plt.ylabel('Amplitude')
plt.grid(True)
plt.show()

RCS_Mean = np.mean(frequency_domain_data_amp_db)
