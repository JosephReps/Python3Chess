'''
Behaviour and attributes unique to Pawn pieces.
'''
import piece

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
            piece_x <int>: The x-position of the piece on the game screen.
            piece_y <int>: The y-position of the piece on the game screen.
            tile_number <int>: The tile number the piece is on.
            colour <tuple><int>: RGB, either BLACK or WHITE.
            piece_image <str>: The image of the piece.
            piece_label <string>: String containing name of piece.
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

    def valid_move(self, target_square, game):
        """
        Checks whether an attempted move is valid. 

        Parameters:
            target_square <Tile object>: The tile which the piece is attempting 
                                         to move to.
            game <Pychess object>: The main game controller.

        Returns:
            2: If the selected move was a capture.
            1: If the selected move was a normal move.
            potential_moves <list><int>: A list of the tile numbers that 
                                        the piece could move to.
        """
        potential_moves = []

        for tile_direction in self.tile_directions:         
            self.check_tile_direction(potential_moves, tile_direction, game)

        if target_square:
            if target_square.tile_number in potential_moves:
                if target_square.occupant or \
                    target_square.tile_number in game.en_passent_tiles:
                    return 2
                else:
                    return 1
        
        else:
            return potential_moves

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
        left_edge_squares = [1, 9, 17, 25, 33, 41, 49, 57]
        right_edge_squares = [8, 16, 24, 32, 40, 48, 56, 64]

        if self.tile_number in right_edge_squares and abs(tile_direction) == 7:
            return
        
        elif self.tile_number in left_edge_squares and abs(tile_direction) == 9:
            return

        elif 64 < self.tile_number + tile_direction or \
                    self.tile_number + tile_direction < 0:          
            return

        if abs(tile_direction) == 8:
            if not game.tiles[self.tile_number + tile_direction].occupant:
                potential_moves.append(self.tile_number + tile_direction)

        elif game.tiles[self.tile_number + tile_direction].occupant:
            if game.tiles[self.tile_number + tile_direction].occupant.colour != self.colour:
                potential_moves.append(self.tile_number + tile_direction)
        
        
        elif self.tile_number + tile_direction in game.en_passent_tiles.keys():
            potential_moves.append(self.tile_number + tile_direction)

        # self.tile_directions[1] == 8 or -8
        if self.has_moved == False:
            if not game.tiles[self.tile_number + self.tile_directions[1]].occupant:
                if not game.tiles[self.tile_number + ((self.tile_directions[1])*2)].occupant:
                    potential_moves.append(self.tile_number + self.tile_directions[1]*2)                