# --- personajes.py ---
import pygame

class Jugador:
    def __init__(self, x, y, nombre_personaje):
        
        self.nombre = nombre_personaje
        self.ancho = 40
        self.alto = 60
        
        if self.nombre == "V":
            self.color = (128, 0, 128) # Morado (V)
        elif self.nombre == "J-Hope":
            self.color = (0, 150, 0)   # Verde (J-Hope)
        else:
            self.color = (200, 200, 200) # Gris (default)
        
        # El 'rect' es la "caja de colisión" y posición EN EL MUNDO
        self.rect = pygame.Rect(x, y, self.ancho, self.alto)
        
        # --- Físicas (¡Modificadas!) ---
        self.vel_x = 5  # ¡NUEVO! Velocidad de movimiento lateral
        self.vel_y = 0  # Velocidad vertical
        self.gravedad = 1
        self.fuerza_salto = -20
        self.esta_en_el_suelo = False # Empieza en el aire hasta que toque el suelo

    def saltar(self):
        """Aplica la fuerza de salto si el jugador está en el suelo."""
        if self.esta_en_el_suelo:
            self.vel_y = self.fuerza_salto
            self.esta_en_el_suelo = False # Ya no está en el suelo

    def update_horizontal(self, teclas):
        """Maneja el movimiento de Izquierda/Derecha basado en las teclas."""
        if teclas[pygame.K_d]:
            self.rect.x += self.vel_x
        if teclas[pygame.K_a]:
            self.rect.x -= self.vel_x

    def update_vertical(self):
        """Maneja la gravedad y el salto."""
        # Aplicar gravedad
        self.vel_y += self.gravedad
        # Limitar velocidad de caída
        if self.vel_y > 15:
            self.vel_y = 15
        
        self.rect.y += self.vel_y
        
        # Asumimos que no está en el suelo hasta que las colisiones digan lo contrario
        self.esta_en_el_suelo = False

    def dibujar(self, superficie, camera_x):
        """Dibuja al jugador en la pantalla, ajustado por la cámara."""
        
        # Creamos un Rect temporal solo para dibujar
        # Su posición en pantalla es su posición en el mundo MENOS la cámara
        rect_en_pantalla = self.rect.copy()
        rect_en_pantalla.x -= camera_x
        
        # Dibujamos ese rect temporal
        pygame.draw.rect(superficie, self.color, rect_en_pantalla)