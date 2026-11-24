import pygame

pygame.init()

tamanho_tela = (800, 800) # Tamanho da tela do jogo
tela = pygame.display.set_mode(tamanho_tela)
pygame.display.set_caption("Brick Breaker")
relogio = pygame.time.Clock()
fonte = pygame.font.Font(None, 30)
fonte_fim = pygame.font.Font(None, 64)

tamanho_bola = 15 # Tamanho da bola
bola = pygame.Rect(400, 500, tamanho_bola, tamanho_bola)
tamanho_jogador = 100 # Tamanho do jogador
jogador = pygame.Rect(
    (tamanho_tela[0] - tamanho_jogador) // 2,
    750,
    tamanho_jogador,
    15,
)

qtde_blocos_linha = 8 # Quantidade de blocos por linha
qtde_linhas_blocos = 5 # Quantidade de linhas de blocos
qtde_total_blocos = qtde_blocos_linha * qtde_linhas_blocos

cores = {
    "branca": (255, 255, 255),
    "preta": (0, 0, 0),
    "amarela": (255, 255, 0),
    "azul": (0, 0, 255),
    "verde": (0, 255, 0),
}

velocidade_bola = 7
movimento_bola = [velocidade_bola, -velocidade_bola]


def criar_blocos(qtde_blocos_linha, qtde_linhas_blocos): # Função para criar os blocos do jogo
    distancia_entre_blocos = 5
    margem = 10
    largura_disponivel = tamanho_tela[0] - (margem * 2)
    largura_bloco = (
        largura_disponivel - distancia_entre_blocos * (qtde_blocos_linha - 1)
    ) // qtde_blocos_linha 
    altura_bloco = 15
    distancia_entre_linhas = altura_bloco + 10

    blocos = [] #
    for linha in range(qtde_linhas_blocos): 
        for coluna in range(qtde_blocos_linha):
            x = margem + coluna * (largura_bloco + distancia_entre_blocos)
            y = margem + linha * distancia_entre_linhas
            blocos.append(pygame.Rect(x, y, largura_bloco, altura_bloco))
    return blocos


def desenhar_inicio_jogo(): # Função para desenhar o jogador e a bola na tela
    tela.fill(cores["preta"])
    pygame.draw.rect(tela, cores["azul"], jogador)
    pygame.draw.rect(tela, cores["branca"], bola)


def desenhar_blocos(blocos): # Função para desenhar os blocos na tela
    for bloco in blocos:
        pygame.draw.rect(tela, cores["verde"], bloco)


def movimentar_jogador(teclas, velocidade=8): # Função para movimentar o jogador com as teclas de seta ou WASD
    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        jogador.x -= velocidade
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        jogador.x += velocidade

    jogador.x = max(0, min(jogador.x, tamanho_tela[0] - jogador.width))


def movimentar_bola(blocos): # Função para movimentar a bola e verificar colisões
    global movimento_bola

    bola.x += movimento_bola[0]
    bola.y += movimento_bola[1]

    # Paredes laterais e topo
    if bola.left <= 0:
        bola.left = 0
        movimento_bola[0] = abs(movimento_bola[0])
    elif bola.right >= tamanho_tela[0]:
        bola.right = tamanho_tela[0]
        movimento_bola[0] = -abs(movimento_bola[0])

    if bola.top <= 0:
        bola.top = 0
        movimento_bola[1] = abs(movimento_bola[1])

    # Caiu embaixo da tela
    if bola.bottom >= tamanho_tela[1]:
        return False

    # Colisao com o jogador (ajusta angulo conforme o ponto de impacto)
    if bola.colliderect(jogador) and movimento_bola[1] > 0:
        bola.bottom = jogador.top
        centro_jogador = jogador.centerx
        desvio = (bola.centerx - centro_jogador) / (jogador.width / 2)
        movimento_bola[0] = desvio * velocidade_bola
        movimento_bola[1] = -abs(movimento_bola[1])

    # Colisao com os blocos
    for bloco in blocos[:]:
        if bola.colliderect(bloco):
            sobreposicao_esq = bola.right - bloco.left
            sobreposicao_dir = bloco.right - bola.left
            sobreposicao_cima = bola.bottom - bloco.top
            sobreposicao_baixo = bloco.bottom - bola.top

            min_horizontal = min(sobreposicao_esq, sobreposicao_dir)
            min_vertical = min(sobreposicao_cima, sobreposicao_baixo)

            if min_horizontal < min_vertical:
                movimento_bola[0] = -movimento_bola[0]
            else:
                movimento_bola[1] = -movimento_bola[1]

            blocos.remove(bloco)
            break

    return True


def atualizar_pontuacao(pontuacao): # Função para atualizar a pontuação na tela
    texto = fonte.render(f"Pontuacao: {pontuacao}", True, cores["amarela"])
    tela.blit(texto, (10, 770))


def mostrar_mensagem_fim(mensagem): # Função para mostrar a mensagem de fim de jogo
    tela.fill(cores["preta"])
    texto = fonte_fim.render(mensagem, True, cores["amarela"])
    retangulo = texto.get_rect(center=(tamanho_tela[0] // 2, 350))
    tela.blit(texto, retangulo)
    instrucoes = fonte.render(
        "Pressione R para jogar novamente ou ESC para sair",
        True,
        cores["branca"],
    )
    retangulo_instrucoes = instrucoes.get_rect(
        center=(tamanho_tela[0] // 2, 430)
    )
    tela.blit(instrucoes, retangulo_instrucoes)
    pygame.display.flip()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    return True
                if evento.key in (pygame.K_ESCAPE, pygame.K_q):
                    return False
        relogio.tick(30)


jogando = True
while jogando:
    bola = pygame.Rect(400, 500, tamanho_bola, tamanho_bola)
    jogador = pygame.Rect(
        (tamanho_tela[0] - tamanho_jogador) // 2,
        750,
        tamanho_jogador,
        15,
    )
    movimento_bola = [velocidade_bola, -velocidade_bola]
    blocos = criar_blocos(qtde_blocos_linha, qtde_linhas_blocos)
    fim_jogo = False
    vitoria = False

    while not fim_jogo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                fim_jogo = True
                jogando = False

        teclas = pygame.key.get_pressed()
        movimentar_jogador(teclas)

        if not movimentar_bola(blocos):
            fim_jogo = True

        desenhar_inicio_jogo()
        desenhar_blocos(blocos)
        atualizar_pontuacao(qtde_total_blocos - len(blocos))

        if not blocos:
            vitoria = True
            fim_jogo = True

        pygame.display.flip()
        relogio.tick(40)

    if jogando:
        if vitoria:
            jogando = mostrar_mensagem_fim("Vitoria!")
        else:
            jogando = mostrar_mensagem_fim("Game Over!")

pygame.quit()