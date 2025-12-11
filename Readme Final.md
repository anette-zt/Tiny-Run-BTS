# Tiny Run BTS - Proyecto Final de Graficacion

## Descripcion General
Este proyecto es un videojuego de plataformas en 2D desarrollado como entrega final para la materia de Graficacion. 
El juego integra manejo de sprites, sonido y bases de datos.

El objetivo de V es navegar por el nivel saltando entre plataformas, esquivando a los enemigos rojos y recolectando todos los "Lightsticks" para completar el juego.

## Inspiracion y Desarrollo
Este proyecto toma como referencia un tarea sobre "colisiones" realizado en clase. 
A partir de esa base, se expandio el codigo para incluir gravedad, estados del juego (Menu, Juego, Fin) y una estructura mas compleja.

La identidad visual y la tematica del juego estan inspiradas en la banda BTS. Se han personalizado los elementos graficos y sonoros para reflejar este gusto personal, convirtiendo la recoleccion de items en una busqueda de los iconicos Lightsticks del grupo.

## Caracteristicas Tecnicas
1. Lenguaje y Librerias: Escrito en Python utilizando Pygame.
2. Base de Datos: Uso de SQLite para guardar y consultar el puntaje maximo (Record) localmente.
3. Colisiones: Sistema logico para detectar contacto con plataformas (suelo), enemigos (daño) y objetos (puntos).
4. Inteligencia Artificial Basica: Los enemigos patrullan su plataforma y cambian de direccion al tocar bordes.
5. Interfaz Grafica: Incluye menu principal, puntuacion en tiempo real y pantallas de finalizacion.

## Controles
- Flecha Izquierda: Mover personaje a la izquierda.
- Flecha Derecha: Mover personaje a la derecha.
- Barra Espaciadora: Saltar.

## Ejecucion
Para correr el juego, asegurese de tener instalado Python y la libreria Pygame. Ejecute el archivo principal desde la terminal:

> python tiny_run_bts.py

## Creditos
- Desarrollado por: Ariam Anette Zurita Torres
- Asignatura: Graficacion
- Fecha de entrega: Diciembre 2025