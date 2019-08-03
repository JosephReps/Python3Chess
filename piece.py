'''
Basic piece functionality and class for all pieces.
'''
import move_validation
import movement

class Piece():
    '''
    Basic attributes/functions relevant to piece type objects.
    '''

    def __init__(self, piece_x, piece_y, tile_number, colour, piece_image):
        ''' 
        Args:
            piece_x <int><int>: Piece's x-position.
            piece_y <int><int>: Piece's y-position.
            current_tile_number <int><int>: Self's tile number on the board.
            colour <tuple><int>: RGB, BLACK or WHITE.
            piece_image <image>: Image of piece.
        '''

        self.piece_image = piece_image
        self.piece_x = piece_x
        self.piece_y = piece_y
        self.tile_number = tile_number
        self.colour = colour

        self.has_moved = False

    def draw_piece(self, screen):
        '''
        Draws piece to screen.

        Args:
            screen <Pygame object>: Pygame screen object.
        '''
        self.piece_object = screen.blit(self.piece_image, 
                                       (self.piece_x, self.piece_y))

    def execute_move(self, game, pos):   
        '''
        Executes a selected move.

        Args:
            pos <tuple><int>: Mouse x and y coordinates.
            game <Pychess object>: The main game controller.
        '''
        target_square = move_validation.find_closest_tile(game.tiles, pos)

        # Normal move
        if self.valid_move(target_square, game) == 1:
            
            self.pawn_specific(target_square, game)

            self.tile_number = target_square.tile_number
            movement.drag_piece((target_square.tile_x + 30, target_square.tile_y + 30), 
                                    self)

            self.has_moved = True
            game.toggle_turn()

        # Capture
        elif self.valid_move(target_square, game) == 2:

            if target_square.tile_number in game.en_passent_tiles.keys():
                piece_to_capture = game.en_passent_tiles[target_square.tile_number]
            else:
                piece_to_capture = target_square.occupant

            game.capture_piece(piece_to_capture)
            self.tile_number = target_square.tile_number
            movement.drag_piece((target_square.tile_x + 30, target_square.tile_y + 30), 
                                    self)
            
            self.has_moved = True
            game.toggle_turn()

        # Castling
        elif self.valid_move(target_square, game) == 3:
            self.castle(target_square.tile_number, game)
            self.tile_number = target_square.tile_number
            movement.drag_piece((target_square.tile_x + 30, target_square.tile_y + 30), 
                                    self)
            game.toggle_turn()
        
        # Returns the piece to origin
        else:
            movement.drag_piece((game.tiles[self.tile_number].tile_x + 30,
                                    game.tiles[self.tile_number].tile_y + 30),
                                    self)

        game.tiles[self.tile_number].occupant = self
        game.update_occupied_squares()

    def pawn_specific(self, target_square, game):
        """
        Deals with pawn-only move validation:
            - Enpassent
            - Piece promotion

        Parameters:
            target_square <Tile object>: The tile which the piece is attempting 
                                         to move to.
            game <Pychess object>: The main game controller.  
        """
        for each_tile in game.en_passent_tiles:
            game.tiles[each_tile].occupant = None         

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

    def check_tile_direction(self, potential_moves, tile_direction, game):
        """
        Creates a list of potential moves in direction of tile_direction.

        Parameters:
            potential_moves <list>: An empty list which will contain
                                    our potential moves.
            tile_direction <int>: The direction we are checking, eg:
                                  vertical will be +8 or -8.
            game <Pychess object>: The main game controller. 
        """
        edge_squares = [1, 9, 17, 25, 33, 41, 49, 57, 8, 
                        16, 24, 32, 40, 48, 56, 64]
        left_edge = [1, 9, 17, 25, 33, 41, 49, 57]
        right_edge = [8, 16, 24, 32, 40, 48, 56, 64]

        if self.tile_number in left_edge and tile_direction in [-9, 7, -1]:
            return

        elif self.tile_number in right_edge and tile_direction in [9, -7, 1]:
            return

            square = tile_direction
            while 0 < self.tile_number + square < 65:
                if abs(tile_direction) != 8:
                    if (self.tile_number + square) in edge_squares:
                        break
                if game.tiles[self.tile_number + square].occupant:
                    if game.tiles[self.tile_number + square].occupant.colour != self.colour:
                        potential_moves.append(self.tile_number + square)
                        break
                    else:
                        break
                else:
                    potential_moves.append(self.tile_number + square)
                
                square += tile_direction

    def castle(self, square_number, game):
        """
        Castles, and adjusts tile/piece attributes accordingly.

        Parameters:
            square_number <int>: The new square number of the king.
            game <Pychess object>: The main game controller. 
        """
        if square_number == 3:
            game.tiles[4].occupant = game.tiles[1].occupant
            game.tiles[4].occupant.tile_number = 4
            game.tiles[1].occupant = None
            movement.drag_piece((game.tiles[4].tile_x + 30, game.tiles[4].tile_y + 30), 
                        game.tiles[4].occupant)
        elif square_number == 7:
            game.tiles[6].occupant = game.tiles[8].occupant
            game.tiles[6].occupant.tile_number = 6
            game.tiles[8].occupant = None
            movement.drag_piece((game.tiles[6].tile_x + 30, game.tiles[6].tile_y + 30), 
                        game.tiles[6].occupant)
        elif square_number == 63:
            game.tiles[62].occupant = game.tiles[64].occupant
            game.tiles[62].occupant.tile_number = 62
            game.tiles[64].occupant = None
            movement.drag_piece((game.tiles[62].tile_x + 30, game.tiles[62].tile_y + 30), 
                        game.tiles[62].occupant)
        elif square_number == 59:
            game.tiles[60].occupant = game.tiles[57].occupant
            game.tiles[60].occupant.tile_number = 60
            game.tiles[57].occupant = None
            movement.drag_piece((game.tiles[60].tile_x + 30, game.tiles[60].tile_y + 30), 
                        game.tiles[60].occupant)
        




            


