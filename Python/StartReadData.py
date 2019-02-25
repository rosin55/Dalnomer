# Чтение информации COM порта и печатает результаты в консоль.
import sys, glob, time, serial, os, struct, subprocess, threading
# from serial.tools.list_ports import comports


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


ports = serial_ports()
message = 'Найден порт ' + ports[0]
print(message)

ser = serial.Serial()

ser.port = (ports[0])
ser.baudrate = '9600'
ser.timeout = 10
ser.bytesize = 8
ser.parity = 'N'
ser.stopbits = 1
ser.open()
time.sleep(2)  # ожидание открытия порта 

cmd = [ord('C')]
ser.write(cmd)

mesage_s = []
for i in range(6):
	s = ser.readline()
	mesage_s.append(s[:-2])
ser.close()
print(mesage_s)

# if __name__ == '__main__':
#     print(serial_ports())