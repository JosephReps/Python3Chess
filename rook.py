'''
Behaiviour and attributes unique to Queen pieces.
'''
import pygame
import sys
import piece

BLACK = (0,0,0)
WHITE = (255,255,255)

class Rook(piece.Piece):
    '''
    This class is responsible for the behaviour of all Rook pieces
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

        for tile_direction in [8, -8, 1, -1]:     
            self.check_tile_direction(potential_moves, tile_direction, tiles)

        if target_square.tile_number in potential_moves:
            if target_square.occupant:
                return 2
            else:
                return 1
        