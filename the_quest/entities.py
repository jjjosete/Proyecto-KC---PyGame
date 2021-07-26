from the_quest import HEIGHT, WIDTH, FPS, WHITE, BLACK, RED, BLUE, GREEN, img_dir, music_dir

from os import path
import pygame
from pygame import font
import random





#Marcador
class Marcador(pygame.sprite.Sprite):
    plantilla = "{}"

    def __init__(self, x, y, justificado = "topleft", fontsize=25, color=WHITE):
        super().__init__()
        self.fuente = pygame.font.Font(None, fontsize)
        self.contador = 0
        self.color = color
        self.x = x
        self.y = y
        self.justificado = justificado
        self.image = self.fuente.render(str(self.plantilla.format(self.contador)), True, self.color)
      
    def update(self):
        self.image = self.fuente.render(str(self.plantilla.format(self.contador)), True, self.color)
        d = {self.justificado: (self.x, self.y)}
        self.rect = self.image.get_rect(**d)

class Player(pygame.sprite.Sprite):
    
    class Estado():
        volando = 0
        preAterrizando=1
        aterrizando = 2
        fin = 3

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #colocamos la imagen
        self.player_img = pygame.image.load(path.join(img_dir, "playerShip1_red.png")).convert() 
        self.imageOriginal = pygame.transform.scale(self.player_img,(38, 50))
        self.imageOriginal.set_colorkey(BLACK)
        self.image = self.imageOriginal.copy()
        #posicion inicial        
        self.rect = self.image.get_rect()
        self.radius = 20
       # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.top = (HEIGHT // 2) - 20
        self.rect.left = 50
        #incio velocidad a 0
        self.speedY = 0
        self.teclasPulsadas = True
        self.rotacion = 0 
        self.vRotacion = 6.2
        self.last_update = pygame.time.get_ticks()
        self.estado = self.Estado.volando
        

    def update(self):
        #inicio la velocidad a 0 y la subo o la bajo según la tecla pulsada 
        if self.estado == self.Estado.volando or self.Estado.preAterrizando:
            self.speedY = 0
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_DOWN] and self.teclasPulsadas:
                self.speedY = 7
            else: 
                pass
            if keystate[pygame.K_UP]and self.teclasPulsadas:
                self.speedY = -7
            else: 
                pass
            #actualizo la posición del eje.Y con la velocidad.
            self.rect.y += self.speedY
            #Restringir movimientos a la pantalla
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT
            if self.rect.top < 0:
                self.rect.top = 0
        elif self.estado == self.Estado.preAterrizando:
            pass
        elif self.estado== self.Estado.aterrizando:
            self.aterrizaje()

    def reset(self):
        self.player_img = pygame.image.load(path.join(img_dir, "playerShip1_red.png")).convert() 
        self.image = pygame.transform.scale(self.player_img,(38, 50))
        self.image.set_colorkey(BLACK)
        self.rect.left = 50
        self.rect.top = (HEIGHT // 2) - 20
        self.teclasPulsadas = True
        self.estado = self.Estado.volando

    def aterrizaje(self):
        
        if self.rect.top > 175:
            self.rect.y -=1
        elif self.rect.top < 175:
            self.rect.y +=1
        elif self.rect.bottom > 225:
            self.rect.y -=1
        elif self.rect.bottom < 225:
            self.rect.y += 1
        else:
            pass

        if self.rect.left < 612:
            self.rect.x += 5
        #vuelta 180 grados
            now = pygame.time.get_ticks()   
            if now - self.last_update > 50: 
                self.last_update = now
                self.rotacion = (self.rotacion + self.vRotacion) % 180
                newImage = pygame.transform.rotate(self.imageOriginal, self.rotacion)
                old_center = self.rect.center
                self.image = newImage
                self.rect = self.image.get_rect()
                self.rect.center = old_center
                self.teclasPulsadas = False
            
        else:
            pass
        
class Asteroides(pygame.sprite.Sprite):
   
    asteroides_lista = ["meteorBrown_big1.png", "meteorBrown_big2.png",'meteorBrown_med2.png',
                    "meteorBrown_med1.png", "meteorBrown_small1.png","meteorBrown_small2.png",
                    "meteorBrown_tiny1.png"]
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #superficie y color de asteroides
        
        self.image = self.cargaImagenes()
        self.image.set_colorkey(BLACK)
        #posición inicial
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .8// 2)
       # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.y = random.randrange(HEIGHT - self.rect.height)
        self.rect.x = random.randrange(780, 800)
        #velocidad
        self.speedx = random.randrange(8,12)
        #self.speedy = random.randrange(-3, 3)       
       
    def update(self):
        #actualizar posición con velocidad
        #self.rect.y -= self.speedy
        self.rect.x  -= self.speedx
        #reaparición de asteroides
        if self.rect.left < -40:
            self.rect.y = random.randrange(HEIGHT - self.rect.height)
            self.rect.x = random.randrange(820, 850)
            
    def cargaImagenes(self): 
        asteroides_img= []
        for img in self.asteroides_lista:
            asteroides_img.append(pygame.image.load(path.join(img_dir, img)).convert())
        
        return random.choice(asteroides_img)
          
class Explosion(pygame.sprite.Sprite):
    
    expl_img = []
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = self.cargaImagenes()
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
        
    def update(self):
        now = pygame.time.get_ticks()
                
        if now -self.last_update > self.frame_rate:
            self.last_update = now
            self.frame +=1
            if self.frame == len(self.expl_img):
                self.kill()
                
            else:
                center = self.rect.center
                self.image = self.expl_img[self.frame] 
                self.rect = self.image.get_rect()
                self.rect.center = center
    
    
    def cargaImagenes(self):
        if len(self.expl_img) == 0:

            for i in range(9):
                filename = 'regularExplosion0{}.png'.format(i)
                img = pygame.image.load(path.join(img_dir, filename)).convert()
                img.set_colorkey(BLACK)
                img_def = pygame.transform.scale(img, (75, 75))
                self.expl_img.append(img_def)
            return self.expl_img[0]
        else: 
            return self.expl_img[0]
        
class Planeta(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #colocamos la imagen
        self.planeta_img = pygame.image.load(path.join(img_dir, "planeta1.png")).convert() 
        self.image = pygame.transform.scale(self.planeta_img,(400, 402))
        
        self.image.set_colorkey(WHITE)
        #posicion inicial        
        self.rect = self.image.get_rect()
        self.rect.left = 800
        self.radius= 362


    def update(self):
        if self.rect.left > 600:
            self.rect.x -= 3
        else:
            pass
            