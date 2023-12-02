from cell import AStarCell
import random as r
import pygame

WIDTH = 600
CELLS = 20
CELL_WIDTH = WIDTH // CELLS

def draw(screen, board):
    screen.fill((255, 255, 255))

    for row in board:
        for cell in row:
            cell.draw(screen)

    # pygame.display.update()

def generate_board() -> list[list[AStarCell]]:
    return [[AStarCell(j, i, CELL_WIDTH) for i in range(CELLS)] for j in range(CELLS)]


def get_neighbours(cell: AStarCell, board: list[list[AStarCell]]) -> list[AStarCell]:
    x, y = cell.get_grid_coords()
    neighbors = []

    if x-1 >= 0:
        neighbors.append(board[x-1][y])
    if x+1 <= CELLS-1: 
        neighbors.append(board[x+1][y])
    if y-1 >= 0:
        neighbors.append(board[x][y-1])
    if y+1 <= CELLS-1:
        neighbors.append(board[x][y+1])
        
    neighbors = [c for c in neighbors if not c.visited]
    if neighbors: 
        # return neighbors[-1]
        return r.choice(neighbors)
    
    return None

def get_maze_neighbours(cell: AStarCell, board: list[list[AStarCell]]) -> list[AStarCell]:
    x, y = cell.get_grid_coords()
    neighbors = []

    if x-1 >= 0:
        neighbors.append(board[x-1][y])
    if x+1 <= CELLS-1: 
        neighbors.append(board[x+1][y])
    if y-1 >= 0:
        neighbors.append(board[x][y-1])
    if y+1 <= CELLS-1:
        neighbors.append(board[x][y+1])
        
    neighbors = [c for c in neighbors if cell.is_connected(c)]
    return neighbors


def generate_maze(board, current_cell: AStarCell):
    stk = []
    current_cell.visited = True
    stk.append(current_cell)

    while stk:
        current_cell = stk.pop()
        n_cell = get_neighbours(current_cell, board)
        if n_cell:
            stk.append(current_cell)
            n_cell.remove_wall(current_cell)
            n_cell.visited = True
            stk.append(n_cell)

    return board