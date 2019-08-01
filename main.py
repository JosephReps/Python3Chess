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

    def event_handler(self):
        """
        """
        pass

    def new_game(self):
        """
        Initiates the game.
        """
        self.piece_list = []
        self.init_pieces()

    def init_pieces(self):
        '''
        Creates black/white pieces, sets the starting pos/square of each piece.
        '''
        #WHITE QUEEN
        self.init_piece(59, 1, Queen, WHITE, 'piece_sprite/white_queen.png', 'white queen', 0)
        #BLACK QUEEN
        self.init_piece(3, 1, Queen, BLACK, 'piece_sprite/black_queen.png', 'black queen', 0)
        #WHITE BISHOP
        self.init_piece(60, 2, Bishop, WHITE, 'piece_sprite/white_bishop.png', 'white bishop', -5)
        #BLACK BISHOP
        self.init_piece(2, 2, Bishop, BLACK, 'piece_sprite/black_bishop.png', 'black bishop', 4)
        #WHITE ROOK
        self.init_piece(64, 1, Rook, WHITE, 'piece_sprite/white_rook.png', 'white rook', -4)
        #BLACK ROOK
        self.init_piece(5, 2, Rook, BLACK, 'piece_sprite/black_rook.png', 'black rook', 4)
        #WHITE KING
        self.init_piece(61, 1, King, WHITE, 'piece_sprite/white_king.png', 'white king', 0)
        #WHITE KNIGHT
        self.init_piece(40, 1, Knight, WHITE, 'piece_sprite/white_knight.png', 'white knight', 0)
        #BLACK KNIGHT
        self.init_piece(30, 1, Knight, BLACK, 'piece_sprite/black_knight.png', 'black knight', 0)
        #BLACK PAWN
        self.init_piece(23, 1, Pawn, BLACK, 'piece_sprite/black_pawn.png', 'black pawn', 0)
        #WHITE PAWN
        self.init_piece(57, 1, Pawn, WHITE, 'piece_sprite/white_pawn.png', 'white pawn', 0)

    def init_piece(self, tile_num, number_of_pieces, 
    piece_type, colour, image, piece_label, tile_num_change):
        '''
        Creates piece objects.

        Args:
            tile_num (int): The tile number the piece will be created on.
            number_of_pieces (int): The number of pieces to be created.
            piece_type (Class): The class of piece to be created.
            colour (tuple): A tuple containing rgb colour of piece.
            image (image): Image of piece sprite.
            piece_label (str): The name of the piece.
            tile_num_change (int): The difference in square number between each piece created.
        '''
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
        '''
        Draws the pieces from piece_list to screen.

        Args:
            screen (Pygame object): Pygame screen object.
            piece_list (list): A list of Piece objects on the board.
        '''
        
        for i in self.piece_list:
            i.draw_piece(self.screen)
    
    def update_occupied_squares(self):
        """
        """
        self.occupied_squares = [tile.tile_number for tile in self.tiles[1:] if tile.occupant]
        
    def capture_piece(self, captured_piece):
        """
        """
        print(captured_piece.piece_label)
        self.piece_list.remove(captured_piece)

    def promote_pawn(self, pawn_to_promote):
        """
        """
        if pawn_to_promote.colour == BLACK:
            image = pygame.image.load('piece_sprite/black_queen.png')
            label = 'black queen'
        else:
            image = pygame.image.load('piece_sprite/white_queen.png')
            label = 'white queen'

        self.piece_list[(self.piece_list.index(pawn_to_promote))] = Queen(pawn_to_promote.piece_x, pawn_to_promote.piece_y, pawn_to_promote.tile_number, pawn_to_promote.colour, image, label)


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