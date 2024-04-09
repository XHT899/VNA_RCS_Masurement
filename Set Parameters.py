import pyvisa
#import time
import numpy as np
import matplotlib.pyplot as plt
rm = pyvisa.ResourceManager()
instruments = rm.list_resources()
print(instruments)  # 打印所有连接的仪器VISA地址
vna_address = 'TCPIP0::169.254.52.221::inst0::INSTR'  # 根据连接电脑以太网的ipv4地址设置矢网仪的IP地址
vna = rm.open_resource(vna_address)
vna.timeout = 10000             # 设置超时时间，单位ms 
start_freq = 14e9             # 起始频率，单位为Hz
stop_freq = 16e9              # 终止频率，单位为Hz
points = 201                    # 扫描点数
bandwidth= 1e3                  # 中频带宽
#antenna gain_1=                # 端口1天线增益
#antenna gain_2=                # 端口2天线增益
idn = vna.query('*IDN?')        # 查询当前设备信息
frequency = np.linspace(start_freq, stop_freq, points)
frequency_resolution = frequency[1] - frequency[0]
time_duration = 1 / frequency_resolution
time = np.linspace(0, time_duration, points, endpoint=False)
time *= 1e9


#vna.write('CALC:NORM:INT ON ')      #设置内插模式打开
vna.write('*RST')                               # 复位矢网仪
vna.write(f'SENS:BWID {bandwidth}')             # 设置中频带宽
vna.write(':SENSe1:SWEep:TYPE LIN')             # 设置扫描模式为线性扫描
vna.write(f':SENS:FREQ:STAR {start_freq}')      # 设置起始频率
vna.write(f':SENS:FREQ:STOP {stop_freq}')       # 设置终止频率
vna.write(f':SENSe1:SWEep:POINts {points}')     # 设置扫描点数
vna.write(':SENSe1:SWEep:TIME:AUTO  ON')        #将扫描时间设置为自动
vna.write(':SOUR:POW  0dBm')                   #扫描功率电平设置为10dBm
#vna.write('SENSe1:COUPle ALL')                  #设置同时扫描 NONE为交替扫描


vna.close()




