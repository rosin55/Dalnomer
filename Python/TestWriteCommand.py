# Чтение информации COM порта и печатает результаты в консоль.
import sys, glob, time, serial, os, struct, subprocess, threading, struct

ser = serial.Serial()

# reading_bytes = 10

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
ser.port = 'COM9'
ser.baudrate = '9600'
ser.timeout = 1
ser.bytesize = 8
ser.parity = 'N'
ser.stopbits = 1
ser.open()
# command = [ord('C'), ord('\n'), ord('\r')]
for i in range(254):
	print(i)
	ser.write(i)
	s = ser.readline(1)
	print(s)
# ser.write(command)

mesage_s = []
for i in range(6):
	s = ser.readline()
	mesage_s.append(s[:-2])
ser.close()
print(mesage_s)
                