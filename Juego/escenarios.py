# --- escenario.py ---
import pygame
import random

class Escenario:
    def __init__(self, ancho_ventana, alto_ventana):
        self.ANCHO_VENTANA = ancho_ventana
        self.ALTO_VENTANA = alto_ventana
        
        # Colores
        self.COLOR_FONDO = (135, 206, 235) # Cielo
        self.COLOR_SUELO = (0, 100, 0)      # Verde
        self.COLOR_OBSTACULO = (255, 0, 0)  # Rojo

        # El rectángulo del suelo (para colisión)
        self.suelo_rect = pygame.Rect(0, alto_ventana - 50, ancho_ventana, 50)
        
        # Lógica de obstáculos
        self.obstaculos = [] # Lista de todos los obstáculos en pantalla
        self.velocidad_juego = 8

        # Evento para generar obstáculos (el +1 es para que sea único)
        self.GENERAR_OBSTACULO = pygame.USEREVENT + 1
        pygame.time.set_timer(self.GENERAR_OBSTACULO, 1500) # Genera uno cada 1.5 seg

    def generar_obstaculo(self):
        """Crea un nuevo obstáculo a la derecha de la pantalla."""
        # Un obstáculo simple de 30x30
        nuevo_obstaculo = pygame.Rect(
            self.ANCHO_VENTANA,      # Posición X (fuera de la pantalla)
            self.suelo_rect.top - 30, # Posición Y (justo sobre el suelo)
            30, 30                   # Tamaño (ancho, alto)
        )
        self.obstaculos.append(nuevo_obstaculo)

    def update(self):
        """Mueve todos los obstáculos hacia la izquierda."""
        for obstaculo in self.obstaculos:
            obstaculo.x -= self.velocidad_juego
            
        # Elimina los obstáculos que ya salieron de la pantalla
        self.obstaculos = [obs for obs in self.obstaculos if obs.x > -50]

    def check_colision(self, jugador_rect):
        """Verifica si el jugador chocó con algún obstáculo."""
        for obstaculo in self.obstaculos:
            if jugador_rect.colliderect(obstaculo):
                return True # ¡Hubo colisión!
        return False # No hubo colisión

    def dibujar(self, superficie):
        """Dibuja el fondo, el suelo y todos los obstáculos."""
        # 1. Fondo
        superficie.fill(self.COLOR_FONDO)
        # 2. Suelo
        pygame.draw.rect(superficie, self.COLOR_SUELO, self.suelo_rect)
        # 3. Obstáculos
        for obstaculo in self.obstaculos:
            pygame.draw.rect(superficie, self.COLOR_OBSTACULO, obstaculo)