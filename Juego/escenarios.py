# --- escenarios.py ---
import pygame

# Ventana: ancho por defecto (usado por el dibujo de tiles)
ANCHO_VENTANA = 800

class Escenario:
    def __init__(self, nombre_imagen_fondo, mapa_del_nivel):
        # ... (cargas la imagen de fondo como antes) ...
        
        self.mapa_del_nivel = mapa_del_nivel
        self.TAMAÑO_TILE = 40 # Cada bloque (0, 1, 2) mide 40x40 píxeles
        
        # Cargar imágenes para los tiles (ladrillo, suelo, etc.)
        # self.suelo_img = pygame.image.load(...)
        # self.ladrillo_img = pygame.image.load(...)
        
        # Ya no necesitamos la lista 'obstaculos'
        # ¡YA NO SE GENERA NADA ALEATORIAMENTE!
        
        # Almacenaremos los rectángulos de colisión del nivel
        self.tiles_solidos = []
        self.crear_rects_colision()

    def crear_rects_colision(self):
        """Lee el 'mapa_del_nivel' y crea los Rects para colisiones"""
        self.tiles_solidos.clear()
        for fila_idx, fila in enumerate(self.mapa_del_nivel):
            for col_idx, tile in enumerate(fila):
                if tile == 1 or tile == 2: # Si es suelo o ladrillo
                    x = col_idx * self.TAMAÑO_TILE
                    y = fila_idx * self.TAMAÑO_TILE
                    rect_solido = pygame.Rect(x, y, self.TAMAÑO_TILE, self.TAMAÑO_TILE)
                    self.tiles_solidos.append(rect_solido)
    
    # ¡YA NO SE USA update()! El escenario es estático.
    
    def update_colisiones_jugador(self, jugador):
        """Maneja las colisiones del jugador con el escenario"""
        
        # Colisión Vertical (Salto y Gravedad)
        for tile_rect in self.tiles_solidos:
            if jugador.rect.colliderect(tile_rect):
                # Si está cayendo (colisión por arriba)
                if jugador.v_velocidad_y > 0:
                    jugador.rect.bottom = tile_rect.top
                    jugador.v_velocidad_y = 0
                    jugador.esta_en_el_suelo = True
                # Si está saltando (colisión por abajo)
                elif jugador.v_velocidad_y < 0:
                    jugador.rect.top = tile_rect.bottom
                    jugador.v_velocidad_y = 0 # Detiene el salto

        # Colisión Horizontal (Movimiento)
        # (Esta parte es más compleja, implica revisar colisiones
        #  antes de mover al jugador en X, pero lo omitimos por simplicidad)


    # ¡MODIFICADO! Ahora necesita la "cámara"
    def dibujar(self, superficie, camera_x):
        """Dibuja el fondo y los tiles del nivel según la cámara"""
        # 1. Fondo (que se mueva un poco para efecto parallax)
        superficie.blit(self.imagen_fondo, (-camera_x * 0.5, 0))
        
        # 2. Dibuja los tiles (ladrillos, suelo)
        for fila_idx, fila in enumerate(self.mapa_del_nivel):
            for col_idx, tile in enumerate(fila):
                # Calculamos la posición real EN EL MUNDO
                x = col_idx * self.TAMAÑO_TILE
                y = fila_idx * self.TAMAÑO_TILE
                
                # Calculamos la posición EN LA PANTALLA (restando la cámara)
                pos_en_pantalla_x = x - camera_x
                
                # Solo dibuja si está visible
                if -self.TAMAÑO_TILE < pos_en_pantalla_x < ANCHO_VENTANA:
                    if tile == 1: # Suelo
                        # pygame.draw.rect(superficie, (0, 100, 0), (pos_en_pantalla_x, y, self.TAMAÑO_TILE, self.TAMAÑO_TILE))
                        pass # Aquí dibujarías tu self.suelo_img
                    elif tile == 2: # Ladrillo
                        # pygame.draw.rect(superficie, (200, 100, 0), (pos_en_pantalla_x, y, self.TAMAÑO_TILE, self.TAMAÑO_TILE))
                        pass # Aquí dibujarías tu self.ladrillo_img