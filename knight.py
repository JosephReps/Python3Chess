'''
Behaiviour and attributes unique to Queen pieces.
'''
import pygame
import sys
import piece

BLACK = (0,0,0)
WHITE = (255,255,255)

class Knight(piece.Piece):
    '''
    This class is responsible for the behaviour of all Knight pieces
    during the game.
    This includes:
        - Move verification
    '''

    def __init__(self, piece_x, piece_y, tile_number, colour, piece_image, piece_label):
        '''
        Args:
            piece_label (string): String containing name of piece.
        '''

        super().__init__(piece_x, piece_y, tile_number, colour, piece_image,)
        self.piece_label = piece_label
        

    def valid_move(self, target_square, tiles):
        """
        Calculates valid move based on the board and this pieces current position.
        Does not take into account check.
        """
        potential_moves = []

        for tile_direction in [6, 10, 15, 17, -6, -10, -15, -17]:         
            self.check_tile_direction(potential_moves, tile_direction, tiles)

        if target_square.tile_number in potential_moves:
            if target_square.is_occupied:
                return 2
            else:
                return 1

    def check_tile_direction(self, potential_moves, tile_direction, tiles):
        """
        """
        left_edge_squares = [1, 9, 17, 25, 33, 41, 49, 57]
        one_from_left_edge_squares = [square + 1 for square in left_edge_squares]
        right_edge_squares = [8, 16, 24, 32, 40, 48, 56, 64]
        one_from_right_edge_squares = [square - 1 for square in right_edge_squares]

        if self.tile_number in left_edge_squares and tile_direction in [6, -10, -17, 15]:
            return

        elif self.tile_number in right_edge_squares and tile_direction in [-6, 10, 17, -15]:
            return
        
        elif self.tile_number in one_from_right_edge_squares and tile_direction in [-6, 10]:
            return

        elif self.tile_number in one_from_left_edge_squares and tile_direction in [6, -10]:
            return

        elif 64 < self.tile_number + tile_direction  or self.tile_number + tile_direction < 0:
            return

        if tiles[self.tile_number + tile_direction].is_occupied:
            if tiles[self.tile_number + tile_direction].is_occupied_colour != self.colour:
                potential_moves.append(self.tile_number + tile_direction)
        else:
            potential_moves.append(self.tile_number + tile_direction)