'''
Python Chess.
'''

"""
CHECKLIST:
    - King pieces <-----
        - Castling <------
        - Check/stale/mate
    - Pawn pieces <------
        - Double move <------
        - en passent <------- 
        - Piece promotion <---- To queen is done (GLTICHY)

    - Draw in 50 moves
    - Draw by 3x reps

    - fix the square numbers uce
"""

import pygame
import board
import movement
from pawn import Pawn
from knight import Knight
from queen import Queen
from bishop import Bishop
from rook import Rook
from king import King
import move_validation

BLACK = (0,0,0)
WHITE = (255,255,255)

class PyChess():
    """
    Game controller.
    """

    def __init__(self):
        """
        """
        pygame.display.init()
        pygame.display.set_caption('Joeys Pygame Chess')
        window = (480,480)

        self.screen = pygame.display.set_mode(window)
        self.tiles = board.draw_board(self.screen)

        self.move_history = []
        self.en_passent_tiles = {}

        self.player_turn = (255,255,255)

        self.piece_list = []
        self.occupied_squares = []

        self.white_check = False
        self.black_check = False

    def event_handler(self):
        """
        """
        pass

    def new_game(self):
        """
        Initiates the game.
        Creates all pieces and sets them to starting position.
        """
        self.init_pieces()
        self.white_king = [piece for piece in self.piece_list if piece.piece_label == 'white king'][0]
        self.black_king = [piece for piece in self.piece_list if piece.piece_label == 'black king'][0]

    def init_pieces(self):
        '''
        Creates black/white pieces, sets the starting pos/square of each piece.
        '''
        #WHITE QUEEN
        self.init_piece(60, 1, Queen, WHITE, 'piece_sprite/white_queen.png', 'white queen', 0)
        #BLACK QUEEN
        self.init_piece(4, 1, Queen, BLACK, 'piece_sprite/black_queen.png', 'black queen', 0)
        #WHITE BISHOP
        self.init_piece(62, 2, Bishop, WHITE, 'piece_sprite/white_bishop.png', 'white bishop', -3)
        #BLACK BISHOP
        self.init_piece(3, 2, Bishop, BLACK, 'piece_sprite/black_bishop.png', 'black bishop', 3)
        #WHITE ROOK
        self.init_piece(64, 2, Rook, WHITE, 'piece_sprite/white_rook.png', 'white rook', -7)
        #BLACK ROOK
        self.init_piece(1, 2, Rook, BLACK, 'piece_sprite/black_rook.png', 'black rook', 7)
        #WHITE KING
        self.init_piece(61, 1, King, WHITE, 'piece_sprite/white_king.png', 'white king', 0)
        #BLACK KING
        self.init_piece(5, 1, King, BLACK, 'piece_sprite/black_king.png', 'black king', 0)
        #WHITE KNIGHT
        self.init_piece(63, 2, Knight, WHITE, 'piece_sprite/white_knight.png', 'white knight', -5)
        #BLACK KNIGHT
        self.init_piece(2, 2, Knight, BLACK, 'piece_sprite/black_knight.png', 'black knight', 5)
        #BLACK PAWN
        self.init_piece(9, 8, Pawn, BLACK, 'piece_sprite/black_pawn.png', 'black pawn', 1)
        #WHITE PAWN
        self.init_piece(56, 8, Pawn, WHITE, 'piece_sprite/white_pawn.png', 'white pawn', -1)

    def init_piece(self, tile_num, number_of_pieces, 
    piece_type, colour, image, piece_label, tile_num_change):
        """
        Creates piece objects, appends them to piece_list.

        Args:
            tile_num (int): The tile number the piece will be created on.
            number_of_pieces (int): The number of pieces to be created.
            piece_type (Class): The class of piece to be created.
            colour (tuple): A tuple containing rgb colour of piece.
            image (image): Image of piece sprite.
            piece_label (str): The name of the piece.
            tile_num_change (int): The difference in square number between 
                                   each piece created.
        """
        tile_num = tile_num

        for _ in range(number_of_pieces):
            self.piece_list.append(piece_type(
                self.tiles[tile_num].tile_x + 5,
                self.tiles[tile_num].tile_y + 5,
                self.tiles[tile_num].tile_number,
                colour,
                pygame.image.load(image),
                piece_label
                ))
            
            self.tiles[tile_num].occupant = self.piece_list[-1]

            tile_num += tile_num_change
    
    def draw_pieces(self):
        """
        Draws the pieces from piece_list to screen.
        """
        for i in self.piece_list:
            i.draw_piece(self.screen)
    
    def update_occupied_squares(self):
        """
        Updates the occupied squares list.
        """
        self.occupied_squares = [tile.tile_number for tile in self.tiles[1:] if tile.occupant]
        
    def capture_piece(self, captured_piece):
        """
        Removes piece from piece list.

        Parameters:
            captured_piece <Piece object>: Piece which is to be removed.
        """
        self.piece_list.remove(captured_piece)

    def promote_pawn(self, pawn_to_promote):
        """
        Promotes pawn to queen.

        Parameters:
            pawn_to_promote <Piece object>: The pawn to be promoted.
        """
        if pawn_to_promote.colour == BLACK:
            image = pygame.image.load('piece_sprite/black_queen.png')
            label = 'black queen'
        else:
            image = pygame.image.load('piece_sprite/white_queen.png')
            label = 'white queen'

        self.piece_list[(self.piece_list.index(pawn_to_promote))] = Queen(pawn_to_promote.piece_x, pawn_to_promote.piece_y, pawn_to_promote.tile_number, pawn_to_promote.colour, image, label)

    def toggle_turn(self):
        """
        Changes the player turn.
        """
        if self.player_turn == (255,255,255):
            self.player_turn = (0,0,0)
        else:
            self.player_turn = (255,255,255)

    def check(self, colour):
        """
        """
        if colour == (255,255,255):
            if self.white_king.tile_number in self.get_attacked_squares(colour):
                print("WHITE CHECK")
                return True
        else:
            if self.black_king.tile_number in self.get_attacked_squares(WHITE):
                print("BLACK CHECK")
                return True

    def get_attacked_squares(self, colour):
        """
        Finds all the tile numbers which are attacked by a player.

        Parameters:
            colour <tuple><int>: RGB, either BLACK or WHITE. The colour of player
                                 who we are checking.
        
        Returns:
            attacked_squares <list><int>: A list of tile numbers which are attacked
                                          by the chosen player.
        """
        attacked_squares = set([square for piece in self.piece_list for square in piece.valid_move(None, self) if piece.colour == colour])
        return list(attacked_squares)


if __name__ == '__main__':
    game = PyChess()
    game.new_game()

    running = True
    drag = False

    while running:

        # Mouse position (x,y)
        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Quitting")
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN: 
                for y in game.piece_list:
                    if y.piece_object.collidepoint(pos):
                        if y.colour == game.player_turn:
                            drag = True
                            active_piece = y
                            game.tiles[active_piece.tile_number].occupant = None

            if event.type == pygame.MOUSEBUTTONUP and drag:
                active_piece.execute_move(game, pos)
                drag = False
                active_piece = None

        if drag:
            movement.drag_piece(pos, active_piece)

        board.draw_board(game.screen)

        game.draw_pieces()

        pygame.display.update()