# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 14:40:27 2024

@author: Administrator
"""

import tkinter as tk
from tkinter import messagebox
import pyvisa
import numpy as np

# 设备设置和测量函数
def setup_s_parameter(channel, parameter):
    vna.write(f'DISP:WIND{channel}:STATE ON')
    vna.write(f'CALC:PAR:DEF "test{parameter}",{parameter}')
    vna.write(f'DISP:WIND{channel}:TRAC{channel}:FEED "test{parameter}"')
    vna.write('CALC:FUNC:STAT ON')

def fetch_s_parameter_amplitude(channel):
    vna.write(f'display:window{channel}:trace{channel}:select')
    vna.write('CALC:FORM MLOG')
    data = vna.query('CALC:DATA? FDATA')
    data = data.strip().split(',')
    data = [float(num) for num in data]
    return data

def fetch_s_parameter_complex(channel):
    vna.write(f'display:window{channel}:trace{channel}:select')
    vna.write('CALC:FORM MLOG')
    data_phase = vna.query('CALC:DATA? SDAT')
    data_phase = data_phase.strip().split(',')
    data_phase = [float(num) for num in data_phase]
    return data_phase

def measure():
    try:
        start_freq = float(start_freq_entry.get()) * 1e9
        stop_freq = float(stop_freq_entry.get()) * 1e9
        points = int(points_entry.get())
        bandwidth = float(bandwidth_entry.get()) * 1e3
        power_level = float(power_level_entry.get())

        amplitude_filename = amplitude_filename_entry.get()
        complex_filename = complex_filename_entry.get()

        if not amplitude_filename or not complex_filename:
            messagebox.showerror("Error", "Please enter file names for both amplitude and complex data.")
            return

        vna.write('*RST')
        vna.write(f'SENS:BWID {bandwidth}')
        vna.write(':SENSe1:SWEep:TYPE LIN')
        vna.write(f':SENS:FREQ:STAR {start_freq}')
        vna.write(f':SENS:FREQ:STOP {stop_freq}')
        vna.write(f':SENSe1:SWEep:POINts {points}')
        vna.write(':SENSe1:SWEep:TIME:AUTO ON')
        vna.write(f':SOUR:POW {power_level}dBm')

        setup_s_parameter(1, 'S21')
        vna.write('INIT:IMM; *WAI')
        vna.write(' :INITiate:CONTinuous  OFF')
        
        s21_amplitude = fetch_s_parameter_amplitude(2)
        s21_complex = fetch_s_parameter_complex(2)

        amplitude_str = "\n".join(map(str, s21_amplitude))
        complex_str = "\n".join(f"{s21_complex[i]}, {s21_complex[i+1]}" for i in range(0, len(s21_complex), 2))

        amplitude_display.config(state=tk.NORMAL)
        amplitude_display.delete('1.0', tk.END)
        amplitude_display.insert(tk.END, amplitude_str)
        amplitude_display.config(state=tk.DISABLED)
        
        complex_display.config(state=tk.NORMAL)
        complex_display.delete('1.0', tk.END)
        complex_display.insert(tk.END, complex_str)
        complex_display.config(state=tk.DISABLED)
        
        with open(amplitude_filename, 'w') as file:
            file.write(amplitude_str)
        with open(complex_filename, 'w') as file:
            file.write(complex_str)

        messagebox.showinfo("Success", "Measurement completed and data saved!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI setup
root = tk.Tk()
root.title("VNA Measurement Setup")

# Parameter setting frame
setting_frame = tk.Frame(root)
setting_frame.pack(fill=tk.BOTH, expand=True)

tk.Label(setting_frame, text="Start Frequency (GHz):").grid(row=0, column=0)
start_freq_entry = tk.Entry(setting_frame)
start_freq_entry.grid(row=0, column=1)

tk.Label(setting_frame, text="Stop Frequency (GHz):").grid(row=1, column=0)
stop_freq_entry = tk.Entry(setting_frame)
stop_freq_entry.grid(row=1, column=1)

tk.Label(setting_frame, text="Points:").grid(row=2, column=0)
points_entry = tk.Entry(setting_frame)
points_entry.grid(row=2, column=1)

tk.Label(setting_frame, text="Bandwidth (kHz):").grid(row=3, column=0)
bandwidth_entry = tk.Entry(setting_frame)
bandwidth_entry.grid(row=3, column=1)

tk.Label(setting_frame, text="Power Level (dBm):").grid(row=4, column=0)
power_level_entry = tk.Entry(setting_frame)
power_level_entry.grid(row=4, column=1)

# File name inputs
tk.Label(setting_frame, text="Amplitude File Name:").grid(row=5, column=0)
amplitude_filename_entry = tk.Entry(setting_frame)
amplitude_filename_entry.grid(row=5, column=1)

tk.Label(setting_frame, text="Complex File Name:").grid(row=6, column=0)
complex_filename_entry = tk.Entry(setting_frame)
complex_filename_entry.grid(row=6, column=1)

# Measurement display frame
display_frame = tk.Frame(root)
display_frame.pack(fill=tk.BOTH, expand=True)

measure_button = tk.Button(display_frame, text="Measure S21", command=measure)
measure_button.pack()

amplitude_display = tk.Text(display_frame, height=25, width=100)
amplitude_display.pack()
amplitude_display.config(state=tk.DISABLED)

complex_display = tk.Text(display_frame, height=25, width=100)
complex_display.pack()
complex_display.config(state=tk.DISABLED)

# Setup VNA
rm = pyvisa.ResourceManager()
vna_address = 'TCPIP0::169.254.52.221::inst0::INSTR'
vna = rm.open_resource(vna_address)

root.mainloop()
