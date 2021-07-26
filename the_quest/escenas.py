from the_quest import WIDTH, HEIGHT, FPS, img_dir, music_dir, BLACK, WHITE, BLUE, RED, GREEN
from the_quest.entities import Marcador, Player, Asteroides, Explosion, Planeta
from data.dbconfig import db_path
from os import path, sys
from pygame import display, font
import random
import sqlite3
import pygame 




class Escene():
    def __init__(self, pantalla):
        self.screen = pantalla
        self.all_sprites = pygame.sprite.Group()
        self.reloj = pygame.time.Clock()
    
    def reset(self):
        pass

    
    def bucle_principal(self):
        pass

    def maneja_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT or \
                evento.type == pygame.KEYDOWN and evento.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

class Game():

    def __init__(self, screen):
        self.screen = screen
        self.all_sprites = pygame.sprite.Group()
        self.explosionSound = pygame.mixer.Sound(path.join(music_dir, "expl6.wav"))
        self.cuentaVidas = Marcador(790, 10, "topright", 30)
        
        self.cuentaVidas.plantilla = "Vidas: {}"
        self.asteroides = pygame.sprite.Group()
        self.cuentaPuntos = Marcador(10,10, fontsize=30)
        self.cuentaPuntos.plantilla = "Puntos: {}"
    
        self.player = Player()
        self.planeta = Planeta()
        self.grupoPlaneta = pygame.sprite.Group()
        self.grupoPlaneta.add(self.planeta)

        self.fondo = pygame.image.load(path.join(img_dir, "background.png")).convert()     
        self.fondo_rect = self.fondo.get_rect()  
        self.caption = pygame.display.set_caption("The Quest")

        self.all_sprites.add(self.cuentaPuntos)
        self.all_sprites.add(self.cuentaVidas)
        self.all_sprites.add(self.player)
        self.vidas = 3
        self.puntos = 0
        self.last_update = pygame.time.get_ticks()
        self.espera = 500

    def creaAsteroides(self):
        if self.cuentaPuntos.contador < 35:
            for i in range(4):
                self.ast = Asteroides()
                self.all_sprites.add(self.ast)
                self.asteroides.add(self.ast)
        else:
            for i in range(6):
                self.ast = Asteroides()
                self.ast.speedx = random.randrange(10, 15)
                self.all_sprites.add(self.ast)
                self.asteroides.add(self.ast)

        
    def reset(self):
        self.vidas = 3
        self.puntos = 0
        self.player.reset()
        self.all_sprites.empty()
        self.all_sprites.add(self.cuentaPuntos)
        self.all_sprites.add(self.cuentaVidas)
        self.all_sprites.add(self.player)
        self.creaAsteroides()

    def mensaje(self, mensaje, x, y):
        self.instrucciones = Marcador(x, y, "topleft", 30, (255, 255, 255))
        self.instrucciones.contador = '{}'.format(mensaje)
        self.all_sprites.add(self.instrucciones)
        teclas_pulsadas = pygame.key.get_pressed()
        if teclas_pulsadas[pygame.K_SPACE]:
            self.running = False

    def mensaje1(self):
                self.mensaje("Enhorabuena!, has conseguido encontrar un planeta!!!", 150, 75)
                self.mensaje("Pero no es lo suficientemente grande, hay que seguir buscando!", 105, 125)
                self.mensaje("Pulsa espacio para continuar", 250, 175)
                teclas_pulsadas = pygame.key.get_pressed()
                if teclas_pulsadas[pygame.K_SPACE]:
                    Game.reset(self)
                    self.vidas = self.vidasActuales
                    self.puntos = 60 
                    

    def mensaje2(self):
                self.mensaje("Enhorabuena!, has conseguido encontrar un planeta!!!", 130, 75)
                self.mensaje("Éste sí es el planeta que la humanidad necesita!", 145, 125)
                self.mensaje("Tu temeraria conducción por el espacio ha salvado a la humanidad!!", 90, 175)
                self.mensaje("Escribe tu nombre en la historia!", 250, 225)
                global globalPuntos 
                globalPuntos = self.cuentaPuntos.contador
                teclas_pulsadas = pygame.key.get_pressed()
                if teclas_pulsadas[pygame.K_SPACE]:
                    running = False
                
    def gameOver(self):
        self.all_sprites.empty()
        game = Game(self.screen)
        font.init
        fuente=pygame.font.Font(None,50)
        mensajeGameOver = fuente.render("SACABAO L'JUEGO, YA LO SIENTO", 1, WHITE)
        game.screen.blit(game.fondo, game.fondo_rect)
        game.screen.blit(mensajeGameOver, (110, 300))
        pygame.display.flip()
        pygame.time.delay(1500)
        
    def bucle_principal(self): 
        pygame.display.init()
        
        clock = pygame.time.Clock()
        pygame.mixer.music.load(path.join(music_dir,"high_tech_lab.flac"))
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(loops=-1)
        running = True 
        
        while running :
            #ajustar la velocidad
            clock.tick(FPS)
            seconds=(pygame.time.get_ticks())
            self.cuentaPuntos.contador = self.puntos
            self.cuentaVidas.contador = self.vidas

            #procesando inputs/eventos
            for event in pygame.event.get():
                #procesando si se cierra la ventana
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
            
            #instrucciones para los estados
            if self.player.estado == self.player.Estado.volando:
                            #comprobar colisión
                
                colisiones = pygame.sprite.spritecollide(self.player, self.asteroides, True, pygame.sprite.collide_circle)
                anticolision = False
                start_time = pygame.time.get_ticks()                 
                for colision in colisiones:
                    
                    if colision and not anticolision:

                        anticolision = True 
                                          
                        expl = Explosion(colision.rect.center)
                        self.explosionSound.play()
                        self.all_sprites.add(expl)                  
                        self.vidas -= 1
                        now = pygame.time.get_ticks()
                        
                        
                        if now- self.last_update > self.espera:
                            self.last_update = now
                    
                        else:
                            
                            anticolision = False
                                
                    else:
                        pass

                    if self.vidas == 0:     
                        self.gameOver()
                        running= False

            elif self.player.estado == self.player.Estado.preAterrizando:            
                if len(self.asteroides) != 0:
                    for asteroide in self.asteroides:
                        if asteroide.rect.left < -10:
                            asteroide.kill()
                        else:
                            pass     
                colisiones = pygame.sprite.spritecollide(self.player, self.asteroides, True, pygame.sprite.collide_circle)
                anticolision = False
            
                for colision in colisiones:
                    
                    if colision and not anticolision:

                        anticolision = True                       
                        expl = Explosion(colision.rect.center)
                        self.explosionSound.play()
                        self.all_sprites.add(expl)                  
                        self.vidas -= 1
                            
            elif self.player.estado == self.player.Estado.aterrizando and self.puntos < 100:
                self.all_sprites.add(self.planeta)   
                self.player.aterrizaje()
                self.vidasActuales = self.vidas
                choque = pygame.sprite.spritecollide(self.player, self.grupoPlaneta, False, pygame.sprite.collide_circle)
                if choque: 
                    self.mensaje1()
            
            elif self.player.estado == self.player.Estado.aterrizando and self.puntos > 100:
                self.all_sprites.add(self.planeta)   
                self.player.aterrizaje()
                self.vidasActuales = self.vidas

                choque = pygame.sprite.spritecollide(self.player, self.grupoPlaneta, False, pygame.sprite.collide_circle)
                if choque: 
                    self.mensaje2()
                    teclas_pulsadas = pygame.key.get_pressed()
                    
                    if teclas_pulsadas[pygame.K_SPACE]:
                        running = False
            else: 
                pass   
            
            #sumar puntos
            if seconds % 70 == 0 and self.player.teclasPulsadas:
                self.puntos += 5

            #cambio de estados
            
            if self.puntos == 35:
                self.player.estado = self.player.Estado.preAterrizando
            
            if self.puntos == 50:
                self.player.estado = self.player.Estado.aterrizando
                
            if self.puntos == 105:
                self.player.estado = self.player.Estado.preAterrizando
            
            if self.puntos == 115:
                self.player.estado = self.player.Estado.aterrizando
                
                
            #actualizar
            self.all_sprites.update()
            
            #dibujar/renderizar la pantalla
            self.screen.fill(BLACK)
            self.screen.blit(self.fondo, self.fondo_rect)
            self.all_sprites.draw(self.screen)
            #flip el display después de dibujar
            pygame.display.flip()

class Portada():
    def __init__(self, screen):
        
        self.screen = screen
        self.fondo = pygame.image.load(path.join(img_dir, "background.png")).convert()     
        self.fondo_rect = self.fondo.get_rect()  
        self.instrucciones = Marcador(WIDTH // 2, HEIGHT // 2, "center", 90, (255, 255, 255))
        self.instrucciones.contador = "The Quest"
        self.instrucciones1 = Marcador(WIDTH // 2, 300, "center", 20, (255, 255, 255))
        self.instrucciones1.contador = "Pulsa espacio para empezar"
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.instrucciones)
        self.all_sprites.add(self.instrucciones1)
        self.reloj = pygame.time.Clock()

    def reset(self):
            pass

    def bucle_principal(self):
        game_over = False
        while not game_over:
            dt = self.reloj.tick(FPS)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT or \
                    evento.type == pygame.KEYDOWN and evento.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

            teclas_pulsadas = pygame.key.get_pressed()
            if teclas_pulsadas[pygame.K_SPACE]:
                pygame.time.delay(500)
                game_over = True

            self.all_sprites.update()
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.fondo, self.fondo_rect)
            self.all_sprites.draw(self.screen)

            pygame.display.flip()

class Portada2():
    def __init__(self, screen):
        
        self.screen = screen
        self.fondo = pygame.image.load(path.join(img_dir, "background.png")).convert()     
        self.fondo_rect = self.fondo.get_rect()  
        self.instrucciones = Marcador(WIDTH // 2, 75, "center", 30, (255, 255, 255))
        self.instrucciones.contador = "La vida humana está en peligro!"
        self.instrucciones2 = Marcador(WIDTH // 2, 125, "center", 30, (255, 255, 255))
        self.instrucciones2.contador = "El calentamiento global ha hecho de la tierra un lugar inhabitable!"
        self.instrucciones3 = Marcador(WIDTH // 2, 175, "center", 30, (255, 255, 255))
        self.instrucciones3.contador = "Salva a la humanidad colonizando otros mundos!"
        self.instrucciones4 = Marcador(WIDTH // 2, 225, "center", 30, (255, 255, 255))
        self.instrucciones4.contador = "Pulsa espacio para jugar"
        self.instrucciones5 = Marcador(WIDTH // 2, 300, "center", 20, (255, 255, 255))
        self.instrucciones5.contador = "Muevete arriba y abajo utilizando las flechas del teclado para esquivar los asteroides"
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.instrucciones)
        self.all_sprites.add(self.instrucciones2)
        self.all_sprites.add(self.instrucciones3)
        self.all_sprites.add(self.instrucciones4)
        self.all_sprites.add(self.instrucciones5)
        self.reloj = pygame.time.Clock()

    def reset(self):
            pass

    def bucle_principal(self):
        game_over = False
        while not game_over:
            dt = self.reloj.tick(FPS)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT or \
                    evento.type == pygame.KEYDOWN and evento.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

            

            teclas_pulsadas = pygame.key.get_pressed()
            if teclas_pulsadas[pygame.K_SPACE]:
                
                game_over = True

            self.all_sprites.update()
           
            self.screen.blit(self.fondo, self.fondo_rect)
            self.all_sprites.draw(self.screen)

            pygame.display.flip()

class Ranking():
    
    def __init__(self, screen):
        
        self.screen = screen
        self.fondo = pygame.image.load(path.join(img_dir, "background.png")).convert()     
        self.fondo_rect = self.fondo.get_rect()  
        self.instrucciones = Marcador(WIDTH // 2, 50, "center", 50, (255, 255, 255))
        self.instrucciones.contador = "Ranking"
        self.instrucciones = Marcador(WIDTH // 2, 350, "center", 40, (255, 255, 255))
        self.instrucciones.contador = "Pulsa cualquier tecla para salir de la pantalla de rankings"
        
        
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.instrucciones)
        self.font = pygame.font.Font(None, 32)
        self.user_text = ''
        self.reloj = pygame.time.Clock()
        input_rect = pygame.Rect(200,200,140,32)

    def reset(self):
        pass
    
    def readDataBase(self):
        conexion = sqlite3.connect(db_path)
        cur = conexion.cursor()

        cur.execute("SELECT name, score FROM 'scores' ORDER BY score DESC LIMIT 3 ;")

        claves=(cur.description)
        filas = cur.fetchall()
        self.datos_tabla = []

        for fila in filas: 
            d = {}
            for tclave, valor in zip(claves, fila):
                d[tclave[0]] = valor
            self.datos_tabla.append(d)
        
        self.filaRanking0 = Marcador(WIDTH // 2, 150, "center", 40, (255, 255, 255))
        self.filaRanking0.contador = "Name : {} || Score: {}".format(self.datos_tabla[0]['name'], self.datos_tabla[0]['score'])
        self.filaRanking1 = Marcador(WIDTH // 2, 200, "center", 40, (255, 255, 255))
        self.filaRanking1.contador = "Name : {} || Score: {}".format(self.datos_tabla[1]['name'], self.datos_tabla[1]['score'])
        self.filaRanking2 = Marcador(WIDTH // 2, 250, "center", 40, (255, 255, 255))
        self.filaRanking2.contador = "Name : {} || Score: {}".format(self.datos_tabla[2]['name'], self.datos_tabla[2]['score'])
    


    def insertDatabase(self, name, score):
        conexion = sqlite3.connect(db_path)
        cur = conexion.cursor()
        query = "INSERT INTO 'scores' (name, score) VALUES( ?, ?)"
        
        cur.execute(query, [name, score])
        
        conexion.commit()
        conexion.close()
        return redirect("/")


    def bucle_principal(self):
        game_over = False
        while not game_over:
            dt = self.reloj.tick(FPS)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT :
                        pygame.quit()
                        sys.exit()
                
                if evento.type == pygame.KEYDOWN:                
                    
                    game_over = True
                else:
                    pass                

                try:
                    self.readDataBase()
                    self.all_sprites.add(self.filaRanking0)
                    self.all_sprites.add(self.filaRanking1)
                    self.all_sprites.add(self.filaRanking2)

                except:
                    print("Ha habido un error al conectar con la base de datos")

            self.all_sprites.update()
           
            self.screen.blit(self.fondo, self.fondo_rect)
            self.all_sprites.draw(self.screen)

            pygame.display.flip()

class Ranking1():
    
    def __init__(self, screen):
        
        self.screen = screen
        self.fondo = pygame.image.load(path.join(img_dir, "background.png")).convert()     
        self.fondo_rect = self.fondo.get_rect()  
        self.instrucciones = Marcador(WIDTH // 2, 50, "center", 50, (255, 255, 255))
        self.instrucciones.contador = "Ranking"
        self.instrucciones1 = Marcador(WIDTH // 2, 100, "center", 30, (255, 255, 255))
        self.instrucciones1.contador = "Escribe tus iniciales"
        self.instrucciones2 = Marcador(WIDTH // 2, 300, "center", 30, (255, 255, 255))
        self.instrucciones2.contador = "Pulsa enter para enviar tu puntuacion al ranking"
        
        
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.instrucciones)
        self.all_sprites.add(self.instrucciones1)
        self.all_sprites.add(self.instrucciones2)
        self.font = pygame.font.Font(None, 32)
        self.user_text = ''
        self.reloj = pygame.time.Clock()
        self.input_rect = pygame.Rect(340,200,140,32)

    def reset(self):
        pass
      
    def insertDatabase(self, name, score):
        conexion = sqlite3.connect(db_path)
        cur = conexion.cursor()
        query = "INSERT INTO 'scores' (name, score) VALUES( ?, ?)"
        
        cur.execute(query, [name, score])
        
        conexion.commit()
        conexion.close()
        
    def bucle_principal(self):
        game_over = False
        while not game_over:
            dt = self.reloj.tick(FPS)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()            
                        
                if evento.type == pygame.KEYDOWN:
                    if evento.type == pygame.KEYDOWN and len(self.user_text) > 2:
                        if evento.key == pygame.K_BACKSPACE:
                            self.user_text = self.user_text[:-1]
                        else: 
                            pass
                    elif evento.key == pygame.K_BACKSPACE:
                        self.user_text = self.user_text[:-1]
                    else:
                        self.user_text += evento.unicode
                    
                    if evento.key == pygame.K_RETURN:
                        try:
                            self.insertDatabase( self.user_text, globalPuntos)
                            game_over = True
                        except:
                            print("Se ha producido un error en la conexion a la base de datos.")
                            print("Inténtalo en otro momento.")
                            game_over = True
                        

                


            self.all_sprites.update()
           
            self.screen.blit(self.fondo, self.fondo_rect)
            self.all_sprites.draw(self.screen)
            pygame.draw.rect(self.screen, WHITE, self.input_rect, 2)
            text_surface = self.font.render(self.user_text, False, (255,255,255))
            self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
            pygame.display.flip()


            