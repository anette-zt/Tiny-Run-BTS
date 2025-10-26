# --- musica.py ---
import pygame
import random
import os

class GestorMusica:
    def __init__(self, music_end_event):
        # 1. Creamos la playlist
        self.playlist = []
        # Buscamos todos los archivos .mp3 en la carpeta 'musica'
        for archivo in os.listdir('musica'):
            if archivo.endswith('.mp3'):
                self.playlist.append(os.path.join('musica', archivo))
        
        print(f"Playlist cargada con {len(self.playlist)} canciones.")
        
        # 2. Configuramos el evento de fin de canción
        # Le decimos a Pygame que "active" este evento cuando una canción termine
        self.MUSIC_END_EVENT = music_end_event
        pygame.mixer.music.set_endevent(self.MUSIC_END_EVENT)

    def cargar_y_reproducir(self):
        """Inicia la reproducción de la playlist."""
        if not self.playlist:
            print("No hay canciones en la carpeta /musica/")
            return
        self.reproducir_siguiente_cancion()

    def reproducir_siguiente_cancion(self):
        """Elige una canción aleatoria y la reproduce."""
        if self.playlist:
            try:
                siguiente_cancion = random.choice(self.playlist)
                pygame.mixer.music.load(siguiente_cancion)
                pygame.mixer.music.play(1) # '1' significa que se reproduce una vez
                print(f"Reproduciendo ahora: {siguiente_cancion}")
            except pygame.error as e:
                print(f"No se pudo cargar la música: {e}")