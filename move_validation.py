def find_closest_tile(tiles, pos):
    '''
    Locates the closest tile on the board to the mouse position.

    Args:
        pos <tuple>: Tuple of mouse x and y.
        tiles <list>: A list of Tile objects.

    Returns:
        closest_tile <Tile object>: Tile object which is closest to mouse.
    '''
    distance_to_closest_tile = 99999999

    for tile in tiles[1:]:
        # Distance Formula
        if (tile.tile_x + 30 - pos[0])**2 + (tile.tile_y + 30 - pos[1])**2 < distance_to_closest_tile:
            distance_to_closest_tile = (tile.tile_x + 30 - pos[0])**2 + (tile.tile_y + 30 - pos[1])**2
            closest_tile = tile

    return closest_tile



