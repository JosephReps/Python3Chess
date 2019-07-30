'''
Python Chess.
'''

"""
CHECKLIST:
    - King pieces <-----
        - Castling
        - Check/stale/mate
    - Pawn pieces <------
        - Double move <------
        - en passent
        - Piece promotion <---- To queen is done

    - Draw in 50 moves
    - Draw by 3x reps

    - fix the square numbers uce
    - use execute move method insted u mung
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
        self.init_piece(60, 1, King, WHITE, 'piece_sprite/white_king.png', 'white king', 0)
        #WHITE KNIGHT
        self.init_piece(40, 1, Knight, WHITE, 'piece_sprite/white_knight.png', 'white knight', 0)
        #BLACK KNIGHT
        self.init_piece(30, 1, Knight, BLACK, 'piece_sprite/black_knight.png', 'black knight', 0)
        #BLACK PAWN
        self.init_piece(23, 1, Pawn, BLACK, 'piece_sprite/black_pawn.png', 'black pawn', 0)
        #WHITE PAWN
        self.init_piece(8, 1, Pawn, WHITE, 'piece_sprite/white_pawn.png', 'white pawn', 0)

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
            
            self.tiles[tile_num].is_occupied = True
            self.tiles[tile_num].is_occupied_colour = colour

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
        self.occupied_squares = [tile.tile_number for tile in self.tiles[1:] if tile.is_occupied]
        
    def capture_piece(self, captured_piece):
        """
        """
        # game.tiles[captured_piece.tile_number].is_occupied = False
        # game.tiles[captured_piece.tile_number].is_occupied_colour = None
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
                        game.tiles[active_piece.tile_number].is_occupied = False
                        game.tiles[active_piece.tile_number].is_occupied_colour = None

            if event.type == pygame.MOUSEBUTTONUP and drag:
                drag = False
                target_square = move_validation.find_closest_tile(game.tiles, pos)
                if active_piece.valid_move(target_square, game.tiles) == 1:
                    active_piece.tile_number = target_square.tile_number
                    movement.drag_piece((target_square.tile_x + 30, target_square.tile_y + 30), 
                                         active_piece)

                    active_piece.has_moved = True

                    if active_piece.piece_label == 'black pawn':
                        if active_piece.tile_number in [tile for tile in range(56, 65)]:
                            game.promote_pawn(active_piece)

                    elif active_piece.piece_label == 'white pawn':
                        if active_piece.tile_number in [tile for tile in range(0, 9)]:
                            game.promote_pawn(active_piece)

                elif active_piece.valid_move(target_square, game.tiles) == 2:
                    game.capture_piece([piece for piece in game.piece_list if piece.tile_number == target_square.tile_number][0])
                    active_piece.tile_number = target_square.tile_number
                    movement.drag_piece((target_square.tile_x + 30, target_square.tile_y + 30), 
                                         active_piece)
                    
                    active_piece.has_moved = True

                else:
                    movement.drag_piece((game.tiles[active_piece.tile_number].tile_x + 30,
                                         game.tiles[active_piece.tile_number].tile_y + 30),
                                         active_piece)

                game.tiles[active_piece.tile_number].is_occupied = True
                game.tiles[active_piece.tile_number].is_occupied_colour = active_piece.colour
                active_piece = None
                game.update_occupied_squares()

                print(game.occupied_squares)

        if drag:
            movement.drag_piece(pos, active_piece)

        board.draw_board(game.screen)

        game.draw_pieces()

        pygame.display.update()