import pygame as pg
import sys
from gerar_labirinto import *
from PIL import Image
from random import choice

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

pg.init()
pg.font.init()
font = pg.font.Font(None, 36)

pg.mouse.set_visible(False)
tela = pg.display.set_mode((tamanho[0]*size+1, tamanho[1]*size+1))
fps = pg.time.Clock()
fundo = pg.image.load("fundo_verde.png")
fundo_rect = fundo.get_rect()
img = Image.open("fundo_verde.png")
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

# Variáveis de movimento
refletir_letras = False
escala_letras = 1.0
distorcao_letras = (1.0, 1.0)

# Função para desenhar as letras na tela
def desenhar_letras(tela, letras, posicoes, letras_coletadas, refletir=False, escala=1.0, distorcao=(1.0, 1.0)):
    for i, (letra, pos) in enumerate(zip(letras, posicoes)):
        cor = (100, 100, 100) if letra in letras_coletadas else (255, 255, 255)
        letra_surface = font.render(letra, True, cor)

        if refletir:
            letra_surface = pg.transform.flip(letra_surface, True, False)

        if escala != 1.0:
            letra_surface = pg.transform.scale(
                letra_surface,
                (int(letra_surface.get_width() * escala), int(letra_surface.get_height() * escala))
            )

        if distorcao != (1.0, 1.0):
            letra_surface = pg.transform.scale(
                letra_surface,
                (
                    int(letra_surface.get_width() * distorcao[0]),
                    int(letra_surface.get_height() * distorcao[1])
                )
            )

        letra_rect = letra_surface.get_rect(center=(pos[0], pos[1]))
        tela.blit(letra_surface, letra_rect.topleft)

# Verificar vitória (chegada ao final e palavra completa)
def verificar_vitoria(posicao, tamanho, size, palavra_coletada, palavra_secreta):
    jogador_x, jogador_y = posicao
    final_x, final_y = size // 2, tamanho[1] * size - size // 2
    if jogador_x == final_x and jogador_y == final_y and "".join(palavra_coletada) == palavra_secreta:
        return True
    return False

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
            if event.key == pg.K_SPACE:  # Coletar letra
                coletar_letra = True
            elif event.key == pg.K_s:  # Soltar última letra
                largar_letra(letras_coletadas, posicoes[id_jogador][0], size, letras_palavra, posicoes_letras)
            elif event.key == pg.K_LEFT:  # Movimentar jogador
                posicoes, jogou = move.esquerda(rgb, size, posicoes, id_jogador)
            elif event.key == pg.K_RIGHT:
                posicoes, jogou = move.direita(rgb, size, posicoes, id_jogador)
            elif event.key == pg.K_UP:
                posicoes, jogou = move.cima(rgb, size, posicoes, id_jogador)
            elif event.key == pg.K_DOWN:
                posicoes, jogou = move.baixo(rgb, size, posicoes, id_jogador)
            elif event.key == pg.K_f:  # Reflexão
                refletir_letras = not refletir_letras
            elif event.key == pg.K_PLUS or event.key == pg.K_KP_PLUS:  # Escala para mais
                escala_letras += 0.1
            elif event.key == pg.K_MINUS or event.key == pg.K_KP_MINUS:  # Escala para menos
                escala_letras = max(0.1, escala_letras - 0.1)
            elif event.key == pg.K_h:  # Distorção horizontal
                distorcao_letras = (distorcao_letras[0] + 0.1, distorcao_letras[1])
            elif event.key == pg.K_v:  # Distorção vertical
                distorcao_letras = (distorcao_letras[0], distorcao_letras[1] + 0.1)

        elif event.type == pg.KEYUP:
            if event.key == pg.K_SPACE:
                coletar_letra = False

    # Verifica se o jogador coleta uma letra
    letras_coletadas, _ = verificar_coleta_letra(
        posicoes[id_jogador][0], letras_palavra, letras_coletadas, posicoes_letras, size, coletar_letra
    )

    # Verifica vitória ao chegar no quadrado final e ter a palavra completa
    if verificar_vitoria(posicoes[id_jogador][0], tamanho, size, letras_coletadas, palavra_secreta):
        vencedor = True

    if vencedor:
        print("Você venceu o jogo! Parabéns!")
        tela.fill((0, 0, 0))
        texto_vitoria = font.render("Você venceu! Parabéns!", True, (0, 255, 0))
        tela.blit(texto_vitoria, (tamanho[0] * size // 4, tamanho[1] * size // 2))
        pg.display.update()
        pg.time.wait(3000)
        break

    # Desenha as letras no labirinto
    desenhar_letras(tela, letras_palavra, posicoes_letras, letras_coletadas, refletir_letras, escala_letras, distorcao_letras)

    # Exibe as letras coletadas
    texto_coletadas = font.render("Coletadas: " + "".join(letras_coletadas), True, (255, 255, 255))
    tela.blit(texto_coletadas, (10, 10))

    # Exibe a palavra completa
    texto_palavra = font.render("Palavra: " + palavra_secreta, True, (255, 255, 255))
    tela.blit(texto_palavra, (10, 40))

    # Atualiza o jogador e exibe
    pg.draw.rect(
        tela,
        cor,
        (
            (posicoes[id_jogador][0][0] - size // 2 + 1, posicoes[id_jogador][0][1] - size // 2 + 1),
            (size - 2, size - 2),
        ),
    )
    pg.display.update()
