# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 13:54:08 2024

@author: Administrator
"""
import tkinter as tk
from tkinter import messagebox
import pyvisa
import numpy as np

def measure():
    try:
        # 获取用户输入的参数
        start_freq = float(start_freq_entry.get()) * 1e9  # 转换为Hz
        stop_freq = float(stop_freq_entry.get()) * 1e9    # 转换为Hz
        points = int(points_entry.get())
        bandwidth = float(bandwidth_entry.get()) * 1e3    # 转换为Hz
        power_level = float(power_level_entry.get())

        # 设置仪器
        rm = pyvisa.ResourceManager()
        vna = rm.open_resource(vna_address.get())
        vna.timeout = 10000
        vna.write('*RST')
        vna.write(f'SENS:BWID {bandwidth}')
        vna.write(':SENSe1:SWEep:TYPE LIN')
        vna.write(f':SENS:FREQ:STAR {start_freq}')
        vna.write(f':SENS:FREQ:STOP {stop_freq}')
        vna.write(f':SENSe1:SWEep:POINts {points}')
        vna.write(':SENSe1:SWEep:TIME:AUTO ON')
        vna.write(f':SOUR:POW {power_level}dBm')
        vna.close()

        messagebox.showinfo("Success", "Parameters Set successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# 创建主窗口
root = tk.Tk()
root.title("VNA Measurement Setup")

# 创建标签和输入字段
tk.Label(root, text="Start Frequency (GHz):").grid(row=0, column=0)
start_freq_entry = tk.Entry(root)
start_freq_entry.grid(row=0, column=1)

tk.Label(root, text="Stop Frequency (GHz):").grid(row=1, column=0)
stop_freq_entry = tk.Entry(root)
stop_freq_entry.grid(row=1, column=1)

tk.Label(root, text="Points:").grid(row=2, column=0)
points_entry = tk.Entry(root)
points_entry.grid(row=2, column=1)

tk.Label(root, text="Bandwidth (kHz):").grid(row=3, column=0)
bandwidth_entry = tk.Entry(root)
bandwidth_entry.grid(row=3, column=1)

tk.Label(root, text="Power Level (dBm):").grid(row=4, column=0)
power_level_entry = tk.Entry(root)
power_level_entry.grid(row=4, column=1)

tk.Label(root, text="VNA Address:").grid(row=5, column=0)
vna_address = tk.Entry(root)
vna_address.grid(row=5, column=1)

# 创建按钮
measure_button = tk.Button(root, text="Measure", command=measure)
measure_button.grid(row=6, column=1)

# 启动事件循环
root.mainloop()
