# Чтение информации COM порта
import sys, glob, time, serial, os, struct, subprocess, threading, struct

ser = serial.Serial()

reading_bytes = 10

# ports = ['COM7']
# result = []
#     for port in ports:
#         try:
#             s = serial.Serial(port)
#             s.close()
#             result.append(port)
#         except (OSError, serial.SerialException):
#             pass

ser.close()
ser.port = 'COM7'
ser.baudrate = '9600'
ser.timeout = 10
ser.bytesize = 8
ser.parity = 'N'
ser.stopbits = 1
ser.open()
mesage_s = ser.readline()
print(mesage_s)
ser.close()
                