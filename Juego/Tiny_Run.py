import pygame
import sys
import random

# Inicializa Pygame
pygame.init()

# Configuración de ventana
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("PIXIVIDAD - Estilo Mario Bros")

# Fuente para los puntos
fuente = pygame.font.Font(None, 36)

# Colores
AZUL_CIELO = (135, 206, 235)
MARRON_SUELO = (139, 69, 19)
VERDE_PLATAFORMA = (0, 200, 0)

# Variables del juego
puntos = 0
gravedad = 0.5

# _____________________________
# CLASES
# _____________________________

class Jugador(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Cargar sprites
        self.image_derecha = pygame.image.load("V/V.jpg").convert()
        self.image_derecha.set_colorkey((255, 255, 255))
        self.image_derecha = pygame.transform.scale(self.image_derecha, (50, 70))

        self.image_izquierda = pygame.image.load("V/V.jpg").convert()
        self.image_izquierda.set_colorkey((255, 255, 255))
        self.image_izquierda = pygame.transform.scale(self.image_izquierda, (50, 70))

        self.image = self.image_derecha
        self.rect = self.image.get_rect(center=(x, y))
        self.vel_x = 0
        self.vel_y = 0
        self.en_suelo = False

    def mover(self, teclas):
        self.vel_x = 0
        if teclas[pygame.K_LEFT]:
            self.vel_x = -5
            self.image = self.image_izquierda
        if teclas[pygame.K_RIGHT]:
            self.vel_x = 5
            self.image = self.image_derecha
        if teclas[pygame.K_SPACE] and self.en_suelo:
            self.vel_y = -10  # salto
            self.en_suelo = False

    def aplicar_gravedad(self):
        self.vel_y += gravedad
        if self.vel_y > 10:
            self.vel_y = 10

    def update(self, plataformas):
        # Movimiento horizontal
        self.rect.x += self.vel_x

        # Gravedad
        self.aplicar_gravedad()
        self.rect.y += self.vel_y

        # Colisiones con plataformas
        self.en_suelo = False
        for plataforma in plataformas:
            if self.rect.colliderect(plataforma.rect):
                # Ver si viene cayendo
                if self.vel_y > 0 and self.rect.bottom > plataforma.rect.top:
                    self.rect.bottom = plataforma.rect.top
                    self.vel_y = 0
                    self.en_suelo = True

        # Limitar bordes
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO

class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, ancho, alto):
        super().__init__()
        self.image = pygame.Surface((ancho, alto))
        self.image.fill(VERDE_PLATAFORMA)
        self.rect = self.image.get_rect(topleft=(x, y))

class Moneda(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("sprites-coins/sprite1-1.jpg").convert()
        self.image.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect(center=(x, y))

# _____________________________
# CONFIGURACIÓN DEL MUNDO
# _____________________________

# Jugador
jugador = Jugador(100, 450)
grupo_jugador = pygame.sprite.GroupSingle(jugador)

# Plataformas
grupo_plataformas = pygame.sprite.Group()
plataforma_suelo = Plataforma(0, 550, ANCHO, 50)
grupo_plataformas.add(plataforma_suelo)

# Plataformas adicionales
grupo_plataformas.add(Plataforma(200, 450, 150, 20))
grupo_plataformas.add(Plataforma(450, 350, 150, 20))
grupo_plataformas.add(Plataforma(650, 250, 100, 20))

# Monedas
grupo_monedas = pygame.sprite.Group()
for _ in range(5):
    x = random.randint(100, 700)
    y = random.choice([200, 300, 400])
    grupo_monedas.add(Moneda(x, y))

# _____________________________
# BUCLE PRINCIPAL
# _____________________________

clock = pygame.time.Clock()
corriendo = True

while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    teclas = pygame.key.get_pressed()
    jugador.mover(teclas)

    # Actualizar jugador
    jugador.update(grupo_plataformas)

    # Colisiones con monedas
    colisiones = pygame.sprite.spritecollide(jugador, grupo_monedas, dokill=True)
    if colisiones:
        puntos += 10

    # Si se acaban las monedas, aparecen nuevas
    if len(grupo_monedas) == 0:
        for _ in range(5):
            x = random.randint(100, 700)
            y = random.choice([200, 300, 400])
            grupo_monedas.add(Moneda(x, y))

    # _____________________________
    # DIBUJAR
    # _____________________________
    pantalla.fill(AZUL_CIELO)

    # Suelo
    pygame.draw.rect(pantalla, MARRON_SUELO, (0, 550, ANCHO, 50))

    grupo_plataformas.draw(pantalla)
    grupo_monedas.draw(pantalla)
    grupo_jugador.draw(pantalla)

    # Texto de puntos
    texto_puntos = fuente.render(f"Puntos: {puntos}", True, (0, 0, 0))
    pantalla.blit(texto_puntos, (20, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
