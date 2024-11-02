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
        letra_surface = font.render(letra, True, (255, 255, 255))  # Cor branca para visibilidade
        tela.blit(letra_surface, pos)


# Função para largar uma letra e reposicioná-la corretamente no labirinto
# Função para largar uma letra e reposicioná-la corretamente no labirinto
# Função para largar a última letra coletada e reposicioná-la corretamente no labirinto
# Função para coletar letras quando o jogador as encontra



# Função para largar a última letra coletada em uma nova posição
# Função para largar uma letra e reposicioná-la corretamente no labirinto
def largar_letra(letras_coletadas, posicao_jogador, size, letras_palavra, posicoes_letras):
    if letras_coletadas:
        # Remove a última letra coletada e a coloca em uma nova posição
        ultima_letra = letras_coletadas.pop()

        # Gera uma nova posição ao redor da posição do jogador, garantindo que seja única
        nova_pos = (
            posicao_jogador[0] + randint(-size, size),
            posicao_jogador[1] + randint(-size, size)
        )

        # Checa se a posição já está ocupada para evitar duplicatas
        while nova_pos in posicoes_letras:
            nova_pos = (
                posicao_jogador[0] + randint(-size, size),
                posicao_jogador[1] + randint(-size, size)
            )

        # Adiciona a letra e a posição correspondentes nas listas
        letras_palavra.append(ultima_letra)
        posicoes_letras.append(nova_pos)

        return ultima_letra, nova_pos


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
    if "".join(sorted(letras_coletadas)) == "".join(sorted(letras_palavra)):
        vencedor = True

    # Verifica condição de vitória
    if vencedor:
        print("Você venceu!")
        break

    # Desenha as letras no labirinto
    desenhar_letras(tela, letras_palavra, posicoes_letras)

    # Desenha o jogador e as letras coletadas
    posicionar_jogadores(tela, posicoes, size)

    # Exibe as letras coletadas
    texto = font.render("Palavra: " + "".join(letras_coletadas), True, (255, 255, 255))
    tela.blit(texto, (10, 10))

    # Desenhar a palavra completa na tela
    texto_palavra = font.render("Palavra: " + palavra_secreta, True, (255, 255, 255))
    tela.blit(texto_palavra, (10, 30))

    pg.draw.rect(tela, cor, (
    (posicoes[id_jogador][0][0] - size // 2 + 1, posicoes[id_jogador][0][1] - size // 2 + 1), (size - 1, size - 1)))
    pg.display.update()

    if vencedor:
        print("Você venceu o jogo!")
        break
