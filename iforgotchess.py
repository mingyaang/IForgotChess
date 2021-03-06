import pygame
import math
import random
import numpy as np

pygame.init()   # Initiate the pygame module


WHITE = (232, 235, 239)  # "White" tiles for the board
BLACK = (125, 135, 150)  # "Black" tiles for the board
HEIGHT = 644    # Height of window
WIDTH = 644     # Width of window


display = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SRCALPHA)
# Declare global variables of color color and determines the game window size

import jpnPieces as JPN
import euPieces as EUP
# These import modules are not in the header since they require a display to be
# made in pygame so that they can get the display size


COORD_ID = np.array([['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8'],
                     ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8'],
                     ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8'],
                     ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8'],
                     ['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8'],
                     ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8'],
                     ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8'],
                     ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8']])
# 2D Coordinate array that shows the position of each tile of the chess board

# List of different pieces of different value to place onto the board
random_pawn = [EUP.pawn, JPN.pawn, EUP.pawn, EUP.pawn, JPN.pawn, JPN.gold,
               EUP.checker, JPN.silver]
random_exclusive = [EUP.bishop, EUP.knight, EUP.rook, JPN.knight, JPN.bishop,
                    JPN.lance, EUP.queen, JPN.gold, JPN.rook]
random_king = [EUP.king, JPN.king]


class tile:
    ''' tile class stores information such as its colour, position and whether
    the tile is empty. draw_tile draws a tile onto the display'''

    def __init__(self, colour, x_pos, y_pos):
        self.full = False   # default tile is empty (Full == False)
        self.piece = empty()
        self.colour = colour    # colour of tile
        self.x_pos = x_pos      # top of tile
        self.y_pos = y_pos      # left side of tile
        # create tile with pygame rect function
        self.rect = pygame.Rect(self.x_pos, self.y_pos, WIDTH / 8, HEIGHT / 8)

    def draw_tile(self):
        ''' draws tile onto pygame window '''
        pygame.draw.rect(display, self.colour, self.rect)  # draw the tile


class empty:

    def __init__(self):
        self.full = False
        self.player = None

    def updatep(self, new_tile):
        pass

    def move(self, a, b, c, d):
        pass


class board:
    ''' stores tiles into a board class where the tile label ('A1')
    is stored as a key to a dictionary with its subsequent tile
    class as the value of the key'''

    def __init__(self):
        self.dc = {}    # dictionary to store tiles
        self.label = [['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8'],
                      ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8'],
                      ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8'],
                      ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8'],
                      ['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8'],
                      ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8'],
                      ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8'],
                      ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8']]
        self.make_board()

    def give_dictionary(self):
        ''' returns created dictionary'''
        return self.dc

    def make_board(self):
        ''' make_board() creates a white tile for odd indexes
        and a black tile for even indexes.'''
        counter = 1  # used to determine even or odd
        initalx = 0  # intial x (left) coordinate for first tile
        initaly = 0  # intial y (top) coordinate for first tile
        for x in self.label:    # for each row
            for term in x:  # for each column in row
                if counter % 2 != 0:    # if odd create white tile
                    self.dc[term] = tile(WHITE, initalx, initaly)   # make tile
                    # increase left coordinate by width of tile
                    initalx += WIDTH / 8
                    counter += 1    # increase counter by 1
                else:   # if even create black tile
                    self.dc[term] = tile(BLACK, initalx, initaly)   # make tile
                    # increase left coordinate by width of tile
                    initalx += WIDTH / 8
                    counter += 1    # increase counter by 1

            initaly += HEIGHT / 8  # new row, move down by height of tile
            initalx = 0  # reset x postion to beginning of row
            counter = counter - 1   # alternate between black/white

    def draw_board(self):
        ''' uses draw_tile() function to draw tiles (stored in dictionayr)
        onto the board'''
        for _, tile in self.dc.items():
            tile.draw_tile()


def wait_button():
    ''' wait_button() clears past events and waits for user to press
    mouse button again. If button is pressed, wait_button() will end
    and game loop will continue '''
    pygame.event.clear()    # clear all events
    while True:
        pygame.time.delay(100)  # wait for user
        for event in pygame.event.get():
            # if mouse button is pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                return(True)    # return true


def find_tile(board, mouse_pos, tile_flag):
    ''' find tile will find the corresponding tile to mouse_pos, if it's the
    first iteration, the tile_flag will be on so that if an empty space is
    clicked, it will stop the loop and allow player to try again '''
    for key, tile in board.dc.items():  # iterate through tiles
        # if y position corresponds to a tile
        if mouse_pos[1] > tile.y_pos and mouse_pos[
                1] < (tile.y_pos + HEIGHT / 8):
            # if x position corresponds to a tile
            if mouse_pos[0] > tile.x_pos and mouse_pos[
                    0] < (tile.x_pos + WIDTH / 8):
                # if tile is empty
                if tile.piece.player is None and tile_flag:
                    return(False, None, None)
                # if tile found return key and tile
                return(True, key, tile)
    # if no tile is found
    return(False, None, None)


def checkmate(player, enemy, king):
    ''' checkmate() iterates through all sprites in sprite group corresponding
    to players pieces except for players king and calles the moveset function
    corresponding to each pieces class. It then checks if any of the possible
    moves corresponds to the enemy's kings position. If true, "check" will
    be outputed. Additinally, checkmate() checks if the the enemy king is alive.
    if dead, game loop will end. '''
    for x in all_sprites:   # loop through all sprites (pieces)
        # if piece found is same as player piece
        if x.player == player and not isinstance(x, type(king)):
            if x != new_tile.piece:  # if piece hasn't moved
                # find moveset using old coordinates
                x.moveset(player, enemy, x.key, dc)
            else:   # if piece moved
                # find moveset using new coordinates
                x.moveset(player, enemy, new_key, dc)
            for y in x.available_moves:  # loop through all available moves
                # if any of the available moves for a piece is on a king
                if int(y.x_pos) == king.rect.x and int(y.y_pos) == king.rect.y:
                    print("CHECK")  # print check
        try:
            for y in x.kill_set.items():
                if int(y[1].x_pos) == king.rect.x and int(
                        y[1].y_pos) == king.rect.y:
                    print("CHECK")  # print check
        except:
            pass

    if not king.alive():    # if king is killed
        print(enemy, "LOSES")   # print you lose
        return(False)   # return running is false (breaks game loop)
    return(True)    # else return true (king is alive)


def make_pieces():
    i = 1   # initial tile coordinate (eg B1 , i=1)
    for x in range(0, 8):  # black pieces
        key = "B{}"     # start a second row for pawns
        key = key.format(i)  # i is the column number
        # pick a random pawn from pawn list and place it on the tile
        # corresponing to the key
        x = random.choice(random_pawn)(board.dc[key], "BLACK", key)
        all_sprites.add(x)  # add created sprite to sprite list
        key = "A{}"     # start first row for "exclusive" pieces
        key = key.format(i)  # column number
        if key == "A5":     # tile "A5" is reserved for king
            k1 = EUP.king(board.dc["A5"], "BLACK", "A5")    # create king
            all_sprites.add(k1)  # add king to sprite group
            i += 1  # next column
            continue
        # next piece
        x = random.choice(random_exclusive)(board.dc[key], "BLACK", key)
        all_sprites.add(x)  # add next piece
        i += 1  # new column

    i = 1   # start at column 1 for white pieces
    for x in range(0, 8):  # white pieces
        key = "G{}"  # Row "G"
        key = key.format(i)  # create key (G{i}; i is column number)
        # select random piece from pawn list
        x = random.choice(random_pawn)(board.dc[key], "WHITE", key)
        all_sprites.add(x)  # add piece to sprite group
        key = "H{}"  # Row "H"
        key = key.format(i)  # create key with i as column number
        if key == "H5":  # Reserved tile for king
            K2 = EUP.king(board.dc["H5"], "WHITE", "H5")    # create king
            all_sprites.add(K2)  # add king to sprite group
            i += 1  # next column
            continue
        # create next piece
        x = random.choice(random_exclusive)(board.dc[key], "WHITE", key)
        all_sprites.add(x)  # add piece to sprite group
        i += 1  # next column
    return(k1, K2)   # retun kings (black, white) to check for checkmate


tile_flag = 1
fps = 30
clock = pygame.time.Clock()
board = board()  # initialize board
dc = board.give_dictionary()    # dictionary containing all tiles
all_sprites = pygame.sprite.Group()  # sprite group
k1, K2 = make_pieces()   # make pieces onto board, return kings

running = True  # run game
white_turn = True   # white goes first

if __name__ == "__main__":
    while running:
        clock.tick(fps)  # set constant fps
        board.draw_board()  # draw board
        all_sprites.update()    # update sprite
        all_sprites.draw(display)   # draw sprite
        pygame.display.update()  # update display
        pygame.display.flip()   # update display

        for event in pygame.event.get(
        ):  # if close button is hit, close window
            if event.type == pygame.QUIT:
                running = False
            # if player clicked on something
            if event.type == pygame.MOUSEBUTTONDOWN:
                # get the location of the mouse
                mouse_pos = pygame.mouse.get_pos()
                # see if player clicked on a tile and if there is a piece on it
                found, key, tile = find_tile(
                    board, mouse_pos, tile_flag)

                # if a tile and piece is found, check the player is 'white'
                # and if it's white turn
                if found and tile.piece.player == "WHITE" and white_turn:
                    # highlight the available moves corresponding to the piece
                    tile.piece.highlight(key, tile, dc)
                    wait_button()   # wait for input for new location to move to
                    # obtain location of new location
                    new_mouse_pos = pygame.mouse.get_pos()
                    # if new location is tile, found will be true
                    found, new_key, new_tile = find_tile(
                        board, new_mouse_pos, not tile_flag)
                    if found:   # if tile is found
                        # move piece to new location and check promotion
                        changed, promotion, new_promo = tile.piece.move(
                            new_tile)
                        if changed:  # if the move is successful
                            try:    # see if enemy king is in check
                                running = checkmate("WHITE", "BLACK", k1)
                            except:
                                pass
                            white_turn = False  # switch to black turn
                            if promotion:   # if piece qualifies for promotion
                                # add new promoted piece to sprite group
                                all_sprites.add(new_promo)

                elif found and tile.piece.player == "BLACK" and not white_turn:
                    # highlight available moves
                    tile.piece.highlight(key, tile, dc)
                    wait_button()   # wait for input for new location
                    # get new mouse position
                    new_mouse_pos = pygame.mouse.get_pos()
                    found, new_key, new_tile = find_tile(
                        board, new_mouse_pos, not tile_flag)  # locate new tile
                    if found:
                        # move piece to new tile
                        changed, promotion, new_promo = tile.piece.move(
                            new_tile)
                        if changed:
                            try:
                                # check if checkmate
                                running = checkmate("BLACK", "WHITE", K2)
                            except:
                                pass
                            white_turn = True   # switch turns
                            if promotion:
                                # add promoted piece to sprite group
                                all_sprites.add(new_promo)
    pygame.quit()
