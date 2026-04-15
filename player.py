import pygame
import os

class Player:
    def __init__(self, largura_tela, altura_tela):
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        
        # Dimensões do soldado (mantendo o tamanho proporcional)
        self.largura_p = 100
        self.altura_p = 100 
        
        # --- VELOCIDADE AUMENTADA ---
        # Aumentada de 3 para 8 para o soldado se mover mais rápido
        self.velocidade = 8 
        
        # Posição inicial (centralizado)
        self.x = largura_tela // 2
        self.y = altura_tela // 2

        # Lógica inteligente de carregamento da imagem soldado.png
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        caminho_imagem = os.path.join(diretorio_atual, "assets", "soldado.png")

        if os.path.exists(caminho_imagem):
            # convert_alpha() é obrigatório para transparência PNG
            self.imagem_original = pygame.image.load(caminho_imagem).convert_alpha()
            self.imagem = pygame.transform.scale(self.imagem_original, (self.largura_p, self.altura_p))
            print("Sucesso: Imagem soldado.png carregada com velocidade aumentada!")
        else:
            print(f"Erro: Não encontrei {caminho_imagem}. Usando bloco reserva.")
            self.imagem = pygame.Surface((self.largura_p, self.altura_p))
            self.imagem.fill((255, 0, 0))

    def mover(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.x -= self.velocidade
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.x += self.velocidade
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            self.y -= self.velocidade
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            self.y += self.velocidade

        # Limites da tela (Clamp)
        self.x = max(0, min(self.x, self.largura_tela - self.largura_p))
        self.y = max(0, min(self.y, self.altura_tela - self.altura_p))

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x, self.y))