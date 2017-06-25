import pygame
import cv2
import numpy as np
import os;
from pygame.locals import *
import random
import sys

from menu import *
pygame.init()
camera = cv2.VideoCapture(0)
pygame.display.set_caption("OpenCV camera stream on Pygame")
camera.set(3,144)
camera.set(4,144)

CURR_PATH = os.path.dirname(os.path.realpath(__file__));
OUTPUT_DIRECTORY = str(CURR_PATH) + "\\Input";

#costanti globali

# V. Colori
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLUE_PLATFORM1 = (51, 153, 255)
BLUE_PLATFORM2 = (12, 50, 100)
BACKGROUND = (231, 229, 205)
PUNTO = (255,102,51)
YELLOW = (255,128,0)
PLATFORM_GREY = (105,104,104)
COIN_COLOR = (251,135,5)
RED_HEARTH =(219,32,39)

# Dimensione Schermo
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 576

global P_R, P_B, P_G, PLAYER_COLOR

P_R = 0
P_G = 204
P_B = 0

PLAYER_COLOR = (P_R,P_G,P_B)

full = (SCREEN_WIDTH,SCREEN_HEIGHT)

global DIFFICULTY

DIFFICULTY = 1.0;




class Player(pygame.sprite.Sprite):

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)

        self.MORTAL = True

        self.image = pygame.image.load('assets/sprites/player.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (20, 20))

        # Riferimento rect
        self.rect = self.image.get_rect()
        
        # Vel. player
        self.change_x = 0
        self.change_y = 0

        # Lista variabili
        self.level = None
        
        self.attempt = 1
        self.total_points = 0

        ## Changed -- tagged --
        self.life = 99999
        self.mixer = pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=4096)
        self.pick_coin = pygame.mixer.Sound('assets/audio/point.ogg')

    def update(self):
        #Aggiorno le variabili e muovo il player
        if self.life < 1:
            game_over()


        # Severity
        self.calc_grav()

        # Muovo a sinistra e a destra
        self.rect.x += self.change_x

        #---------------pick coin--------------------------------------------
        coin_hit = pygame.sprite.spritecollide(self,self.level.coin_list,True)
        for block in coin_hit:
            self.total_points  +=1
            self.pick_coin.play(maxtime =850,fade_ms = 0)
        #----------------------coin--------------------------------------------


        # spritecollide platform, se muovo a destra collido, cambio direzione
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list,False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left

                #se collido in X con gli obstacles game over
        #-----------------------GAME OVER---------------------#

                if (self.MORTAL):
                    ## CHANGED -- tagged --
                    if self.level.obstacles_list.has(block):
                        #vado a y 550 e riavvio
                        self.attempt +=1
                        self.life -= 1
                        self.life += 1
                        self.rect.x = -5
                        self.rect.y = 550
                            
        #-----------------------GAME OVER---------------------#

        #Muovo su e giu
        self.rect.y += self.change_y


        # spritecollide su e giu
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            # Resetto la posizione dell'oggetto sopra e sotto
            if self.change_y > 0:
                self.rect.bottom = block.rect.top

                if (self.MORTAL):
                    ## CHANGED -- tagged --
                    #If I collide in y with the obstacles game over
                    if self.level.obstacles_list.has(block):
                        #I go to y 510 and restart
                        self.attempt +=1
                        self.life -= 1
                        self.life += 1
                        self.rect.x = -5
                        self.rect.y = 550

            if self.change_y < 0:
                self.rect.bottom = block.rect.top
                    
            # Movimento Veritcale a 0
            self.change_y = 0
        #-------------------------------------------------------------SE SCONTRO CON I BLOCCHI points--------------------------
    
     

    def calc_grav(self):
        #def gravità

        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .55
            

        # Pav
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        # Definition jumping
        
        self.rect.y += 3      
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 3


        for platform in platform_hit_list:
            if self.change_y < 0:
                self.rect.bottom = platform.rect.top
                print("top it")
        
    ## -- tagged --
       
        # If I jump and collide with the platform shut down the player
        if self.rect.bottom >= SCREEN_HEIGHT or (len(platform_hit_list) > 0):
            self.change_y = -9
            

    # Movimento left, right , stop
    def go_left(self):
        self.change_x = -5
       

    def go_right(self):
        global DIFFICULTY
        self.change_x = 5  #* DIFFICULTY
        
    def stop(self):
        self.change_x = 0
        


#class Proiettili(pygame.sprite.Sprite):
#    def __init__(self):
#        pygame.sprite.Sprite.__init__(self)

#        self.image = pygame.Surface([10,4])
#        self.image.fill(BLACK)
#        self.rect = self.image.get_rect()

#    def update(self):       
#        self.rect.x += 10
        

class Platform(pygame.sprite.Sprite):
    
    def __init__(self, width, height):

        # -- tagged --

        global DIFFICULTY
        
        self.width = width
        self.height = height

        width = min((int)(width * DIFFICULTY), 10000)
        
        pygame.sprite.Sprite.__init__(self)
        
        
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()


class obstacles_1(Platform):

    def __init__(self, width, height):

    # -- tagged --
##        global DIFFICULTY
##
##        width = (int)(width * DIFFICULTY)

        self.width = width
        self.height = height
        
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('assets/sprites/ostacolo_1.png').convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (width, height))
        self.rect = self.image.get_rect()


class obstacles_2(Platform):

    def __init__(self, width, height):

        # -- tagged --

##        global DIFFICULTY
##
##        width = (int)(width * DIFFICULTY)

        self.width = width
        self.height = height

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('assets/sprites/ostacolo_2.png').convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (width, height))
        self.rect = self.image.get_rect()

class obstacles_3(Platform):

    def __init__(self, width, height):

        # -- tagged --

##        global DIFFICULTY
##
##        width = (int)(width * DIFFICULTY)

        self.width = width
        self.height = height

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('assets/sprites/ostacolo_3.png').convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (width, height))
        self.rect = self.image.get_rect()    

class points_1(Platform):
 
    
    def __init__(self,x,y):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('assets/sprites/gemma1.png')         
        self.image = pygame.transform.smoothscale(self.image, (31, 28))   
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

    def update(self):
        pass

class points_2(Platform):   
    def __init__(self,x,y):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('assets/sprites/gemma2.png')         
        self.image = pygame.transform.smoothscale(self.image, (31, 28))   
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

    def update(self):
        pass 

class points_3(Platform):   
    def __init__(self,x,y):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('assets/sprites/gemma3.png')         
        self.image = pygame.transform.smoothscale(self.image, (31, 28))   
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

    def update(self):
        pass        

class Level(object):
    #Super class che controlla i livelli

    def __init__(self, player):
        #al costruttore passo come paramentro il player e le relative variabili

        self.platform_list = pygame.sprite.Group()
        self.proiettili_lista = pygame.sprite.Group()
        self.player = player
        self.coin_list = pygame.sprite.Group()
        self.obstacles_list = pygame.sprite.Group()

        # Background   
        self.background = None
        self.world_shift = 0
        self.level_limit = -1000

        
        
        #POSIZIONE PLAYER--------------------------
        self.player.rect.x = 50
        self.player.rect.y =  400 - self.player.rect.height
        

    # Update livelli
    def update(self):
        self.platform_list.update()

    def draw(self, screen):
        #Disegno su schermo 

        # background
        screen.fill(BACKGROUND)
        screen.blit(self.background,(self.world_shift // 3,0))
        
        # Tutti gli sprite delle liste plat e coin
        self.platform_list.draw(screen)
        self.coin_list.draw(screen)


    def shift_world(self,shift_x):
        self.world_shift += shift_x

        #per tutti gli sprite nella lista sposto
        for platform in self.platform_list:
            platform.rect.x += shift_x

        #per tutti gli sprite nella lista sposto
        for coin in self.coin_list:
            coin.rect.x += shift_x

# Classi figlie di "level" 
class Level_01(Level):

    def __init__(self, player):

        # Richiamo il costruttore
        Level.__init__(self, player)
        self.level_limit = -3000
        #CARICO LO SFONDO
        self.background = pygame.image.load('assets/sprites/background_lvl_1_invert.png').convert()

        # Array that passes class parameters width, height, x and y
        level = [[10, 600, -100, 0], #lato sinistro  
                [2400, 1, 0, 400],#1
                [300, 1, 500, 350],
                [31, 2, 1500, 360],
                [31, 2, 1650, 330],
                [31, 2, 1850, 330],
                [31, 2, 2040, 330],

                ## -- tagged -- 
                #[10000, 1, 0, 350],


                [31, 2, 2210, 330],

                #MOD. LVL 1
                [31, 2, 2350, 290],
                [31, 2, 2500, 250],
                [31, 2, 2650, 210],

                [30, 2, 2750, 250],
                [100, 2, 2790, 170],
                [100, 2, 2820, 310],

                [50, 2, 3000, 290],
                [30, 2, 3170, 250],
                [40, 2, 3330, 250],

                [1000, 1, 3480, 250]
                 ]


        obstacles = [[30, 30 , 450, 370],                   
                    [30, 30, 550, 370],
                    [30, 30, 650, 320],#sopra
                    [30, 30, 750,370],                   
                    [30, 30, 850, 370],
                    [30, 30, 1450, 370],
                    [30, 30, 1550, 370],
                    [30, 30, 1650, 370],
                    [30, 30, 1750, 370],
                    [30, 30, 1850, 370],
                    [30, 30, 1950, 370],
                    [30, 30, 2050, 370],
                    [30, 30, 2200, 370],
                    [30, 30, 2350, 370],

                    [30, 30, 1750, 300],
                    [30, 30, 1960, 300],
                    [30, 30, 2140, 300],
                    
                    
                    #MOD. LVL 1 obstacles
                    
                    [30, 30, 2355, 300],
                    [30, 30, 2505, 270],
                    [30, 30, 2655, 240],  
                    [30, 30, 2890, 280]
                              
                    ]



        coins = [[30,30,300,320],
                 [30,30, 650, 250],
                 [30,30, 1000, 360],
                 [30,30, 1100, 320],
                 [30, 30, 1200, 360],
                 [30, 30, 1300, 360],

                 [30, 30, 1750, 240],
                 [30, 30, 1960, 240],
                 [30, 30, 2140, 240],
                 [30, 30, 2600, 150],
                 [30, 30, 2810, 110],
                 [30, 30, 3250, 170],
                 [30, 30, 3410, 170]
                 ]

         # ciclo for che grabba i dati dall'array
        for coin in coins:
            block = points_1(coin[0], coin[1])
            block.rect.x = coin[2]
            block.rect.y = coin[3]
            block.player = self.player
            self.coin_list.add(block)
            

        # ciclo for che grabba i dati dall'array
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

         # ciclo for che grabba i dati dall'array
        for ost in obstacles:
            #obstacles---------------
            block = obstacles_1(ost[0],ost[1])
            block.rect.x = ost[2]
            block.rect.y = ost[3]
            block.player = self.player
            self.platform_list.add(block)
            self.obstacles_list.add(block)


class Level_02(Level):
    def __init__(self, player):

        Level.__init__(self, player)
        #CARICO LO SFONDO
        self.background = pygame.image.load('assets/sprites/background_lvl_2.png').convert()

        #psozione player
        self.player.rect.x = 80
        self.player.rect.y = 300
        self.level_limit = -3000


        # Array che passa i parametri della classe width, height, x e y
        level = [[10000, 0, -200, 550],#sotto
                 [10, 600, -100, 0], #lato sinistro


                ## -- tagged -- 
                #[10000, 1, 0, 350],
                 

        #PIATTAFORME
                 [400, 1.5, 50, 420],#1                 
                 [110, 1.5, 520, 350],#2
                 [110, 1.5, 650, 280],
                 [350, 1.5, 790, 210],

                 #scalinata scesa
                 
     
                 [30, 30, 1200, 250],
                 [30, 30, 1310, 300],
                 [30, 30, 1420, 350],
                 [30, 30, 1530, 400],
                 [30, 30, 1640, 450],
                 [30, 30, 1850, 500],

                 #scalinata salita
                
                 [70, 2, 1940, 450],
                 [70, 2, 2090, 400],
                 [400, 2, 2250, 350],

                 # paltform vari
                 [60, 2, 2700, 300],
                 [60, 2, 2800, 370],
                 [60, 2, 3000, 370],
                 [60, 2, 3200, 370],
                 [1000, 2, 3350, 300]]  


        obstacles = [[30,30, 850,180],
                    [30,30, 1050,180],
                    [30,30, 2350,320],
                    [30,30, 2500, 320],                  
                    [30,30, 3400, 270]
                    ]

        coins = [[30,30,300,350],

                 [30,30, 900, 120],
                 [30, 30, 1200, 210],
                 [30, 30, 1530, 300],
                 [30, 30, 1740, 380],
                 [30, 30, 2250, 320],
                 [30, 30, 2415, 280],
                 [30, 30, 2600, 320],

                 [30, 30, 2915, 270],
                 [30, 30, 3115, 270],
                 [30, 30, 3350, 260]
                 
                 ]


         # ciclo for che grabba i dati dall'array
        for coin in coins:
            block = points_2(coin[0], coin[1])
            block.rect.x = coin[2]
            block.rect.y = coin[3]
            block.player = self.player
            self.coin_list.add(block) 
             
             
        #For che grabba i dati dall'array
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)


         # ciclo for che grabba i dati dall'array
        for ost in obstacles:
            #obstacles---------------
            block = obstacles_2(ost[0],ost[1])
            block.rect.x = ost[2]
            block.rect.y = ost[3]
            block.player = self.player
            self.platform_list.add(block)
            self.obstacles_list.add(block)



class Level_03(Level):
    def __init__(self, player):

        Level.__init__(self, player)
        self.level_limit = -3000
        self.background = pygame.image.load('assets/sprites/background_lvl_3.png').convert()
        

         # Array che passa i parametri della classe width, height, x e y
        level = [[10000, 0, -100, 550],#sotto
                 [10, 600, -100, 0], #lato sinistro  

        #PIATTAFORME
                 [320,1, -10, 420],#1                 
                 [50, 1, 450, 400],#2
                 [50, 1, 650, 400],
                 [50, 1, 850, 400],

                 [50, 20, 950, 460],
                 [50, 1, 1080, 400],
                 [50, 20, 1180, 460],
                 [50, 1, 1310, 400],
                 [50, 20, 1450, 350],

                 [30, 30, 1550, 410],
                 [30, 30, 1650, 460],
                 [140, 1, 1730, 500],

                 #scalinata salita
                
                 [50, 20, 1940, 460],
                 [50, 20, 2090, 410],
                 [400, 1, 2250, 360],

                 # paltform vari
                 [50, 1, 2700, 310],
                 [50, 1, 2800, 380],
                 [50, 20, 2910, 440],

                 [50, 1, 3020, 380],
                 [50, 20, 3110, 440],

                 [50, 1, 3240, 370],
                 [500, 1, 3370, 340]]  


        obstacles = [[30,30, 560,370],
                    [30,30, 760,370],
                    [30,30, 960,360],
                    [30,30, 1210, 340],

                    [20,20, 1740, 420],  
                    [20,20, 1770, 420],
                    [20,20, 1800, 420],
                    [20,20, 1830, 420],

                    [30,30, 2300, 330],
                    [30,30, 2600, 330],
                    [30,30, 2920, 350],
                    [30,30, 3130, 340],           
                    [30,30, 3480, 310]
                    ]

        coins =     [[30,30, 560,320],
                    [30,30, 760,320],
                    [30,30, 960,420],
                    [30,30, 1190, 420],

                    [30,30, 1550, 370],

                    [20,20, 1750, 470], 
                    [20,20, 1820, 470],

                    [30,30, 2400, 330],
                    [30,30, 2500, 330],

                    [30,30, 2920, 410],
                    [30,30, 3130, 410],           
                    [30,30, 3420, 310]
                    ]



         # ciclo for che grabba i dati dall'array
        for coin in coins:
            block = points_3(coin[0], coin[1])
            block.rect.x = coin[2]
            block.rect.y = coin[3]
            block.player = self.player
            self.coin_list.add(block) 


         # ciclo for che grabba i dati dall'array
        for ost in obstacles:
            #obstacles---------------
            block = obstacles_3(ost[0],ost[1])
            block.rect.x = ost[2]
            block.rect.y = ost[3]
            block.player = self.player
            self.platform_list.add(block)
            self.obstacles_list.add(block)

        # Grabbo i dati dall'array
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)



def game_over():
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode((size),pygame.DOUBLEBUF | pygame.HWSURFACE )
    pygame.display.set_caption("Endless - Block")

    background_menu = pygame.image.load('assets/sprites/Game_over.png').convert()
    screen.blit(background_menu,(0,0))

    player = Player()
    font3 = pygame.font.Font('KGPrimaryWhimsy.ttf',30)                        
    text = font3.render("  Lifes Used "+str(player.life), True, WHITE)
    screen.blit(text, [420, 415])


    pygame.display.flip()


    menu = cMenu(20, 00, 100, 20, 'horizontal', 100, screen,
                [('MENU', 1, None),
                ('EXIT',2, None)])

    menu.set_center(True, True)
    
    menu.set_alignment('center', 'center')
    state = 0
    prev_state = 1
    rect_list = []

    while 1:
  
        if prev_state != state:
            pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
            prev_state = state
         
        e = pygame.event.wait()

        if e.type == pygame.KEYDOWN or e.type == EVENT_CHANGE_STATE:
            if state == 0:
                rect_list, state = menu.update(e, state)
            elif state == 1:
                main()

                state = 0
            else:
                print ('Exit!')
                pygame.quit()
                sys.exit()


            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            pygame.display.update(rect_list)



def main():
    
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode((size),pygame.DOUBLEBUF | pygame.HWSURFACE )
    pygame.display.set_caption("Endless - Block")

    background_menu = pygame.image.load('assets/sprites/Intro_BG_desktop.png').convert()
    screen.blit(background_menu,(0,0))
    pygame.display.flip()

    tick_speed = 1

    menu = cMenu(20, 00, 100, 28, 'vertical', 100, screen,
               [('PLAY', 1, None),
                ('How To Play',2, None),
                ('QUIT',3, None),])

    menu.set_center(True, True)
    
    menu.set_alignment('center', 'center')
    state = 0
    prev_state = 1
    rect_list = []
    
    
    BG_1 = pygame.image.load('assets/sprites/background_lvl_1.png').convert()
    BG_1i = pygame.image.load('assets/sprites/background_lvl_1_invert.png').convert()


    while 1:

      if prev_state != state:
         pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
         prev_state = state
         
      e = pygame.event.wait()

      if e.type == pygame.KEYDOWN or e.type == EVENT_CHANGE_STATE:
         if state == 0:
            rect_list, state = menu.update(e, state)
         elif state == 1:
      
             #-----------------------------------------------------------------------LOOP GAME------------------------------------------------------

             size = [SCREEN_WIDTH, SCREEN_HEIGHT]
             screen = pygame.display.set_mode((size),pygame.DOUBLEBUF | pygame.HWSURFACE )
 
             pygame.display.set_caption("Endless - Block")
             attempt = 1

             joysticks = []
              
            # Creo il player
             player = Player()

             #Carico le font
             font1 = pygame.font.Font('KGPrimaryWhimsy.ttf', 30)
             font2 = pygame.font.Font('KGPrimaryWhimsy.ttf', 40)
             

            #Creo i livelli
             level_list = []
             level_list.append( Level_01(player) )
             level_list.append( Level_02(player) )
             level_list.append( Level_03(player) )

           #Setto il livello corrente
             current_level_no = 0
             current_level = level_list[current_level_no]
             active_sprite_list = pygame.sprite.Group()
             player.level = current_level
             active_sprite_list.add(player)

             

                #-------------------------------------------JOYPAD-----------------------------
             joystick_count = pygame.joystick.get_count()
             print ("Ho trovato", joystick_count, "joystick/s")
             if joystick_count == 0:
                 print ("Error, I did not find anything")
             else:
                 my_joystick = pygame.joystick.Joystick(0)
                 my_joystick.init()
   
            #-------------------------------------------JOYPAD-----------------------------
             global OUTPUT_DIRECTORY
             clock = pygame.time.Clock()
             #cam_clock = pygame.time.Clock()
             
             
             done = False
             time_elapsed = 0
             
             ret, frame = camera.read()
                   
             #screen.fill([0,0,0])
             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
             frame = np.rot90(frame)
             frame = pygame.surfarray.make_surface(frame)
             
             
             while not done:
             
                 global P_R, P_B, P_G, PLAYER_COLOR

                 PLAYER_COLOR = (P_R,P_G,P_B)
                 player.image.fill(PLAYER_COLOR)
             
             
                 if (P_R < 100):
                  P_R += 1
                 elif (P_G < 100):
                  P_G += 1
                 elif (P_B < 100):
                  P_B += 1
                 else:
                  P_R -= 1
                  P_G -= 1
                  P_B -= 1 
                  
                 global OUTPUT_DIRECTORY
                 # Capture frame-by-frame
                 dt = clock.tick()
                 
                 time_elapsed += dt
                 if time_elapsed > 30:
                   time_elapsed = 0
                   ret, frame = camera.read()
                   cv2.imwrite(OUTPUT_DIRECTORY + "\\face.jpg", frame)
                   frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                   frame = np.rot90(frame)
                   frame = pygame.surfarray.make_surface(frame)
                   #screen.blit(frame, (SCREEN_WIDTH - 144,SCREEN_HEIGHT - 144))
                   pygame.display.update()

                    # Our operations on the frame come here
                    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                    # Display the resulting frame
                   #cv2.imshow('frame', frame)    cv2.imwrite(output_directory + "\\face_" + str(i) + ".jpg", all_faces[i]);

                   if cv2.waitKey(1) & 0xFF == ord('q'):
                       break
                 for event in pygame.event.get():
                   if event.type == pygame.QUIT:
                       done = True                 

          #--------------------------------------------------JOYPAD---------------------------

                   elif event.type == pygame.JOYBUTTONDOWN:
                       nome = 'joystick%d-pulsante%d-giu' % (event.joy, event.button)
                       print (nome)

                       if event.button == 0:
                           player.jump()
                       if event.button == 7:
                           player.stop()

                   elif event.type == pygame.JOYBUTTONUP:
                           nome = 'joystick%d-pulsante%d-su' % (event.joy, event.button)
                           print(nome)
                  

                   elif event.type == pygame.JOYHATMOTION:                
                       nome = 'joystick%d-axis%d' % (event.joy, event.hat)
                       print (nome, event.value)
                       if event.hat == 0:
                           player.go_right()
                       else:
                           player.stop()

         
          #--------------------------------------------------JOYPAD---------------------------
                   elif event.type == pygame.KEYDOWN:
                       if event.key == pygame.K_0:
                           screen = pygame.display.set_mode((full),pygame.FULLSCREEN)
                       if event.key == pygame.K_1:
                           screen = pygame.display.set_mode(size)
                       if event.key == pygame.K_ESCAPE:
                           main()

                      #if event.key == pygame.K_SPACE:
                      #    proiettili = Proiettili()
                      #    proiettili.rect.x = player.rect.x 
                      #    proiettili.rect.y = player.rect.y+10 
                      #    active_sprite_list.add(proiettili)
                      #    proiettili_lista.add(proiettili)
           
          #-----------------------------------------------------KEYBOARD-----------------------         
            
                       if event.key == pygame.K_RIGHT:
                           player.go_right()                                     
                       if event.key == pygame.K_UP:
                           player.jump()

                       global DIFFICULTY

                      ## -- tagged --
                       if event.key == pygame.K_q:
                           DIFFICULTY += 0.1
                           print (DIFFICULTY)


                       if event.key == pygame.K_w:
                           DIFFICULTY -= 0.1
                           print (DIFFICULTY)
                       
                       if event.key == pygame.K_c:
                           player.level.background = BG_1 #pygame.image.load('assets/sprites/background_lvl_1.png').convert()
                           screen.blit(player.level.background,(0,0))
                           
                       if event.key == pygame.K_v:
                           player.level.background = BG_1i #pygame.image.load('assets/sprites/background_lvl_1_invert.png').convert()
                           screen.blit(player.level.background,(0,0))

                       if event.key == pygame.K_t:
##                             level_list = []
##                             level_list.append( Level_01(player) )
##                             level_list.append( Level_02(player) )
##                             level_list.append( Level_03(player) )
##                             print("Updated list")


                           set_level = -1

                           if (current_level_no == 0):
                               set_level = Level_01(player)
                           elif (current_level_no == 1):
                               set_level = Level_02(player)
                           else:
                              set_level = Level_03(player)

                           
                           player.level = current_level = level_list[current_level_no] = set_level
     
                           player.update()
                               
                           

                       if event.key == pygame.K_e:
                           player.MORTAL = False;
                           print("IMMORTAL")

                       if event.key == pygame.K_r:
                           player.MORTAL = True;
                           print("MORTAL")

                       
                       if event.key == pygame.K_y:
                           tick_speed += 1;
                           
                       if event.key == pygame.K_u:
                       #width, height, x e y
                       
                          """
                          for platform in level:
                            block = Platform(platform[0], platform[1])
                            block.rect.x = platform[2]
                            block.rect.y = platform[3]
                            block.player = self.player
                            self.platform_list.add(block)
                          """
                          #global DIFFICULTY
                            
                          local_platform_list = player.level.platform_list
                          player.level.platform_list = []
                       
                          for plat in local_platform_list:
                            local_width = (int)(max(plat.width * DIFFICULTY, 10000))
                            local_height = plat.height
                            
                            block = Platform(local_width, local_height)
                            block.rect.x = plat.rect.x
                            block.rect.y = plat.rect.y
                            block.player = player
                            player.level.platform_list.append(block)
                              
                              

                       if event.key == pygame.K_a:
                           print("q - increase DIFFICULTY")
                           print("w - decrease DIFFICULTY")
                           print("t - update levels")
                           print("e - IMMORTAL")
                           print("r - MORTAL")
                           print("y - change speed")
                                 

                   if event.type == pygame.KEYUP:
                       if event.key == pygame.K_RIGHT and player.change_x > 0:
                           player.go_right()
                       if event.key == pygame.K_s and player.change_x >0:
                           player.stop()                           
                       if event.key == pygame.K_UP and player.change_x == 0:
                           player.stop()


                      
            #-----------------------------------------------------TASTIERA-----------------------         
  
                # Update the Player
                 active_sprite_list.update()
        
                # Update Objects
                 current_level.update()

                #Se il player si trova a + 300 parallax a -x (300)
                 if player.rect.x >= 300:
                     diff = player.rect.x - 300
                     player.rect.x = 300
                     current_level.shift_world(-diff)


                # #Se il player si trova a - 300 parallax a +x (300)
                 if player.rect.x <= 0:
                     diff = level_durtion - player.rect.x
                     player.rect.x = 50
                     current_level.shift_world(diff)
 
                     #If the player reaches the end of the level and limit, load the second level, stop
                 current_position = player.rect.x + current_level.world_shift
                 if current_position < current_level.level_limit:
                     if current_level_no < len(level_list)-1:
                         player.rect.x = 120
                         current_level_no += 1
                         current_level = level_list[current_level_no]
                         player.level = current_level
                         player.stop()
                         
                         #se i livelli finiscono carica menu "END"
                     else:
                         size = [SCREEN_WIDTH, SCREEN_HEIGHT]
                         screen = pygame.display.set_mode((size),pygame.DOUBLEBUF | pygame.HWSURFACE )
                         pygame.display.set_caption("Impossible Py-Block")

                         background_menu = pygame.image.load('assets/sprites/Game_results.png').convert()
                         
                         screen.blit(background_menu,(0,0))
                         
                         font3 = pygame.font.Font('KGPrimaryWhimsy.ttf',30)
                         
                         text = font3.render("  Diamonds collected "+str(player.total_points), True, WHITE)
                         screen.blit(text, [380, 390])

                         text = font3.render("  Total ATTEMPT "+str(total_attempt), True, WHITE)
                         screen.blit(text, [380, 440])


                         pygame.display.flip()


                         menu = cMenu(20, 00, 100, 20, 'horizontal', 100, screen,
                                    [('MENU', 1, None),
                                    ('EXIT',2, None)])

                         menu.set_center(True, True)
    
                         menu.set_alignment('center', 'center')
                         state = 0
                         prev_state = 1
                         rect_list = []

                         while 1:

                             if prev_state != state:
                                 pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
                                 prev_state = state
 
                             e = pygame.event.wait()

                             if e.type == pygame.KEYDOWN or e.type == EVENT_CHANGE_STATE:
                                 if state == 0:
                                     rect_list, state = menu.update(e, state)
                                 elif state == 1:
                                     main()

                                     state = 0
                                 else:
                                     print ('Exit!')
                                     pygame.quit()
                                     sys.exit()

                                 if e.type == pygame.QUIT:
                                     pygame.quit()
                                     sys.exit()

     
                                 pygame.display.update(rect_list)

                
                 level_durtion =  -current_position + player.rect.x
        
        
        
                #-----------------------GAME OVER---------------------#
                 
                 current_pos_player = player.rect.y
                 if current_pos_player > 480:
                     player.rect.x = -level_durtion  - current_level.world_shift
                     player.rect.y = 300
                     current_level = level_list[current_level_no]
                     player.level = current_level
                     player.stop()
                     attempt +=1
                     player.life -= 1
                     

                  


                #AGGIORNO LE LISTE E DISEGNO
                 current_level.draw(screen)
                 active_sprite_list.draw(screen)
                 total_attempt =attempt
                 

        

                #OGGETTI TESTO
                #--------------------PUNTEGGIO - lvl - ATTEMPT------------------------------------------
                 text = font2.render("ATTEMPT "+str(attempt), True, WHITE)
                 screen.blit(text, [400, 80])

                 text = font1.render("Lvl "+str(current_level_no+1), True, WHITE)
                 screen.blit(text, [20, 50])


                 text = font1.render("Lvl stat: "+str(level_durtion)+"/3300", True, WHITE)
                 screen.blit(text, [800, 50])

                 text = font1.render("Gems X "+str(player.total_points ), True, COIN_COLOR)
                 screen.blit(text, [430, 50])




                 text = font2.render("x", True,WHITE)
                 screen.blit(text,[485, 125])

                 text = font2.render(str(player.life), True,WHITE)
                 screen.blit(text,[510, 130])

                 hearth = pygame.image.load('assets/sprites/hearth.png').convert_alpha()
                 hearth = pygame.transform.smoothscale(hearth, (45, 35)) 
                
                 screen.blit(hearth,(430,130))
                #--------------------PUNTEGGIO - lvl - ATTEMPT------------------------------------------
      

                 # 60 frame
                 ##global DIFFICULTY
                 ## -- tagged --

                 ##tick_speed = 60 * DIFFICULTY

                 clock.tick(tick_speed * 30 % 180 + 30)
                 #cam_clock.tick(30)
                 
                 screen.blit(frame, (SCREEN_WIDTH - 144,SCREEN_HEIGHT - 120))
                
                
                #UPDATE
                 pygame.display.flip()

            #EXIT
             pygame.quit()
         elif state == 2:
             size = [SCREEN_WIDTH, SCREEN_HEIGHT]
             screen = pygame.display.set_mode((size),pygame.DOUBLEBUF | pygame.HWSURFACE )
             pygame.display.set_caption("Impossible Py-Block")
             how = pygame.image.load('assets/sprites/How_to_play.png').convert_alpha()
             screen.blit(how,(0,0))
             pygame.display.flip()

             state = 2
             menu = cMenu(20, 00, 100, 20, 'horizontal', 100, screen,
                                    [('MENU', 1, None),
                                    ('EXIT',2, None)])

             menu.set_center(True, True)
    
             menu.set_alignment('center', 'center')
             state = 0
             prev_state = 1
             rect_list = []

             while 1:

                 if prev_state != state:
                     pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
                     prev_state = state

                 e = pygame.event.wait()

                 if e.type == pygame.KEYDOWN or e.type == EVENT_CHANGE_STATE:
                     if state == 0:
                         rect_list, state = menu.update(e, state)
                     elif state == 1:
                         main()

                         state = 0
                     else:
                         print ('Exit!')
                         pygame.quit()
                         sys.exit()

                     if e.type == pygame.QUIT:
                         pygame.quit()
                         sys.exit()

                     pygame.display.update(rect_list)
         else:
             print ('Exit!')
             pygame.quit()
             sys.exit()


      if e.type == pygame.QUIT:
          pygame.quit()
          sys.exit()

      pygame.display.update(rect_list)



if __name__ == "__main__":
    main()
   