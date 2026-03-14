import pcbnew
import numpy as np


def create_density_grid(grid_size):
    return np.zeros((grid_size, grid_size))


def get_board_dimensions(board):
    """
    Safely compute board width and height using tracks
    """

    min_x = float("inf")
    min_y = float("inf")
    max_x = 0
    max_y = 0

    for item in board.GetTracks():

        pos = item.GetStart()

        x = pos.x
        y = pos.y

        if x < min_x:
            min_x = x

        if y < min_y:
            min_y = y

        if x > max_x:
            max_x = x

        if y > max_y:
            max_y = y

    width = max_x - min_x
    height = max_y - min_y

    # Safety check
    if width == 0:
        width = 1

    if height == 0:
        height = 1

    return width, height


def map_copper_to_grid(board, grid, grid_size):

    width, height = get_board_dimensions(board)

    for item in board.GetTracks():

        if isinstance(item, pcbnew.PCB_TRACK):

            pos = item.GetStart()

            x = pos.x
            y = pos.y

            gx = int((x / width) * grid_size)
            gy = int((y / height) * grid_size)

            if gx >= grid_size:
                gx = grid_size - 1

            if gy >= grid_size:
                gy = grid_size - 1

            grid[gx][gy] += item.GetWidth()

    return grid


def calculate_density_imbalance(grid):

    return np.std(grid)


def analyze_copper_density(board, grid_size=10):

    grid = create_density_grid(grid_size)

    grid = map_copper_to_grid(board, grid, grid_size)

    imbalance = calculate_density_imbalance(grid)

    return grid, imbalance


def interpret_density(imbalance):

    if imbalance < 0.2:
        return "Balanced Copper Distribution"

    elif imbalance < 0.4:
        return "Moderate Copper Imbalance"

    else:
        return "High Copper Imbalance"
