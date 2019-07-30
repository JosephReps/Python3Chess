'''
Basic piece functionality and class for all pieces.
'''

import pygame
import move_validation

class Piece():
    '''
    Basic attributes/functions relevant to piece type objects.
    '''

    def __init__(self,piece_x,piece_y,tile_number, colour, piece_image):
        '''
        Args:
            piece_x (int): Piece's x-pixel location, based on top-leftmost pixel of self.
            piece_y (int): Piece's y-pixel location, based on top-leftmost pixel of self.
            current_tile_number (int): Self's tile number on the board.
            colour (tuple): A tuple of three int's, making RGB colour.
            piece_image (image): Image of piece.
        '''

        self.piece_image = piece_image
        self.piece_x = piece_x
        self.piece_y = piece_y
        self.tile_number = tile_number
        self.colour = colour

        self.has_moved = False

    def draw_piece(self,screen):
        '''
        Draws piece to screen.

        Args:
            screen (Pygame object): Pygame screen object set in `Main`.
        
        Returns:
            Draws a pygame image on screen when called.
        '''

        self.piece_object = screen.blit(self.piece_image, (self.piece_x,self.piece_y))

    def execute_move(self, tiles, pos):   
        '''
        Executes attempted move, now that it has been validated by the `valid_move`
            method.
        During execution, it also performs checks for potential castling, piece_promotion
            and captured pieces.
        IMPORTANT:
            It is during this method, that validity of a move based on 'check' is determined.

        Args:
            tiles (list): A list of Tile objects.
            pos (tuple): Tuple of mouse x and y coordinates relative to top-left of screen.

        Returns:
            True if move was valid.
        '''
        self.has_moved = True
        print("MOVED", self.has_moved)
        
        tiles[self.tile_number].is_occupied = False
        move_validation.find_closest_tile(tiles,pos).is_occupied = True
        self.tile_number = move_validation.find_closest_tile(tiles,pos).tile_number

        # Centers piece on tile
        self.piece_x = tiles[self.tile_number].tile_x + 25
        self.piece_y = tiles[self.tile_number].tile_y + 25

        return True

    def check_tile_direction(self, potential_moves, tile_direction, tiles):
        """
        """
        edge_squares = [1, 9, 17, 25, 33, 41, 49, 57, 8, 16, 24, 32, 40, 48, 56, 64]
        left_edge_squares = [1, 9, 17, 25, 33, 41, 49, 57]
        right_edge_squares = [8, 16, 24, 32, 40, 48, 56, 64]

        if self.tile_number in left_edge_squares and tile_direction in [-9, 7, -1]:
            return

        elif self.tile_number in right_edge_squares and tile_direction in [9, -7, 1]:
            return

        if abs(tile_direction) == 8:
            square = tile_direction
            while 0 < self.tile_number + square < 65:
                # print(square)
                if tiles[self.tile_number + square].is_occupied:
                    if tiles[self.tile_number + square].is_occupied_colour != self.colour:
                        potential_moves.append(self.tile_number + square)
                        break
                    else:
                        break
                else:
                    potential_moves.append(self.tile_number + square)
                
                square += tile_direction

        else:
            square = tile_direction
            while 0 < self.tile_number + square < 65:
                if tiles[self.tile_number + square].is_occupied:
                    if tiles[self.tile_number + square].is_occupied_colour != self.colour:
                        potential_moves.append(self.tile_number + square)
                        break
                    else:
                        break
                else:
                    potential_moves.append(self.tile_number + square)

                if (self.tile_number + square) in edge_squares:
                    break

                square += tile_direction
        
        print(potential_moves)





            


