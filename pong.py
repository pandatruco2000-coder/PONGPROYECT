from pygame import *

# 1. INICIALIZACIÓN
init()
font.init()
mixer.init()

# 2. CONFIGURACIÓN Y CONSTANTES
# Es recomendable usar nombres descriptivos para facilitar el mantenimiento
ANCHO, ALTO = 800, 600
FPS = 60
TITULO = 'Plantilla Base Pygame'
COLOR_FONDO = (30, 30, 30) # Un gris oscuro para no cansar la vista
RAQUETA = "raqueta.jpg"
BALL = "pelota.png"
# 3. DEFINICIÓN DE CLASES
class GameSprite(sprite.Sprite):
    """Clase base para todos los objetos visuales del juego."""
    def __init__(self, sprite_img, x, y, w, h, speed):
        super().__init__()
        self.image = transform.scale(image.load(sprite_img), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def reset(self):
        """Dibuja el sprite en su posición actual."""
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    """Clase para el personaje controlado por el usuario."""
    def update_1(self):
        keys = key.get_pressed()

        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < ALTO - self.rect.height:
            self.rect.y += self.speed

    def update_2(self):
        keys = key.get_pressed()
        
        if keys[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < ALTO - self.rect.height:
            self.rect.y += self.speed

class Ball(GameSprite):
    def __init__(self, sprite_img, x, y, w, h, speed, speed_y):
        super().__init__(sprite_img, x, y, w, h, speed)
        self.speed_y = speed_y
    def update(self):
        self.rect.x += self.speed
        self.rect.y += self.speed_y

# 4. INSTANCIACIÓN DE OBJETOS
window = display.set_mode((ANCHO, ALTO))
display.set_caption(TITULO)
reloj = time.Clock()

# Aquí se crearían los grupos de sprites y objetos individuales
player_1 = Player(RAQUETA, 5, ALTO // 2, 40, 100, 5)
player_2 = Player(RAQUETA, ANCHO - 45, ALTO // 2, 40, 100, 5)
pelota = Ball(BALL, ANCHO // 2, ALTO // 2 , 10, 50, 6, 9)

# 5. CICLO PRINCIPAL (GAME LOOP)
run = True
finish = False # Variable para controlar estados (Ej: Pantalla de Game Over)

while run:
    # --- A. Gestión de Eventos ---
    for e in event.get():
        if e.type == QUIT:
            run = False
        
        # Reinicio del juego con una tecla
        if e.type == KEYDOWN:
            if e.key == K_r:
                finish = False
                # Aquí se debería resetear la posición de los objetos

    # --- B. Lógica del Juego (Solo si no ha terminado) ---
    if not finish:
        window.fill(COLOR_FONDO)

        # Actualizar posiciones
        player_1.update_1()
        player_2.update_2()
        pelota.update()


        # Dibujar elementos
        player_1.reset()
        player_2.reset()
        pelota.reset()

        # Ejemplo de condición de fin
        # if sprite.spritecollide(player, enemies, False):
        #     finish = True

    # --- C. Actualización de Pantalla ---
    display.update()
    reloj.tick(FPS)

# Al salir del ciclo, cerrar recursos
quit()