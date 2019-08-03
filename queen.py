'''
Behaviour and attributes unique to Queen pieces.
'''
import piece

BLACK = (0,0,0)
WHITE = (255,255,255)

class Queen(piece.Piece):
    '''
    This class is responsible for the behaviour of all Queen pieces
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

        for tile_direction in [8, -8, 1, -1, 7, -7, 9, -9]:     
            self.check_tile_direction(potential_moves, tile_direction, game)

        if target_square:
            if target_square.tile_number in potential_moves:
                if target_square.occupant:
                    return 2
                else:
                    return 1
        else:
            return potential_moves