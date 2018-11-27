import pygame
import math

pygame.init()
pygame.mixer.init()

WHITE = (232, 235, 239)
BLACK = (125, 135, 150)
HEIGHT = 1444
WIDTH = 1444

display = pygame.display.set_mode((HEIGHT, WIDTH))


class tile:
    def __init__(self, colour, x_pos, y_pos):
        self.full = False
        self.piece = None
        self.colour = colour
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = pygame.Rect(self.x_pos, self.y_pos, WIDTH/8, HEIGHT/8)
        
    def draw_tile(self):
        pygame.draw.rect(display, self.colour, self.rect) # (x,y,xsize,ysize)
    

class pawn(pygame.sprite.Sprite):
    def __init__(self, tile):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('pawn1.png').convert()
        #self.image = pygame.transform.scale(self.image, (100,125))
        self.image.set_colorkey([255,255,255])
        self.rect = self.image.get_rect()
        self.tile = tile
        self.first_move = 0
        
    def set_position(self):
        (self.rect.left, self.rect.top) = (self.tile.x_pos, self.tile.y_pos)
        self.tile.full = True
        self.tile.piece = 'pawn' 
        
    def updatep(self, new_tile):
        self.rect.x = new_tile.x_pos
        self.rect.y = new_tile.y_pos
        self.tile.full = False
        self.tile.piece = None
        self.tile = new_tile
        self.tile.full = True
        self.tile.piece = 'pawn'
        
    def movement(self): #not done
        if self.first_move == 0:
            x, y = self.tile.x_pos - WIDTH/4, self.tile.y_pos
            self.first_move = 1
            return(x, y)
        else:
            x, y = self.tile.x_pos - WIDTH/8, self.tile.y_pos
            return(x, y)
        
class board:
    def __init__(self):
        self.dc = {}
        self.label = [['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8'],
                      ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8'],
                      ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8'],
                      ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8'],
                      ['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8'],
                      ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8'],
                      ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8'],
                      ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8']]
        self.make_board()
    
    def make_board(self):
        counter = 1
        initalx=0
        initaly=0
        for x in self.label:
            for term in x:
                if counter%2 != 0:
                    self.dc[term] = tile(WHITE, initalx, initaly)
                    initalx+=WIDTH/8
                    counter += 1
                else:
                    self.dc[term] = tile(BLACK, initalx, initaly)
                    initalx+=WIDTH/8
                    counter += 1
            
            initaly+=HEIGHT/8
            initalx=0
            counter = counter -1

    def draw_board(self):
        for _, tile in self.dc.items():
            tile.draw_tile()
                
def wait_button():
    pygame.event.clear()
    while True:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                return(True)
            
def find_tile(board, mouse_pos):
    for key, tile in board.dc.items():
        if mouse_pos[1] > tile.y_pos and mouse_pos[1] < (tile.y_pos + HEIGHT/8):
            if mouse_pos[0] > tile.x_pos and mouse_pos[0] < (tile.x_pos + WIDTH/8):
                return(True, key, tile)
    return(False, None, None)

            
fps = 30
clock = pygame.time.Clock()
board = board() # initialize board
all_sprites = pygame.sprite.Group()
p1 = pawn(board.dc["G1"])
all_sprites.add(p1)
running = True
p1.set_position()
while running:
    clock.tick(fps)
    board.draw_board()
    all_sprites.update()
    all_sprites.draw(display)
    pygame.display.update() 
    pygame.display.flip()
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
            if event.type == pygame.MOUSEBUTTONDOWN: # click on piece
                mouse_pos = pygame.mouse.get_pos() # get piece location
                found, key, tile = find_tile(board, mouse_pos)  # find corresponding tile
                if found:
                    if tile.full == True: # is something on the tile
                        if tile.piece == 'pawn': # is it a pawn
                            wait_button()   # wait for input for new location
                            new_mouse_pos = pygame.mouse.get_pos()  # get location
                            found, new_key, new_tile = find_tile(board, new_mouse_pos)  # does the tile exist
                            if found:
                                #allowed_x, allowed_y = p1.movement()
                                #if new_tile.x_pos < tile.x_pos and new_tile.x_pos > allowed_x:
                                p1.updatep(board.dc[new_key])   # move to new tile
                    else:
                        print('empty')
                            
                
                
    
pygame.quit()
#p1 = pawn(dc['G1'], 'G1')




#while True:
    ##move = input('move where: ')
    ##p1.move(dc[move])
    
    
    #for event in pygame.event.get():
        ##if event.type == pygame.QUIT:
           ##pygame.quit()
           ##quit()
        #if event.type == pygame.MOUSEBUTTONDOWN:
            #pos = pygame.mouse.get_pos()
            #m1, m2 = p1.move_limit()
            #if pos[1] > dc[m1].y_pos and pos[1] < (dc[m1].y_pos + HEIGHT/8):
                #if pos[0] > dc[m1].x_pos and pos[0] < (dc[m1].x_pos + WIDTH/8):
                    #p1.move(dc[m1],m1)
                    #pygame.display.flip()
                    #pygame.display.update()                    
            #elif pos[1] > dc[m2].y_pos and pos[1] < (dc[m2].y_pos + HEIGHT/8):
                #if pos[0] > dc[m2].x_pos and pos[0] < (dc[m2].x_pos + WIDTH/8):
                    #p1.move(dc[m2],m2)
                    #pygame.display.flip()
                    #pygame.display.update()
            
                


