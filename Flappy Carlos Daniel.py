import pygame
import random

# Inicializa o Pygame
pygame.init()

# Configurações da tela
LARGURA, ALTURA = 400, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Flappy Carlos Daniel")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)

# Configurações do jogo
GRAVIDADE = 0.5
PULO = -10
LARGURA_CANO = 50
ESPACO_CANO = 150
VELOCIDADE_CANO = 3

# Carrega imagens (substitua pelos caminhos das suas imagens)
fundo = pygame.image.load("fundo.jpg").convert()
passaro_img = pygame.image.load("passaro.png").convert_alpha()
cano_img = pygame.image.load("cano.png").convert_alpha()

# Redimensiona as imagens (se necessário)
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))
passaro_img = pygame.transform.scale(passaro_img, (40, 40))
cano_img = pygame.transform.scale(cano_img, (LARGURA_CANO, 300))

# Função para desenhar o passaro
def desenhar_passaro(x, y):
    tela.blit(passaro_img, (x, y))

# Função para desenhar os canos
def desenhar_canos(canos):
    for cano in canos:
        tela.blit(cano_img, (cano['x'], cano['top']))
        tela.blit(pygame.transform.flip(cano_img, False, True), (cano['x'], cano['bottom']))

# Função para mover os canos
def mover_canos(canos):
    for cano in canos:
        cano['x'] -= VELOCIDADE_CANO
    return [cano for cano in canos if cano['x'] > -LARGURA_CANO]

# Função para criar novos canos
def criar_cano():
    altura_cano = random.randint(100, 400)
    cano = {
        'x': LARGURA,
        'top': altura_cano - ESPACO_CANO // 2 - 300,
        'bottom': altura_cano + ESPACO_CANO // 2
    }
    return cano

# Função para exibir texto na tela
def exibir_texto(texto, tamanho, x, y):
    fonte = pygame.font.SysFont(None, tamanho)
    texto_renderizado = fonte.render(texto, True, PRETO)
    tela.blit(texto_renderizado, (x, y))

# Tela de início
def tela_inicio():
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    return True

        tela.blit(fundo, (0, 0))
        exibir_texto("FLAPPY CARLOS DANIEL", 40, 50, ALTURA // 2-100)
        exibir_texto("Pressione ESPAÇO", 40, 50, ALTURA // 2)
        exibir_texto("para jogar", 40, 50, ALTURA // 2+50)
        pygame.display.update()

# Tela de game over
def tela_game_over(pontuacao):
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    return True

        tela.blit(fundo, (0, 0))
        exibir_texto("Game Over!", 50, 120, ALTURA // 2 - 50)
        exibir_texto(f"Pontuação: {int(pontuacao)}", 40, 130, ALTURA // 2)
        exibir_texto("Pressione ESPAÇO para jogar novamente", 30, 50, ALTURA // 2 + 50)
        pygame.display.update()

# Função principal do jogo
def jogo():
    passaro_x, passaro_y = 50, ALTURA // 2
    velocidade_passaro = 0  # Inicializa a velocidade do pássaro
    canos = [criar_cano()]
    pontuacao = 0
    rodando = True

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    velocidade_passaro = PULO

        # Atualiza a posição do pássaro
        velocidade_passaro += GRAVIDADE
        passaro_y += velocidade_passaro

        # Movimenta e remove canos
        canos = mover_canos(canos)
        if canos[-1]['x'] < LARGURA - 200:
            canos.append(criar_cano())
            pontuacao += 1  # Aumenta a pontuação ao passar por um cano

        # Verifica colisões
        for cano in canos:
            if (passaro_x + 40 > cano['x'] and passaro_x < cano['x'] + LARGURA_CANO) and \
               (passaro_y < cano['top'] + 300 or passaro_y + 40 > cano['bottom']):
                rodando = False

        # Verifica se o pássaro saiu da tela
        if passaro_y > ALTURA or passaro_y < 0:
            rodando = False

        # Desenha o fundo, pássaro e canos
        tela.blit(fundo, (0, 0))
        desenhar_passaro(passaro_x, passaro_y)
        desenhar_canos(canos)

        # Exibe a pontuação
        exibir_texto(f"Pontuação: {int(pontuacao)}", 30, 10, 10)

        # Atualiza a tela
        pygame.display.update()

        # Controla a taxa de atualização
        pygame.time.Clock().tick(60)

    # Exibe a tela de game over
    return tela_game_over(pontuacao)

# Loop principal do programa
jogar_novamente = True
while jogar_novamente:
    if not tela_inicio():
        break
    jogar_novamente = jogo()

pygame.quit()