'''
Basic piece functionality and class for all pieces.
'''

import pygame
import move_validation
import movement

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

        self.piece_object = screen.blit(self.piece_image, (self.piece_x, self.piece_y))

    def execute_move(self, game, pos):   
        '''
        Args:
            pos (tuple): Tuple of mouse x and y coordinates relative to top-left of screen.
        '''
        target_square = move_validation.find_closest_tile(game.tiles, pos)
        if self.valid_move(target_square, game) == 1:
            
            try:
                for each_tile in game.en_passent_tiles:
                    # game.tiles[each_tile].is_occupied = False
                    # game.tiles[each_tile].is_occupied_colour = None
                    game.tiles[each_tile].occupant = None         
            except IndexError as e:
                print(f"ERROR: {e}")
                print(each_tile)

            game.en_passent_tiles = {}

            if self.piece_label == 'black pawn':
                if abs(self.tile_number - target_square.tile_number) == 16:
                    game.en_passent_tiles[self.tile_number + 8] = self

                if target_square.tile_number in [tile for tile in range(56, 65)]:
                    game.promote_pawn(self)

            elif self.piece_label == 'white pawn':
                if abs(self.tile_number - target_square.tile_number) == 16:
                    game.en_passent_tiles[self.tile_number - 8] = self

                if target_square.tile_number in [tile for tile in range(0, 9)]:
                    game.promote_pawn(self)

            self.tile_number = target_square.tile_number
            movement.drag_piece((target_square.tile_x + 30, target_square.tile_y + 30), 
                                    self)

            self.has_moved = True

        elif self.valid_move(target_square, game) == 2:
            print("Capturing")
            if target_square.tile_number in game.en_passent_tiles.keys():
                piece_to_capture = game.en_passent_tiles[target_square.tile_number]
            else:
                piece_to_capture = target_square.occupant
            game.capture_piece(piece_to_capture)
            self.tile_number = target_square.tile_number
            movement.drag_piece((target_square.tile_x + 30, target_square.tile_y + 30), 
                                    self)
            
            self.has_moved = True

        else:
            movement.drag_piece((game.tiles[self.tile_number].tile_x + 30,
                                    game.tiles[self.tile_number].tile_y + 30),
                                    self)

        game.tiles[self.tile_number].occupant = self
        game.update_occupied_squares()
        print(game.en_passent_tiles)


    def check_tile_direction(self, potential_moves, tile_direction, game):
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
                if game.tiles[self.tile_number + square].occupant:
                    print("Occupied sq")
                    if game.tiles[self.tile_number + square].occupant.colour != self.colour:
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
                if game.tiles[self.tile_number + square].occupant:
                    if game.tiles[self.tile_number + square].occupant.colour != self.colour:
                        potential_moves.append(self.tile_number + square)
                        break
                    else:
                        break
                else:
                    potential_moves.append(self.tile_number + square)

                if (self.tile_number + square) in edge_squares:
                    break

                square += tile_direction
        




            


