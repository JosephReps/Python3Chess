import pygame

class Tile(object):
    '''
    Tile object which makes up the board.
    '''

    def __init__(self, tile_x, tile_y, tile_size, tile_colour,
    tile_number, occupant=None):
        '''
        Parameters:
            tile_x <int>: X-position of tile.
            tile_y <int>: Y-position of tile.
            tile_size <int>: Size of tile.
            tile_colour <tuple><int>: RGB.
            tile_number <Piece object>: Piece which is occupying tile.

        '''
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.tile_number = tile_number
        self.tile_size = tile_size
        self.tile_colour = tile_colour
        self.occupant = occupant
        
    def draw_tile(self, screen):
        '''
        Creates tile and draws to screen.

        Args:
            screen <Pygame object>: Pygame screen object set in Main.
            tile_object <Pygame rectangle>: Pygame rectangle object. 
        
        Returns:
            Draws a pygame rectangle on screen when called.
            Sets self.tile_object to the pygame rectangle object.
        '''
        self.tile_object = pygame.draw.rect(screen, self.tile_colour, 
                                            [self.tile_x,
                                             self.tile_y,
                                             self.tile_size,
                                             self.tile_size])

def draw_board(screen):
    """
    Creates/draws board.
    """
    tile_number = 1
    tiles = ['']
    tile_size = 60     # Height and width of checkerboard squares.

    for i in range(8):             # Note that i ranges from 0 through 7, inclusive.
        for y in range(8):           # So does j.
            if (i + y) % 2 == 0:       # The top left square is white.
                tile_colour = (255,255,255)
            else:
                tile_colour = (40,40,40)


            tile_x = tile_size*y
            tile_y = tile_size*i

            tiles.append(Tile(tile_x,tile_y,tile_size,tile_colour,tile_number))

            tile_number += 1
    
    for i in tiles[1:]:
        i.draw_tile(screen)

    return tiles
