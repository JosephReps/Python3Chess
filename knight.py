'''
Behaviour and attributes unique to Queen pieces.
'''
import piece

BLACK = (0,0,0)
WHITE = (255,255,255)

class Knight(piece.Piece):
    '''
    This class is responsible for the behaviour of all Knight pieces
    during the game.
    '''

    def __init__(self, piece_x, piece_y, tile_number, colour, piece_image, 
                 piece_label):
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

        for tile_direction in [6, 10, 15, 17, -6, -10, -15, -17]:         
            self.check_tile_direction(potential_moves, tile_direction, game)

        if target_square:
            if target_square.tile_number in potential_moves:
                if target_square.occupant:
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
        one_from_left_edge = [square + 1 for square in left_edge_squares]
        right_edge_squares = [8, 16, 24, 32, 40, 48, 56, 64]
        one_from_right_edge = [square - 1 for square in right_edge_squares]

        if self.tile_number in left_edge_squares \
                and tile_direction in [6, -10, -17, 15]:
            return

        elif self.tile_number in right_edge_squares \
                and tile_direction in [-6, 10, 17, -15]:
            return
        
        elif self.tile_number in one_from_right_edge and \
                                            tile_direction in [-6, 10]:
            return

        elif self.tile_number in one_from_left_edge \
                                and tile_direction in [6, -10]:
            return

        elif 64 < self.tile_number + tile_direction or \
                    self.tile_number + tile_direction < 0:
            return

        if game.tiles[self.tile_number + tile_direction].occupant:
            if game.tiles[self.tile_number + tile_direction].occupant.colour != self.colour:
                potential_moves.append(self.tile_number + tile_direction)
        else:
            potential_moves.append(self.tile_number + tile_direction)