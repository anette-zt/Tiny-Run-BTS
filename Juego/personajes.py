# --- personajes.py ---
import pygame

class Jugador:
    # ¡MODIFICADO! Añadimos 'nombre_personaje' aquí
    def __init__(self, x, y, nombre_personaje):
        
        self.nombre = nombre_personaje
        
        # Por ahora, un simple rectángulo
        self.ancho = 40
        self.alto = 60
        
        # El color depende del nombre
        if self.nombre == "V":
            self.color = (128, 0, 128) # Morado (V)
        elif self.nombre == "J-Hope":
            self.color = (0, 150, 0)   # Verde (J-Hope)
        else:
            self.color = (200, 200, 200) # Gris (default)
        
        # El 'rect' es la "caja de colisión" del jugador
        self.rect = pygame.Rect(x, y, self.ancho, self.alto)
        
        # Físicas del salto
        self.v_velocidad_y = 0
        self.gravedad = 1
        self.fuerza_salto = -20
        self.esta_en_el_suelo = True
    
    # ... (El resto de tus funciones 'saltar', 'update' y 'dibujar' van aquí) ...
    
    def saltar(self):
        """Aplica la fuerza de salto si el jugador está en el suelo."""
        if self.esta_en_el_suelo:
            self.v_velocidad_y = self.fuerza_salto
            self.esta_en_el_suelo = False

    def update(self, suelo_rect):
        """Actualiza la física (gravedad y colisión con el suelo) cada frame."""
        if not self.esta_en_el_suelo:
            self.v_velocidad_y += self.gravedad
            self.rect.y += self.v_velocidad_y

        if self.rect.colliderect(suelo_rect):
            self.rect.bottom = suelo_rect.top
            self.v_velocidad_y = 0
            self.esta_en_el_suelo = True

    def dibujar(self, superficie):
        """Dibuja al jugador en la pantalla."""
        pygame.draw.rect(superficie, self.color, self.rect)