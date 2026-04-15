import pygame
import sys
import os
from player import Player
from item import Item
from inimigo import Inimigo

# --- Inicialização ---
pygame.init()
pygame.mixer.init()

# --- Configurações da Tela ---
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Missão Tática - 60 FPS")

# 1. RELÓGIO PARA CONTROLAR O FPS
relogio = pygame.time.Clock()

# --- Carregamento de Assets ---
diretorio_assets = os.path.join(os.path.dirname(__file__), "assets")

# Carregar Fundo
caminho_fundo = os.path.join(diretorio_assets, "background.png")
if os.path.exists(caminho_fundo):
    background = pygame.image.load(caminho_fundo).convert()
    background = pygame.transform.scale(background, (largura, altura))
else:
    background = pygame.Surface((largura, altura))
    background.fill((50, 50, 50))

# Carregar Som (Opcional)
caminho_som = os.path.join(diretorio_assets, "moeda.wav")
som_moeda = pygame.mixer.Sound(caminho_som) if os.path.exists(caminho_som) else None

# --- Criar Objetos ---
player = Player(largura, altura)
moeda = Item(largura, altura)
lista_inimigos = [Inimigo(largura, altura) for _ in range(5)]

# --- Variáveis de Estado ---
pontos = 0
vidas = 3
fonte = pygame.font.SysFont("Arial", 30, bold=True)
fonte_grande = pygame.font.SysFont("Arial", 60, bold=True)
game_over = False

# --- Loop Principal ---
while True:
    # 2. MANTER 60 QUADROS POR SEGUNDO
    relogio.tick(60) 

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # LOGICA DO REINICIAR (Tecla R)
        if game_over and evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_r:
                # Reseta tudo
                vidas = 3
                pontos = 0
                game_over = False
                player.x = largura // 2
                player.y = altura // 2
                for inimigo in lista_inimigos:
                    inimigo.resetar_posicao()

    if not game_over:
        # --- LÓGICA DE MOVIMENTO ---
        player.mover()
        
        if moeda.verificar_colisao(player):
            pontos += 1
            if som_moeda:
                som_moeda.play()
                
        for inimigo in lista_inimigos:
            inimigo.mover()
            if inimigo.verificar_colisao(player):
                vidas -= 1
                inimigo.resetar_posicao()
                if vidas <= 0:
                    game_over = True

    # --- DESENHO ---
    # 1. Fundo
    tela.blit(background, (0, 0))
    
    # 2. Objetos
    moeda.desenhar(tela)
    player.desenhar(tela)
    for inimigo in lista_inimigos:
        inimigo.desenhar(tela)

    # 3. UI (Interface)
    txt_pontos = fonte.render(f"Pontos: {pontos}", True, (255, 255, 255))
    txt_vidas = fonte.render(f"Vidas: {vidas}", True, (255, 0, 0))
    tela.blit(txt_pontos, (20, 20))
    tela.blit(txt_vidas, (largura - 150, 20))

    # 4. TELA DE GAME OVER
    if game_over:
        # Desenha um fundo escuro semi-transparente
        overlay = pygame.Surface((largura, altura), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180)) 
        tela.blit(overlay, (0,0))
        
        txt_fim = fonte_grande.render("GAME OVER", True, (255, 0, 0))
        txt_retry = fonte.render("Pressione 'R' para Reiniciar", True, (255, 255, 255))
        
        tela.blit(txt_fim, (largura//2 - txt_fim.get_width()//2, altura//2 - 50))
        tela.blit(txt_retry, (largura//2 - txt_retry.get_width()//2, altura//2 + 40))

    pygame.display.update()