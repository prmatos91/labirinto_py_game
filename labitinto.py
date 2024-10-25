import base64
import pygame as pg
import sys
from gerar_labirinto import *
from PIL import Image
from random import randint
import random
import pickle
from time import sleep

	
# Número de linhas e colunas
tamanho = [15,10]
#---------------------------

# Tamanho do espaço entre as linhas e colunas
size = 33
#--------------------------------------------

# Retorna um lista com duas sublista contendo 1 para parede, 0 para espaço vazio -
l = gerar_labirinto(tamanho[0],tamanho[1])
#---------------------------------------------------------------------------------

# Cria uma imagem em branco ------------------------------------------------------
img_new = Image.new('RGB', (tamanho[0]*(size+1)+1,tamanho[1]*(size+1)+1), (0,0,0))
#---------------------------------------------------------------------------------

# Cria uma "máscara" onde o labirinto vai ser desenhado
draw = ImageDraw.Draw(img_new)
#------------------------------------------------------

# Desenha o labirinto na "máscara" --------------
desenhar_labirinto_pillow(draw, tamanho, l, size)
#------------------------------------------------

# Salva a imagem com o labirinto já desenhado
img_new.save("fundo_verde.png")
#--------------------------------------------

size += 1
id_jogador = 0
cor = [randint(15,255),randint(15,255),randint(15,255)]

conectado_servidor = False
#-------------------------------------------------------------------------------------

pg.init()

try:
	pg.joystick.init()
	joystick = pg.joystick.Joystick(0)
	joystick.init()
	houver_controle = True
except:
	houver_controle = False

pygame.mouse.set_visible(False)
tela = pg.display.set_mode((tamanho[0]*size+1,tamanho[1]*size+1))
fps = pg.time.Clock()
img = Image.open("fundo_verde.png")
fundo = pg.image.load("fundo_verde.png")
fundo_rect = fundo.get_rect()
img = img.convert('RGB')
rgb = img.load()
posicoes = {id_jogador:[[tamanho[0]*size-size/2,size/2], cor]}
print(posicoes[id_jogador][0])
pg.mouse.set_pos(posicoes[id_jogador][0])
x_mouse, y_mouse = posicoes[id_jogador][0]
tela.blit(fundo, fundo_rect)
pg.display.update()

while True:

	fps.tick(10)
	tela.blit(fundo, fundo_rect)

	for event in pg.event.get():

		x_mouse, y_mouse = pg.mouse.get_pos()
		jogou = False

		if event.type == pg.QUIT:
			pg.quit()
			sys.exit()

		elif event.type == pg.KEYDOWN:
			if event.key == pg.K_LEFT:
				posicoes, jogou = move.esquerda(rgb, size, posicoes, id_jogador)
			elif event.key == pg.K_RIGHT:
				posicoes, jogou = move.direita(rgb, size, posicoes, id_jogador)
			elif event.key == pg.K_UP:
				posicoes, jogou = move.cima(rgb, size, posicoes, id_jogador)
			elif event.key == pg.K_DOWN:
				posicoes, jogou = move.baixo(rgb, size, posicoes, id_jogador)
		
		else:
			if x_mouse < posicoes[id_jogador][0][0] - size/2:
				posicoes, jogou = move.esquerda(rgb, size, posicoes, id_jogador)
			elif x_mouse > posicoes[id_jogador][0][0] + size/2:
				posicoes, jogou = move.direita(rgb, size, posicoes, id_jogador)
			elif y_mouse < posicoes[id_jogador][0][1] - size/2:
				posicoes, jogou = move.cima(rgb, size, posicoes, id_jogador)
			elif y_mouse > posicoes[id_jogador][0][1] + size/2:
				posicoes, jogou = move.baixo(rgb, size, posicoes, id_jogador)

	if houver_controle:

		vertical = round(joystick.get_axis(1))
		horizontal = round(joystick.get_axis(0))

		if horizontal < 0:
			posicoes, jogou = move.esquerda(rgb, size, posicoes, id_jogador)
		elif horizontal > 0:
			posicoes, jogou = move.direita(rgb, size, posicoes, id_jogador)
		elif vertical < 0:
			posicoes, jogou = move.cima(rgb, size, posicoes, id_jogador)
		elif vertical > 0:
			posicoes, jogou = move.baixo(rgb, size, posicoes, id_jogador)

	vencedor = verificar_vitoria(posicoes, tamanho, size)


	posicionar_jogadores(tela, posicoes, size)

	pg.draw.rect(tela, cor, ((posicoes[id_jogador][0][0]-size/2+1, posicoes[id_jogador][0][1]-size/2+1),(size-1,size-1)))

	pg.display.update()
	


	if vencedor:
		exit()




