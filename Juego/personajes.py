# --- En la clase Jugador de personajes.py ---

def __init__(self, x, y, nombre_personaje):
    # ... (código existente) ...
    self.velocidad_x = 5 # ¡NUEVO! Velocidad de movimiento lateral

# ¡NUEVA FUNCIÓN!
def mover(self, direccion):
    """Mueve al jugador a la izquierda (-1) o derecha (1)"""
    if direccion == 1:
        self.rect.x += self.velocidad_x
    elif direccion == -1:
        self.rect.x -= self.velocidad_x
        
def update(self): # ¡YA NO NECESITA 'suelo_rect'!
    # 1. Aplicar gravedad
    if not self.esta_en_el_suelo:
        self.v_velocidad_y += self.gravedad
        self.rect.y += self.v_velocidad_y
    
    # 2. La colisión con el suelo ahora se manejará en 'escenarios.py'
    #    junto con la colisión de los ladrillos.
    #    Así que puedes simplificar esta función.
    self.esta_en_el_suelo = False # Asumimos que está en el aire