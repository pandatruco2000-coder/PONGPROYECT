from pygame import *

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

window = display.set_mode((ANCHO, ALTO))
display.set_caption(TITULO)
reloj = time.Clock()

fondo = transform.scale(image.load(IMG_FONDO), (ANCHO, ALTO))

messi = Player(IMG_MESSI, 0, ALTO // 2 - 60, 50, 120, 9)
cristiano = Player(IMG_CRISTIANO, ANCHO - 50, ALTO // 2 - 60, 50, 120, 9)
pelota = Ball(BALL, ANCHO // 2 - 15, ALTO // 2 - 15, 30, 30, 4, 4)

puntos_messi = 0
puntos_cristiano = 0
imagen_final = None

run = True
finish = False 
pausa = False 

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        
        if e.type == KEYDOWN:
            if e.key == K_p and not finish:
                pausa = not pausa
            
            if e.key == K_r:
                finish = False
                pausa = False
                puntos_messi = 0
                puntos_cristiano = 0
                pelota.rect.x = ANCHO // 2 - 15
                pelota.rect.y = ALTO // 2 - 15
                pelota.speed = 4
                pelota.speed_y = 4
                messi.rect.y = ALTO // 2 - 60
                cristiano.rect.y = ALTO // 2 - 60

    if not finish and not pausa:
        window.blit(fondo, (0, 0))

        messi.update_1()
        cristiano.update_2()
        pelota.update()

        if pelota.rect.colliderect(messi.rect) or pelota.rect.colliderect(cristiano.rect):
            pelota.speed *= -1
            if pelota.speed > 0: pelota.speed += 1
            else: pelota.speed -= 1
            if pelota.speed_y > 0: pelota.speed_y += 1
            else: pelota.speed_y -= 1

        if pelota.rect.x < 0:
            puntos_cristiano += 1
            pelota.rect.x = ANCHO // 2 - 15
            pelota.rect.y = ALTO // 2 - 15
            pelota.speed = 4  
            pelota.speed_y = 4

        if pelota.rect.x > ANCHO - pelota.rect.width:
            puntos_messi += 1
            pelota.rect.x = ANCHO // 2 - 15
            pelota.rect.y = ALTO // 2 - 15
            pelota.speed = -4 
            pelota.speed_y = 4

        if puntos_messi == 5:
            finish = True
            imagen_final = transform.scale(image.load(IMG_VIC_1), (ANCHO, ALTO))
        elif puntos_cristiano == 5:
            finish = True
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