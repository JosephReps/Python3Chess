'''
Behaviour and attributes unique to King pieces.
'''
import piece

BLACK = (0,0,0)
WHITE = (255,255,255)

class King(piece.Piece):
    '''
    This class is responsible for the behaviour of all King pieces
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

        # These are the directions which pieces can attack based on tile numbers 
        self.tile_directions = [8, -8, 1, -1, 7, -7, 9, -9]

    def valid_move(self, target_square, game):
        """
        Checks whether an attempted move is valid. 

        Parameters:
            target_square <Tile object>: The tile which the piece is attempting 
                                         to move to.
            game <Pychess object>: The main game controller.

        Returns:
            3: If the the selected move was to castle.
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
                if abs(target_square.tile_number - self.tile_number) == 2:
                    return 3
                if target_square.occupant:
                    return 2
                else:
                    return 1
        else:
            return potential_moves

    def check_tile_direction(self, potential_moves, tile_direction, game):
        """
        Finds all the possible moves for a piece.

        Parameters:
            potential_moves <list><int>: A list of the tile numbers that 
                                         the piece could move to.
            tile_direction <int>: The number to increment tile number by
                                  while searching for moves. 
            game <Pychess object>: The main game controller.                               
        """
        left_edge = [1, 9, 17, 25, 33, 41, 49, 57]
        right_edge = [8, 16, 24, 32, 40, 48, 56, 64]

        if self.tile_number in left_edge and tile_direction in [-9, 7, -1]:
            return

        elif self.tile_number in right_edge and tile_direction in [9, -7, 1]:
            return

        # If the potential move is off the board.
        elif 64 < self.tile_number + tile_direction or \
                    self.tile_number + tile_direction < 0:
            return

        # If the tile has a piece on it.
        if game.tiles[self.tile_number + tile_direction].occupant:
            if game.tiles[self.tile_number + tile_direction].occupant.colour != self.colour:
                potential_moves.append(self.tile_number + tile_direction)
        else:
            potential_moves.append(self.tile_number + tile_direction)

        self.check_castle(game, potential_moves)

    def check_castle(self, game, potential_moves):
        """
        Checks if it is possible to castle.

        Parameters:
            game <Pychess object>: The main game controller.
            potential_moves <list><int>: A list of the tile numbers that 
                                         the piece could move to.
        """
        if self.has_moved == False:
            if self.colour == (0,0,0):
                if not game.tiles[2].occupant and not game.tiles[3].occupant and not game.tiles[4].occupant:
                    if game.tiles[1].occupant:
                        if game.tiles[1].occupant.has_moved == False and game.tiles[1].occupant.piece_label == 'black rook':
                            potential_moves.append(game.tiles[3].tile_number)

                if not game.tiles[6].occupant and not game.tiles[7].occupant:
                    if game.tiles[8].occupant:
                        if game.tiles[8].occupant.has_moved == False and game.tiles[8].occupant.piece_label == 'black rook':
                            potential_moves.append(game.tiles[7].tile_number)

            if self.colour == (255,255,255):
                if not game.tiles[63].occupant:
                    if not game.tiles[62].occupant:
                        if game.tiles[64].occupant:
                            if game.tiles[64].occupant.has_moved == False and game.tiles[64].occupant.piece_label == 'white rook':
                                potential_moves.append(game.tiles[63].tile_number)

                if not game.tiles[58].occupant:
                    if not game.tiles[59].occupant:
                        if not game.tiles[60].occupant:
                            if game.tiles[57].occupant:
                                if game.tiles[57].occupant.has_moved == False and game.tiles[57].occupant.piece_label == 'white rook':
                                    potential_moves.append(game.tiles[59].tile_number)



