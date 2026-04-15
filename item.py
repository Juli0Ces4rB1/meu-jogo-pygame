import pygame
import random
import os

class Item:
    def __init__(self, largura_tela, altura_tela):
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.tamanho = 50 # Medalha visível

        # Lógica de carregamento inteligente da imagem moeda.png
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        caminho_imagem = os.path.join(diretorio_atual, "assets", "moeda.png")

        if os.path.exists(caminho_imagem):
            # --- ESTA É A CORREÇÃO CRÍTICA ---
            # Antes: .convert()
            # Agora: .convert_alpha() é OBRIGATÓRIO para imagens transparentes PNG
            self.imagem_original = pygame.image.load(caminho_imagem).convert_alpha()
            self.imagem = pygame.transform.scale(self.imagem_original, (self.tamanho, self.tamanho))
            print("Sucesso: Imagem moeda.png carregada COM TRANSPARÊNCIA!")
        else:
            print(f"Erro: Não encontrei {caminho_imagem}. Usando reserva.")
            # Cria um bloco verde se não achar a imagem
            self.imagem = pygame.Surface((self.tamanho, self.tamanho))
            self.imagem.fill((0, 255, 0))

        self.reposicionar()

    def reposicionar(self):
        # Sorteia posição dentro da tela
        self.x = random.randint(0, self.largura_tela - self.tamanho)
        self.y = random.randint(0, self.altura_tela - self.tamanho)

    def verificar_colisao(self, player):
        # Sincronizado com as novas variáveis do Player
        player_rect = pygame.Rect(player.x, player.y, player.largura_p, player.altura_p)
        item_rect = pygame.Rect(self.x, self.y, self.tamanho, self.tamanho)
        
        if player_rect.colliderect(item_rect):
            self.reposicionar()
            return True
        return False

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x, self.y))