# --- escenarios.py ---
import pygame
import random
import os # ¡NUEVO! Necesario para unir rutas de archivos

class Escenario:
    # ¡MODIFICADO! Añadimos 'nombre_imagen_fondo'
    def __init__(self, ancho_ventana, alto_ventana, nombre_imagen_fondo):
        self.ANCHO_VENTANA = ancho_ventana
        self.ALTO_VENTANA = alto_ventana
        
        # --- ¡NUEVO! Carga de la imagen de fondo ---
        try:
            # Une la carpeta 'escenarios' con el nombre del archivo (ej: "escenarios/IDOL.jpg")
            ruta_imagen = os.path.join('escenarios', nombre_imagen_fondo)
            # Carga la imagen original
            imagen_original = pygame.image.load(ruta_imagen)
            # Escala la imagen al tamaño de tu ventana
            self.imagen_fondo = pygame.transform.scale(imagen_original, (ancho_ventana, alto_ventana))
            print(f"Fondo '{nombre_imagen_fondo}' cargado correctamente.")
        except FileNotFoundError:
            print(f"¡ERROR! No se encontró el archivo: {ruta_imagen}")
            # Si falla, crea un fondo azul de emergencia
            self.imagen_fondo = pygame.Surface((ancho_ventana, alto_ventana))
            self.imagen_fondo.fill((135, 206, 235)) # Color cielo
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")

        # --- Colores ---
        self.COLOR_SUELO = (0, 100, 0)
        self.COLOR_OBSTACULO = (255, 0, 0)

        # El rectángulo del suelo (para colisión)
        self.suelo_rect = pygame.Rect(0, alto_ventana - 50, ancho_ventana, 50)
        
        # Lógica de obstáculos
        self.obstaculos = []
        self.velocidad_juego = 8

        # Evento para generar obstáculos (el +1 es para que sea único)
        self.GENERAR_OBSTACULO = pygame.USEREVENT + 1
        pygame.time.set_timer(self.GENERAR_OBSTACULO, 1500)

    def generar_obstaculo(self):
        """Crea un nuevo obstáculo a la derecha de la pantalla."""
        nuevo_obstaculo = pygame.Rect(
            self.ANCHO_VENTANA,
            self.suelo_rect.top - 30,
            30, 30
        )
        self.obstaculos.append(nuevo_obstaculo)

    def update(self):
        """Mueve todos los obstáculos hacia la izquierda."""
        for obstaculo in self.obstaculos:
            obstaculo.x -= self.velocidad_juego
            
        self.obstaculos = [obs for obs in self.obstaculos if obs.x > -50]

    def check_colision(self, jugador_rect):
        """Verifica si el jugador chocó con algún obstáculo."""
        for obstaculo in self.obstaculos:
            if jugador_rect.colliderect(obstaculo):
                return True
        return False

    def dibujar(self, superficie):
        """Dibuja el fondo, el suelo y todos los obstáculos."""
        # 1. ¡MODIFICADO! Dibuja la imagen de fondo en lugar del color
        superficie.blit(self.imagen_fondo, (0, 0))
        
        # 2. Suelo (podemos hacerlo transparente para ver el fondo)
        # superficie.fill((0, 0, 0, 0)) # -> esto es para transparencia
        pygame.draw.rect(superficie, self.COLOR_SUELO, self.suelo_rect)
        
        # 3. Obstáculos
        for obstaculo in self.obstaculos:
            pygame.draw.rect(superficie, self.COLOR_OBSTACULO, obstaculo)