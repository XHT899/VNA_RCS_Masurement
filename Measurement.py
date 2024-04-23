import pyvisa
#import time
import numpy as np
import matplotlib.pyplot as plt
rm = pyvisa.ResourceManager()
vna_address = 'TCPIP0::169.254.52.221::inst0::INSTR'  # 根据连接电脑以太网的ipv4地址设置矢网仪的IP地址
vna = rm.open_resource(vna_address)
def setup_s_parameter(channel, parameter):
    vna.write(f'DISP:WIND{channel}:STATE ON') #激活该窗口 
    vna.write(f'CALC:PAR:DEF "test{parameter}",{parameter}') #选择测量参数为S参数
    vna.write(f'DISP:WIND{channel}:TRAC{channel}:FEED "test{parameter}"') #在窗口中显示该参数
    vna.write('CALC:FUNC:STAT ON')          #打开激活窗口的轨迹统计
    
# 获取S参数数据
def fetch_s_parameter_amplitude(channel):
    vna.write(f'display:window{channel}:trace{channel}:select')#激活窗口1的轨迹
    vna.write('CALC:FORM MLOG')      # 设置数据格式为对数格式
    #vna.write(f'CALC{channel}:DATA? FDATA')  # 获取S参数的复数数据
    
    data = vna.query('CALC:DATA? FDATA')        #获取Ｓ参数的幅值，单位ｄＢ
    
    data=data.split(',')
    data=[float(num) for num in data]
    vna.write(f'CALCulate{channel}:TRANsform:TIME:STATe ON') 
    vna.write(f'display:window{channel}:trace{channel}:y:scale:auto ')#把窗口的自动比例打开
    return data
def fetch_s_parameter_complex (channel):
    vna.write(f'display:window{channel}:trace{channel}:select')#激活窗口1的轨迹
    vna.write('CALC:FORM MLOG')      # 设置数据格式为对数格式
    #vna.write(f'CALC{channel}:DATA? FDATA')  # 获取S参数的复数数据
    
    data_phase = vna.query('CALC:DATA? SDAT')        #获取Ｓ参数的实部与虚部
    
    data_phase=data_phase.split(',')
    data_phase=[float(num) for num in data_phase]
    return data_phase
#setup_s_parameter(1, 'S11')
setup_s_parameter(1, 'S21')
#setup_s_parameter(3, 'S12')
#setup_s_parameter(4, 'S22')

# 设置各个S参数
vna.write('INIT:IMM; *WAI')  # 开始扫描并等待扫描完成
vna.write(' :INITiate:CONTinuous  OFF') 
# 获取各个S参数的数据
#s11_amplitude = fetch_s_parameter_amplitude(1)
s21_amplitude = fetch_s_parameter_amplitude(2)
#s12_amplitude = fetch_s_parameter_amplitude(3)
#s22_amplitude = fetch_s_parameter_amplitude(4)
s21_complex = fetch_s_parameter_complex(2)
with open('s21_amplitude.txt', 'w') as file:
    for value in s21_amplitude:
        file.write(f"{value}\n")
with open('s21_complex.txt', 'w') as file:
    for i in range(0, len(s21_complex), 2):  # 步长为2，因为数据是实部和虚部成对出现
        file.write(f"{s21_complex[i]}, {s21_complex[i+1]}\n")
s21_real=s21_complex[0::2]
s21_imaginary=s21_complex[1::2]
complex_array = np.array(s21_real) + 1j * np.array(s21_imaginary)
s21_amp=np.abs(complex_array)
time_domain_signal = np.fft.ifft(complex_array)
time_domain_signal_real = np.real(time_domain_signal)
time_domain_signal_db=10*np.log10(time_domain_signal)
time_domain_signal_db= time_domain_signal_db[:len(time[time <= 100])]  # 限制在100ns内
vna.close()
