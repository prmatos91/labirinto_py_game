import base64
import pygame as pg
import sys
from gerar_labirinto import *
from PIL import Image
from random import randint, choice
import pickle
from time import sleep

# Configurações iniciais
tamanho = [15, 10]  # Número de linhas e colunas do labirinto
size = 33  # Tamanho do espaço entre as linhas e colunas

# Retorna uma lista com duas sublistas contendo 1 para parede e 0 para espaço vazio
l = gerar_labirinto(tamanho[0], tamanho[1])

# Cria uma imagem em branco para o labirinto
img_new = Image.new('RGB', (tamanho[0]*(size+1)+1, tamanho[1]*(size+1)+1), (0, 0, 0))
draw = ImageDraw.Draw(img_new)

# Desenha o labirinto na "máscara"
desenhar_labirinto_pillow(draw, tamanho, l, size)

# Salva a imagem com o labirinto desenhado
img_new.save("fundo_verde.png")

size += 1
id_jogador = 0
cor = [randint(15, 255), randint(15, 255), randint(15, 255)]
conectado_servidor = False

pg.init()

# Inicializa joystick, se disponível
try:
    pg.joystick.init()
    joystick = pg.joystick.Joystick(0)
    joystick.init()
    houver_controle = True
except:
    houver_controle = False

pg.mouse.set_visible(False)
tela = pg.display.set_mode((tamanho[0]*size+1, tamanho[1]*size+1))
fps = pg.time.Clock()
img = Image.open("fundo_verde.png")
fundo = pg.image.load("fundo_verde.png")
fundo_rect = fundo.get_rect()
img = img.convert('RGB')
rgb = img.load()
posicoes = {id_jogador: [[tamanho[0]*size-size/2, size/2], cor]}
pg.mouse.set_pos(posicoes[id_jogador][0])
x_mouse, y_mouse = posicoes[id_jogador][0]
tela.blit(fundo, fundo_rect)
pg.display.update()

# Função para gerar objetos coletáveis em posições aleatórias no labirinto
def gerar_objetos():
    objetos = []
    for _ in range(5):  # Número de objetos coletáveis
        x = choice(range(1, tamanho[0] - 1)) * size + size // 2
        y = choice(range(1, tamanho[1] - 1)) * size + size // 2
        objetos.append([x, y])
    return objetos

objetos = gerar_objetos()

# Função para desenhar os objetos na tela
def desenhar_objetos(tela, objetos):
    for obj in objetos:
        pg.draw.circle(tela, (0, 255, 0), obj, size // 4)  # Verde para os objetos

# Função para verificar se o jogador coleta um objeto
def verificar_coleta(posicoes, objetos):
    novos_objetos = []
    for obj in objetos:
        if abs(posicoes[id_jogador][0][0] - obj[0]) < size // 2 and abs(posicoes[id_jogador][0][1] - obj[1]) < size // 2:
            continue  # Coletado, não adiciona na nova lista
        novos_objetos.append(obj)
    return novos_objetos

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

    # Controle via joystick
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

    # Verifica se o jogador coletou algum objeto
    objetos = verificar_coleta(posicoes, objetos)
    if len(objetos) < 5:  # Reabastece os objetos se necessário
        objetos.extend(gerar_objetos())

    # Desenha o jogador e os objetos coletáveis na tela
    posicionar_jogadores(tela, posicoes, size)
    desenhar_objetos(tela, objetos)

    pg.draw.rect(tela, cor, ((posicoes[id_jogador][0][0] - size/2 + 1, posicoes[id_jogador][0][1] - size/2 + 1), (size-1, size-1)))
    pg.display.update()

    if vencedor:
        print("Você venceu o jogo!")
        break
