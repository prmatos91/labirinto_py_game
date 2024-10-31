from random import shuffle, randrange, choice, randint
from PIL import ImageDraw
import pygame
from pygame import *
import sys

sys.setrecursionlimit(10000)


# Função para gerar o layout do labirinto com 1 para parede e 0 para espaço livre
def gerar_labirinto(w=10, h=10):
    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
    ver = [["|  "] * w + ['|'] for _ in range(h)] + [[]]
    hor = [["+--"] * w + ['+'] for _ in range(h + 1)]

    def walk(x, y):
        vis[y][x] = 1
        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]: continue
            if xx == x: hor[max(y, yy)][x] = "+  "
            if yy == y: ver[y][max(x, xx)] = "   "
            walk(xx, yy)

    walk(randrange(w), randrange(h))
    linhas_colunas = [[], []]
    for (a, b) in zip(hor, ver):
        for l in a:
            if l == "+--":
                linhas_colunas[0].append(1)
            elif l == "+":
                pass
            else:
                linhas_colunas[0].append(0)
        if len(b) != 0:
            for c in b:
                if "|" in c:
                    linhas_colunas[1].append(1)
                else:
                    linhas_colunas[1].append(0)

    return linhas_colunas


# Função para desenhar o labirinto com a biblioteca Pillow
def desenhar_labirinto_pillow(img, tamanho, posicoes, size=11):
    (x, y) = tamanho
    size += 1
    contX = contY = 0
    cor = (255, 255, 255)
    for yy in range(0, y * size + 1, size):
        for xx in range(0, x * size + 1, size):
            try:
                if posicoes[0][contX] == 1:
                    img.line((xx, yy, xx + size, yy), fill=cor)
                if posicoes[1][contY] == 1:
                    img.line((xx, yy, xx, yy + size), fill=cor)
                contX += 1
                contY += 1
            except:
                pass
        contX -= 1
    desenha_fim_pillow(img, tamanho, size)


# Função para gerar a posição das letras no labirinto
def gerar_posicoes_letras(tamanho, size, letras):
    posicoes = []
    for letra in letras:
        x = randint(1, tamanho[0] - 2) * size + size // 2
        y = randint(1, tamanho[1] - 2) * size + size // 2
        posicoes.append((x, y))
    return posicoes


# Função para verificar e coletar letras quando o jogador pressiona 'Espaço'
def verificar_coleta_letra(posicao_jogador, letras, letras_coletadas, posicoes_letras, size, coletar):
    novas_posicoes = []
    for i, pos in enumerate(posicoes_letras):
        if abs(posicao_jogador[0] - pos[0]) < size // 2 and abs(posicao_jogador[1] - pos[1]) < size // 2:
            # Coleta a letra apenas se a tecla espaço for pressionada
            if coletar:
                letras_coletadas.append(letras[i])
            else:
                novas_posicoes.append(pos)
        else:
            novas_posicoes.append(pos)
    return letras_coletadas, novas_posicoes


# Função para desenhar o fim do labirinto
def desenha_fim_pillow(tela, tamanho, size=11):
    (x, y) = tamanho
    tela.rectangle((1, y * size - size + 1, size - 1, y * size - 1), fill=(255, 0, 0), outline=(255, 0, 0))


# Funções de movimentação do jogador
class move:
    def esquerda(rgb, size, pos, id_jogador):
        r, g, b = rgb[pos[id_jogador][0][0] - size // 2, pos[id_jogador][0][1]]
        jogou = False
        if r == 0:
            jogou = True
            pos[id_jogador][0][0] -= size
        pygame.mouse.set_pos(pos[id_jogador][0])
        return pos, jogou

    def direita(rgb, size, pos, id_jogador):
        r, g, b = rgb[pos[id_jogador][0][0] + size // 2, pos[id_jogador][0][1]]
        jogou = False
        if r == 0:
            jogou = True
            pos[id_jogador][0][0] += size
        pygame.mouse.set_pos(pos[id_jogador][0])
        return pos, jogou

    def cima(rgb, size, pos, id_jogador):
        r, g, b = rgb[pos[id_jogador][0][0], pos[id_jogador][0][1] - size // 2]
        jogou = False
        if r == 0:
            jogou = True
            pos[id_jogador][0][1] -= size
        pygame.mouse.set_pos(pos[id_jogador][0])
        return pos, jogou

    def baixo(rgb, size, pos, id_jogador):
        r, g, b = rgb[pos[id_jogador][0][0], pos[id_jogador][0][1] + size // 2]
        jogou = False
        if r == 0:
            jogou = True
            pos[id_jogador][0][1] += size
        pygame.mouse.set_pos(pos[id_jogador][0])
        return pos, jogou


# Função para posicionar os jogadores no labirinto
def posicionar_jogadores(tela, posicoes, size):
    for p in posicoes.values():
        cor = p[1]
        x, y = p[0]
        pygame.draw.rect(tela, cor, ((x - size // 2 + 1, y - size // 2 + 1), (size - 1, size - 1)))


# Função para verificar a vitória
def verificar_vitoria(posicao, tamanho, size):
    for ID, p in posicao.items():
        if p[0] == [size // 2, tamanho[1] * size - size // 2]:
            return True
    return False
