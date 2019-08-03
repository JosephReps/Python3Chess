def drag_piece(pos, active_piece):
    '''
    Sets currently clicked piece's x/y values to that of mouse,
    creating a drag effect.

    Args:
        pos <tuple>: Tuple of mouse x and y.
        active_piece <Piece object>: The currently clicked piece.

    Returns:
        Clicked piece's new x/y coordinates, which are equal to the mouse.
    '''
    # -25 to center the piece.
    active_piece.piece_x = pos[0] - 25
    active_piece.piece_y = pos[1] - 25