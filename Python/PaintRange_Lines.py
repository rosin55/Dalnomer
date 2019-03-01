# Рисует график расстояний, измеренных УЗ дальномером
# и переданным в массив MassivTochek
# с помощью Lines(x, y)
# создан 27.01.2019

import pygame
import math
import sys, serial, time#, glob, os, struct, subprocess, threading

def serial_ports():
	# Возвращает список доступных СОМ портов
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

def PaintSimbol( s, x, y):
	text = font.render(s, 1, (COLOR_TEXT))
	place = text.get_rect(center = (x, (sc.get_height()-y)))
	sc.blit(text, place)

def PaintMetki():
	n_metok_x = int(sc.get_width()/20)
	n_metok_y = int(sc.get_height()/20)
	for i in range(n_metok_x):
		x = 20*i+10
		pygame.draw.line(sc, COLOR_LINE,\
			[x, (sc.get_height() - 10)], [x, (sc.get_height() - 15)])
	for i in range(n_metok_y):
		y = 20*i+10
		pygame.draw.line(sc, COLOR_LINE, [10, y],[15, y])

def InitCOM():
	# ser = serial.Serial()
	ser.close()
	ser.port = (ports[0])
	# ser.port = 'COM9'
	ser.baudrate = '9600'
	ser.timeout = 10
	ser.bytesize = 8
	ser.parity = 'N'
	ser.stopbits = 1
	ser.open()
	time.sleep(2)  # ожидание открытия порта

def ReadRangeFrom_COM():
	cmd = [ord('C')] # запуск сканирования
	ser.write(cmd)
	# range_s.clear()  # инициализация массива данных
	for i in range(6):
		s = ser.readline()
		range_s.append(s[:-2]) # удаление служебных символов в конце
	# ser.close()
	print(range_s)
	return(range_s)

def ReadRange100From_COM():
	cmd = [ord('S')] # запуск сканирования
	ser.write(cmd)
	for i in range(100):
		s = ser.readline()
		range_s.append(s[:-2]) # удаление служебных символов в конце
	# ser.close()
	print(range_s)
	return(range_s)

def PaintRange():
	""" Read data of range from COM port and paint diagram
	"""
	# Чтение данных с дальномера
	ReadRangeFrom_COM()
	# Расчет точек графика
	MassivTochekRange = []
	for i in range(len(range_s)):
		MassivTochekRange.append([50*i+10, (500 - 5 * int(range_s[i]))])
		print(MassivTochekRange[i])
	pygame.draw.lines(sc, COLOR_TEXT, False, MassivTochekRange,2)
	pygame.display.update()

def PaintRange100():
	""" Read data of range from COM port and paint diagram
	"""
	# Чтение данных с дальномера
	ReadRange100From_COM()
	# Расчет точек графика
	MassivTochekRange = []
	for i in range(len(range_s)):
		MassivTochekRange.append([10*i+10, (700 - 5 * int(range_s[i]))])

	pygame.draw.lines(sc, COLOR_TEXT, False, MassivTochekRange,2)
	pygame.display.update()

COLOR_FONE = (32, 32, 32)
COLOR_TEXT = (0, 255, 64)
COLOR_LINE = (255, 255, 255)
COLOR_GRAF = (255, 255, 0)

pygame.init()

ports = serial_ports()
if len(ports) > 0:
	message = 'Найден порт ' + ports[0]
	stop = False
else:
	message = 'СОМ портов не найдено'
	stop = True
print(message)
if stop:
	pygame.quit()

ser = serial.Serial()
InitCOM()

sc = pygame.display.set_mode((1100, 600))
pygame.display.set_caption("Дальность")

sc.fill(COLOR_FONE)
# Линии координат 
pygame.draw.line(sc, COLOR_LINE,[10, sc.get_height()-10], [sc.get_width()-10, sc.get_height()-10])
pygame.draw.line(sc, COLOR_LINE,[10, 10], [10, sc.get_height()-10])
pygame.display.update()

#  Обозначение линий координат и их разметка
font = pygame.font.SysFont('Consolas', 18)
PaintSimbol("0", 17, 17)
PaintSimbol("D", 17, sc.get_height() - 17)
PaintSimbol("t", sc.get_width() - 17, 17)
PaintMetki()
pygame.display.update()
running = True 
global range_s
range_s = [] # инициализация массива данных
while running:
	for i in pygame.event.get():
		if i.type == pygame.QUIT:
			running = False
		elif i.type == pygame.KEYDOWN:
			range_s.clear()  # инициализация массива данных
			if i.key == pygame.K_s:
				PaintRange100()
			elif i.key == pygame.K_c:
				PaintRange()
	pygame.time.delay(20)
ser.close()
pygame.quit()
