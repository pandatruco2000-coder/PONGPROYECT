from pygame import *
import random

init()
font.init()
mixer.init()

ANCHO, ALTO = 800, 600
FPS = 60
TITULO = 'Ping Pong: El Clásico - Messi vs Cristiano'
COLOR_TEXTO = (0, 0, 0)

BALL = "pelota.webp"
IMG_FONDO = "fondo.jpg"
IMG_VIC_1 = "ganomessi.webp"
IMG_VIC_2 = "ganocris.jpg"
IMG_MESSI = "Messi.jpg.jpg"
IMG_CRISTIANO = "cris.jpg"

IMG_BALON = "balon de oro.jpg"
IMG_CHAMPIONS = "champions.jpg"

mixer.music.load("Fondoaudio.mp3")
mixer.music.set_volume(0.3) 
mixer.music.play(-1)

AUDIO_GOL_MESSI = mixer.Sound("Messigoal.mp3")
AUDIO_GOL_CRIS = mixer.Sound("cr7goal.mp3")

AUDIO_GOL_MESSI.set_volume(1.0)
AUDIO_GOL_CRIS.set_volume(1.0)

fuente_marcador = font.SysFont("Arial", 40, bold=True)
fuente_pausa = font.SysFont("Arial", 70, bold=True)

class GameSprite(sprite.Sprite):
    def __init__(self, sprite_img, x, y, w, h, speed):
        super().__init__()
        self.image = transform.scale(image.load(sprite_img), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
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

        if self.rect.y <= 0 or self.rect.y >= ALTO - self.rect.height:
            self.speed_y *= -1

class PowerUp(GameSprite):
    def __init__(self, sprite_img, x, y, w, h, tipo):
        super().__init__(sprite_img, x, y, w, h, 0)
        self.tipo = tipo
        self.activo_en_pantalla = False

window = display.set_mode((ANCHO, ALTO))
display.set_caption(TITULO)
reloj = time.Clock()

fondo = transform.scale(image.load(IMG_FONDO), (ANCHO, ALTO))

messi = Player(IMG_MESSI, 0, ALTO // 2 - 60, 50, 120, 9)
cristiano = Player(IMG_CRISTIANO, ANCHO - 50, ALTO // 2 - 60, 50, 120, 9)
pelota = Ball(BALL, ANCHO // 2 - 15, ALTO // 2 - 15, 30, 30, 4.0, 4.0)

power_messi = PowerUp(IMG_BALON, 40, 0, 40, 40, "messi")      
power_cristiano = PowerUp(IMG_CHAMPIONS, ANCHO - 80, 0, 40, 40, "cristiano") 

puntos_messi = 0
puntos_cristiano = 0
imagen_final = None

run = True
finish = False 
pausa = False 

tiempo_efecto_messi = 0
tiempo_efecto_cristiano = 0

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        
        if e.type == KEYDOWN:
            if e.key == K_p and not finish:
                pausa = not pausa
                if pausa:
                    mixer.music.pause()
                else:
                    mixer.music.unpause()
            
            if e.key == K_r:
                finish = False
                pausa = False
                mixer.music.play(-1)
                puntos_messi = 0
                puntos_cristiano = 0
                pelota.rect.x = ANCHO // 2 - 15
                pelota.rect.y = ALTO // 2 - 15
                pelota.speed = 4.0
                pelota.speed_y = 4.0
                messi.rect.y = ALTO // 2 - 60
                cristiano.rect.y = ALTO // 2 - 60
                power_messi.activo_en_pantalla = False
                power_cristiano.activo_en_pantalla = False

    if not finish and not pausa:
        window.blit(fondo, (0, 0))

        tiempo_actual = time.get_ticks()

        if tiempo_efecto_messi > 0 and tiempo_actual > tiempo_efecto_messi:
            messi.speed = 9
            messi.image = transform.scale(image.load(IMG_MESSI), (50, 120))
            messi.rect.width = 50
            messi.rect.height = 120
            tiempo_efecto_messi = 0

        if tiempo_efecto_cristiano > 0 and tiempo_actual > tiempo_efecto_cristiano:
            cristiano.speed = 9
            cristiano.image = transform.scale(image.load(IMG_CRISTIANO), (50, 120))
            cristiano.rect.width = 50
            cristiano.rect.height = 120
            tiempo_efecto_cristiano = 0

        if not power_messi.activo_en_pantalla and tiempo_efecto_messi == 0:
            if random.randint(1, 300) == 7:
                power_messi.rect.y = random.randint(50, ALTO - 90)
                power_messi.activo_en_pantalla = True

        if not power_cristiano.activo_en_pantalla and tiempo_efecto_cristiano == 0:
            if random.randint(1, 300) == 7:
                power_cristiano.rect.y = random.randint(50, ALTO - 90)
                power_cristiano.activo_en_pantalla = True

        messi.update_1()
        cristiano.update_2()
        pelota.update()

        if power_messi.activo_en_pantalla:
            power_messi.reset()
            if messi.rect.colliderect(power_messi.rect):
                power_messi.activo_en_pantalla = False
                tiempo_efecto_messi = tiempo_actual + 5000 
                efecto = random.randint(1, 2)
                if efecto == 1:
                    messi.speed = 18 
                else:
                    messi.image = transform.scale(image.load(IMG_MESSI), (50, 200))
                    messi.rect.height = 200

        if power_cristiano.activo_en_pantalla:
            power_cristiano.reset()
            if cristiano.rect.colliderect(power_cristiano.rect):
                power_cristiano.activo_en_pantalla = False # --- CORREGIDO AQUÍ ---
                tiempo_efecto_cristiano = tiempo_actual + 5000
                efecto = random.randint(1, 2)
                if efecto == 1:
                    cristiano.speed = 18
                else:
                    cristiano.image = transform.scale(image.load(IMG_CRISTIANO), (50, 200))
                    cristiano.rect.height = 200

        if pelota.rect.colliderect(messi.rect):
            pelota.speed *= -1
            if pelota.speed > 0: pelota.speed += 0.4
            else: pelota.speed -= 0.4
            if pelota.speed_y > 0: pelota.speed_y += 0.4
            else: pelota.speed_y -= 0.4
            pelota.rect.x = messi.rect.right + 1

        if pelota.rect.colliderect(cristiano.rect):
            pelota.speed *= -1
            if pelota.speed > 0: pelota.speed += 0.4
            else: pelota.speed -= 0.4
            if pelota.speed_y > 0: pelota.speed_y += 0.4
            else: pelota.speed_y -= 0.4
            pelota.rect.x = cristiano.rect.left - pelota.rect.width - 1

        if pelota.rect.x < 0:
            AUDIO_GOL_CRIS.play() 
            puntos_cristiano += 1
            pelota.rect.x = ANCHO // 2 - 15
            pelota.rect.y = ALTO // 2 - 15
            pelota.speed = 4.0  
            pelota.speed_y = 4.0

        if pelota.rect.x > ANCHO - pelota.rect.width:
            AUDIO_GOL_MESSI.play() 
            puntos_messi += 1
            pelota.rect.x = ANCHO // 2 - 15
            pelota.rect.y = ALTO // 2 - 15
            pelota.speed = -4.0 
            pelota.speed_y = 4.0

        if puntos_messi == 5:
            finish = True
            mixer.music.stop() 
            imagen_final = transform.scale(image.load(IMG_VIC_1), (ANCHO, ALTO))
        elif puntos_cristiano == 5:
            finish = True
            mixer.music.stop()
            imagen_final = transform.scale(image.load(IMG_VIC_2), (ANCHO, ALTO))

        messi.reset()
        cristiano.reset()
        pelota.reset()
        
        marcador = fuente_marcador.render(f"Messi: {puntos_messi}   -   CR7: {puntos_cristiano}", True, COLOR_TEXTO)
        window.blit(marcador, (ANCHO // 2 - 140, 20))
        
    elif pausa and not finish:
        texto_pausa = fuente_pausa.render("PAUSA", True, (255, 215, 0))
        window.blit(texto_pausa, (ANCHO // 2 - 110, ALTO // 2 - 50))

    elif finish:
        window.blit(imagen_final, (0, 0))

    display.update()
    reloj.tick(FPS)

quit()