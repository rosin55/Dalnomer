# Рисует график точками по заданному массиву MassivTochek
# 28.11.2018

import pygame
import sys
import math
import simple_draw as sd

pygame.init()

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
			[x, (sc.get_height() - 10)],[x, (sc.get_height() - 15)])
	for i in range(n_metok_y):
		y = 20*i+10
		pygame.draw.line(sc, COLOR_LINE,\
			[10, y],[15, y])


COLOR_FONE = (32, 32, 32)
COLOR_TEXT = (0, 255, 64)
COLOR_LINE = (255, 255, 255)
COLOR_GRAF = (255, 255, 0)
MassivTochek = []

sc = pygame.display.set_mode((800, 300))
pygame.display.set_caption("Синус и косинус")

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

for i in range(0,100):
	MassivTochek.append(sd.Point(i, (150 + 120*math.sin(math.pi/12*i))))
 
while 1:
	for i in pygame.event.get():
		if i.type == pygame.QUIT:
			pygame.quit()
			
# # Рисуем синус зелёным
	for i in range(len(MassivTochek)):
		text = font.render(".", 1, (COLOR_TEXT))
		y = sc.get_height()-MassivTochek[i].y+5
		place = text.get_rect(center = (i*10+5, y))
		sc.blit(text, place)
		pygame.display.update()

# # Рисуем косинус желтым
	for i in range(len(MassivTochek)):
		text = font.render(".", 1, (COLOR_GRAF))
		y = sc.get_height()-MassivTochek[i].y+5
		place = text.get_rect(center = (i*10+5+70, y))
		sc.blit(text, place)
		pygame.display.update()
