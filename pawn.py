'''
Behaiviour and attributes unique to Pawn pieces.
'''
import pygame
import sys
import piece
# from queen import Queen

BLACK = (0,0,0)
WHITE = (255,255,255)

class Pawn(piece.Piece):
    '''
    This class is responsible for the behaviour of all Pawn pieces
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
        
        self.en_passent_available = False

        if self.colour == BLACK:
            self.tile_directions = [7, 8, 9]
            self.tile_promotions = [tile for tile in range(56, 65)]
        else:
            self.tile_directions = [-7, -8, -9]
            self.tile_promotions = [tile for tile in range(0, 9)]

    def valid_move(self, target_square, tiles):
        """
        Calculates valid move based on the board and this pieces current position.
        Does not take into account check.
        """
        potential_moves = []

        for tile_direction in self.tile_directions:         
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

        if self.tile_number in right_edge_squares and abs(tile_direction) == 7:
            return
        
        elif self.tile_number in left_edge_squares and abs(tile_direction) == 9:
            return

        elif 64 < self.tile_number + tile_direction  or self.tile_number + tile_direction < 0:
            return
        
        if abs(tile_direction) == 8:
            if tiles[self.tile_number + tile_direction].is_occupied == False:
                potential_moves.append(self.tile_number + tile_direction)

        elif tiles[self.tile_number + tile_direction].is_occupied:
            if tiles[self.tile_number + tile_direction].is_occupied_colour != self.colour:
                potential_moves.append(self.tile_number + tile_direction)


        # self.tile_directions[1] == 8 or -8
        if self.has_moved == False:
            if tiles[self.tile_number + self.tile_directions[1]].is_occupied == False:
                if tiles[self.tile_number + ((self.tile_directions[1])*2)].is_occupied == False:
                    potential_moves.append(self.tile_number + self.tile_directions[1]*2)

    # def promote_pawn(self, piece_list):
    #     """
    #     """
    #     piece_list[piece_list.index(self)] = Queen()