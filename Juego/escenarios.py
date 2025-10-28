# --- escenarios.py ---
import pygame
import os

class Escenario:
    def __init__(self, ancho_ventana, alto_ventana, nombre_imagen_fondo, mapa_lista, tamaño_tile):
        self.ANCHO_VENTANA = ancho_ventana
        self.ALTO_VENTANA = alto_ventana
        self.TAMAÑO_TILE = tamaño_tile
        
        # Carga de la imagen de fondo (igual que antes)
        try:
            ruta_imagen = os.path.join('escenarios', nombre_imagen_fondo)
            imagen_original = pygame.image.load(ruta_imagen)
            self.imagen_fondo = pygame.transform.scale(imagen_original, (ancho_ventana, alto_ventana))
            print(f"Fondo '{nombre_imagen_fondo}' cargado correctamente.")
        except Exception as e:
            print(f"Error al cargar la imagen de fondo: {e}")
            self.imagen_fondo = pygame.Surface((ancho_ventana, alto_ventana))
            self.imagen_fondo.fill((135, 206, 235))

        # Colores
        self.COLOR_SUELO = (0, 100, 0)      # Verde para tiles
        self.COLOR_FONDO_PARALLAX = (50, 50, 150) # Un fondo B por si la imagen no cubre todo
        
        # --- ¡NUEVO! Lógica de Mapa ---
        self.mapa_lista = mapa_lista
        self.tiles_solidos = [] # Lista de Rects para colisiones
        self.crear_mapa()
        
        # Ya no se necesita un timer de obstáculos

    def crear_mapa(self):
        """Lee la 'mapa_lista' y crea los Rects para colisiones."""
        self.tiles_solidos.clear()
        
        # 'enumerate' nos da el índice (y) y el contenido (fila)
        for fila_idx, fila in enumerate(self.mapa_lista):
            # 'enumerate' nos da el índice (x) y el contenido (tipo_tile)
            for col_idx, tipo_tile in enumerate(fila):
                
                # Si el tile es '1' (suelo/ladrillo), crea un Rect
                if tipo_tile == '1':
                    x = col_idx * self.TAMAÑO_TILE
                    y = fila_idx * self.TAMAÑO_TILE
                    tile_rect = pygame.Rect(x, y, self.TAMAÑO_TILE, self.TAMAÑO_TILE)
                    self.tiles_solidos.append(tile_rect)

    def check_colisiones_horizontal(self, jugador):
        """Revisa y corrige colisiones en el eje X."""
        for tile in self.tiles_solidos:
            if jugador.rect.colliderect(tile):
                # Si el jugador se movía a la derecha y chocó
                if jugador.rect.right > tile.left and jugador.rect.left < tile.left:
                    jugador.rect.right = tile.left # Lo frena
                
                # Si el jugador se movía a la izquierda y chocó
                elif jugador.rect.left < tile.right and jugador.rect.right > tile.right:
                    jugador.rect.left = tile.right # Lo frena

    def check_colisiones_vertical(self, jugador):
        """Revisa y corrige colisiones en el eje Y."""
        for tile in self.tiles_solidos:
            if jugador.rect.colliderect(tile):
                # Si el jugador está cayendo (colisión por arriba del tile)
                if jugador.vel_y > 0 and jugador.rect.bottom > tile.top and jugador.rect.top < tile.top:
                    jugador.rect.bottom = tile.top
                    jugador.vel_y = 0
                    jugador.esta_en_el_suelo = True # ¡Está en el suelo!
                
                # Si el jugador está saltando (colisión por abajo del tile)
                elif jugador.vel_y < 0 and jugador.rect.top < tile.bottom and jugador.rect.bottom > tile.bottom:
                    jugador.rect.top = tile.bottom
                    jugador.vel_y = 0 # Detiene el salto

    def dibujar(self, superficie, camera_x):
        """Dibuja el fondo y todos los tiles, ajustados por la cámara."""
        
        # 1. Fondo (color sólido)
        superficie.fill(self.COLOR_FONDO_PARALLAX)
        
        # 2. Imagen de fondo (con efecto parallax)
        # Se mueve a la mitad de velocidad que la cámara para dar profundidad
        fondo_x = -camera_x * 0.5
        superficie.blit(self.imagen_fondo, (fondo_x, 0))
        
        # 3. Dibuja los tiles (suelo, ladrillos)
        for tile in self.tiles_solidos:
            # Ajustamos la posición X del tile por la cámara
            rect_en_pantalla = tile.copy()
            rect_en_pantalla.x -= camera_x
            
            # Dibujamos el tile
            pygame.draw.rect(superficie, self.COLOR_SUELO, rect_en_pantalla)