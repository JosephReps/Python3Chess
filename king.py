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

        # Hard coded castling_squares, but much more self explanatory
        # than alternative
        if self.colour == (0,0,0):
            self.castle_squares = [0, 8]
        else:
            self.castle_squares = [57, 64]

    def valid_move(self, target_square, game):
        """
        Calculates valid move based on the board and this pieces current position.
        Does not take into account check.
        """
        potential_moves = []

        for tile_direction in [8, -8, 1, -1, 7, -7, 9, -9]:         
            self.check_tile_direction(potential_moves, tile_direction, game)

        if target_square.tile_number in potential_moves:
            if abs(target_square.tile_number - self.tile_number) == 2:
                return 3
            if target_square.occupant:
                return 2
            else:
                return 1
            

    def check_tile_direction(self, potential_moves, tile_direction, game):
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

        if game.tiles[self.tile_number + tile_direction].occupant:
            if game.tiles[self.tile_number + tile_direction].occupant.colour != self.colour:
                potential_moves.append(self.tile_number + tile_direction)
        else:
            potential_moves.append(self.tile_number + tile_direction)

        self.check_castle(game, potential_moves)

    def check_castle(self, game, potential_moves):
        """
        GrOsSSSSS right now.
        """
        if self.colour == (0,0,0):
            if not game.tiles[2].occupant:
                if not game.tiles[3].occupant:
                    if not game.tiles[4].occupant:
                        if game.tiles[0].occupant.has_moved == False and game.tiles[0].occupant.piece_label == 'black rook':
                            potential_moves.append(game.tiles[3].tile_number)

                if not game.tiles[6].occupant:
                    if not game.tiles[7].occupant:
                        if game.tiles[8].occupant.has_moved == False and game.tiles[8].occupant.piece_label == 'black rook':
                            potential_moves.append(game.tiles[7].tile_number)

        if self.colour == (255,255,255):
            if not game.tiles[63].occupant:
                if not game.tiles[62].occupant:
                    if game.tiles[64].occupant.has_moved == False and game.tiles[64].occupant.piece_label == 'white rook':
                        potential_moves.append(game.tiles[63].tile_number)

            if not game.tiles[58].occupant:
                if not game.tiles[59].occupant:
                    if not game.tiles[60].occupant:
                        if game.tiles[57].occupant.has_moved == False and game.tiles[57].occupant.piece_label == 'white rook':
                            potential_moves.append(game.tiles[59].tile_number)



