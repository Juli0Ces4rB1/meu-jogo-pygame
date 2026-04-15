import pygame
import random
import os

class Inimigo:
    def __init__(self, largura_tela, altura_tela):
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        
        # Tamanho do inimigo (um pouco menor que o player para ser justo)
        self.largura_i = 70
        self.altura_i = 100
        
        # Carregando a imagem
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        caminho_imagem = os.path.join(diretorio_atual, "assets", "inimigo.png")
        
        if os.path.exists(caminho_imagem):
            self.imagem = pygame.image.load(caminho_imagem).convert_alpha()
            self.imagem = pygame.transform.scale(self.imagem, (self.largura_i, self.altura_i))
        else:
            self.imagem = pygame.Surface((self.largura_i, self.altura_i))
            self.imagem.fill((0, 0, 0)) # Preto se falhar

        self.resetar_posicao()

    def resetar_posicao(self):
        # Inimigo começa em um lugar aleatório
        self.x = random.randint(0, self.largura_tela - self.largura_i)
        self.y = random.randint(-500, -100) # Começa acima da tela para descer
        self.velocidade = random.randint(2, 5)

    def mover(self):
        self.y += self.velocidade
        # Se sair por baixo da tela, volta para cima
        if self.y > self.altura_tela:
            self.resetar_posicao()

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x, self.y))

    def verificar_colisao(self, player):
        player_rect = pygame.Rect(player.x, player.y, player.largura_p, player.altura_p)
        inimigo_rect = pygame.Rect(self.x, self.y, self.largura_i, self.altura_i)
        return player_rect.colliderect(inimigo_rect)