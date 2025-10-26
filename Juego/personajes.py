# --- personaje.py ---
import pygame

class Jugador:
    def __init__(self, x, y):
        # Por ahora, es un rectángulo morado.
        # Más adelante, aquí cargarías la imagen de TinyTAN V
        self.ancho = 40
        self.alto = 60
        self.color = (128, 0, 128) # Morado
        
        # El 'rect' es la "caja de colisión" del jugador
        self.rect = pygame.Rect(x, y, self.ancho, self.alto)
        
        # Físicas del salto
        self.v_velocidad_y = 0
        self.gravedad = 1
        self.fuerza_salto = -20 # Negativo es hacia arriba
        self.esta_en_el_suelo = True

    def saltar(self):
        """Aplica la fuerza de salto si el jugador está en el suelo."""
        if self.esta_en_el_suelo:
            self.v_velocidad_y = self.fuerza_salto
            self.esta_en_el_suelo = False

    def update(self, suelo_rect):
        """Actualiza la física (gravedad y colisión con el suelo) cada frame."""
        # 1. Aplicar gravedad si no está en el suelo
        if not self.esta_en_el_suelo:
            self.v_velocidad_y += self.gravedad
            self.rect.y += self.v_velocidad_y

        # 2. Comprobar colisión con el suelo
        if self.rect.colliderect(suelo_rect):
            self.rect.bottom = suelo_rect.top # Aterriza justo encima del suelo
            self.v_velocidad_y = 0
            self.esta_en_el_suelo = True

    def dibujar(self, superficie):
        """Dibuja al jugador en la pantalla."""
        pygame.draw.rect(superficie, self.color, self.rect)
# --- personaje.py ---