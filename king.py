'''
Behaiviour and attributes unique to King pieces.
'''
import pygame
import sys
import piece

BLACK = (0,0,0)
WHITE = (255,255,255)

class King(piece.Piece):
    '''
    This class is responsible for the behaviour of all King pieces
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

        for tile_direction in [8, -8, 1, -1, 7, -7, 9, -9]:         
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
        right_edge_squares = [8, 16, 24, 32, 40, 48, 56, 64]

        if self.tile_number in left_edge_squares and tile_direction in [-9, 7, -1]:
            return

        elif self.tile_number in right_edge_squares and tile_direction in [9, -7, 1]:
            return

        elif 64 < self.tile_number + tile_direction  or self.tile_number + tile_direction < 0:
            return

        print(self.tile_number, tile_direction)

        if tiles[self.tile_number + tile_direction].is_occupied:
            if tiles[self.tile_number + tile_direction].is_occupied_colour != self.colour:
                potential_moves.append(self.tile_number + tile_direction)
        else:
            potential_moves.append(self.tile_number + tile_direction)

        if not self.has_moved:
            self.check_castle(tiles)

    def check_castle(self, tiles, piece_list):
        """
        """
        # if self.colour == (0,0,0):
        #     if tiles
        pass
