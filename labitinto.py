import base64
import pygame as pg
import sys
from gerar_labirinto import *
from PIL import Image
from random import randint, choice, sample
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
pg.font.init()
font = pg.font.Font(None, 36)

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

# Lista de palavras e escolha aleatória
lista_palavras = ["PYTHON", "LABIRINTO", "JOGO", "DESAFIO"]
palavra_secreta = choice(lista_palavras)
letras_palavra = list(palavra_secreta)
letras_coletadas = []
posicoes_letras = gerar_posicoes_letras(tamanho, size, letras_palavra)

# Função para desenhar as letras na tela
def desenhar_letras(tela, letras, posicoes):
    for letra, pos in zip(letras, posicoes):
        letra_surface = font.render(letra, True, (0, 255, 0))
        tela.blit(letra_surface, pos)

# Inicializa coletar_letra
coletar_letra = False
vencedor = False

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
            if event.key == pg.K_SPACE:
                coletar_letra = True
            elif event.key == pg.K_LEFT:
                posicoes, jogou = move.esquerda(rgb, size, posicoes, id_jogador)
            elif event.key == pg.K_RIGHT:
                posicoes, jogou = move.direita(rgb, size, posicoes, id_jogador)
            elif event.key == pg.K_UP:
                posicoes, jogou = move.cima(rgb, size, posicoes, id_jogador)
            elif event.key == pg.K_DOWN:
                posicoes, jogou = move.baixo(rgb, size, posicoes, id_jogador)

        elif event.type == pg.KEYUP:
            if event.key == pg.K_SPACE:
                coletar_letra = False

    # Verifica se o jogador coleta uma letra
    letras_coletadas, posicoes_letras = verificar_coleta_letra(
        posicoes[id_jogador][0], letras_palavra, letras_coletadas, posicoes_letras, size, coletar_letra
    )

    # Checa se todas as letras foram coletadas para vencer
    if len(letras_coletadas) == len(letras_palavra):
        vencedor = True

    # Verifica condição de vitória
    if vencedor:
        print("Você venceu!")
        break

    # Verifica se o jogador coletou alguma letra
    # letras_coletadas, posicoes_letras = verificar_coleta_letra(posicoes[id_jogador][0], letras_palavra, letras_coletadas, posicoes_letras, size)

    # Desenha o jogador, letras e as letras coletadas
    posicionar_jogadores(tela, posicoes, size)
    desenhar_letras(tela, letras_palavra, posicoes_letras)

    # Exibe as letras coletadas
    texto = font.render("Palavra: " + "".join(letras_coletadas), True, (255, 255, 255))
    tela.blit(texto, (10, 10))

    pg.draw.rect(tela, cor, ((posicoes[id_jogador][0][0] - size/2 + 1, posicoes[id_jogador][0][1] - size/2 + 1), (size-1, size-1)))
    pg.display.update()

    if vencedor:
        print("Você venceu o jogo!")
        break
