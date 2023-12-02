import pickle
import pygame
import time

import board as b
from cell import Cell, AStarCell

pygame.init()

screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()

def import_maze() -> list[list[Cell]]:
    f_path = "maze.dat"

    with open(f_path, "rb") as file:
        board = pickle.load(file)

    return board

def set_board_to_unvisited(board: list[list[Cell]]) -> list[list[Cell]]:
    bo = b.generate_board()
    
    for i in range(len(board)):
        for j in range(len(board)):
            cell = board[i][j]
            cell.visited = False
            bo[i][j] = AStarCell(cell.x, cell.y, cell.width)
            bo[i][j].walls = cell.walls

    return board


def heuristic(cell: AStarCell, end: AStarCell):
    dx = abs(end.x - cell.x)
    dy = abs(end.y - cell.y)
    return dx + dy


def reconstruct_path(current, came_from):
    path = [current]

    while current in came_from:
        current = came_from[current]
        # current.visited = True
        path.insert(0, current)
    
    return path


def astar(draw, board: list[list[AStarCell]]):
    start = board[0][0]
    start.g = 0
    end = board[b.CELLS-1][b.CELLS-1]
    openSet = {start}

    came_from = {}


    while openSet:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()


        current = min(openSet, key=lambda x: x.f)

        if current == end:
            return reconstruct_path(current, came_from)

        path = reconstruct_path(current, came_from)
        draw_path(path)

        openSet.remove(current)
        neighbours = b.get_maze_neighbours(current, board)
        
        for neighbour in neighbours:
            tempG = current.g + 1
            if tempG < neighbour.g:
                came_from[neighbour] = current
                neighbour.g = tempG
                neighbour.f = tempG + heuristic(neighbour, end)
                if neighbour not in openSet:
                    openSet.add(neighbour)
        



board = b.generate_board()
board = b.generate_maze(board, board[0][0])
board = set_board_to_unvisited(board)

path = []

def draw_path(path, color=(125, 125, 125)):
    clock.tick(100)
    if path:
        for cell1, cell2 in zip(path[:-1], path[1:]):
            x1, x2, y1, y2 = cell1.x, cell2.x, cell1.y, cell2.y
            w = cell1.width

            pygame.draw.line(screen, color, (x1+w//2, y1+w//2), (x2+w//2, y2+w//2), 10)

    pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                board = b.generate_board()
                board = b.generate_maze(board, board[0][0])
                path = []
            if event.key == pygame.K_RETURN and not path:
                path = astar(lambda: b.draw(screen, board), board)

    b.draw(screen, board)
    draw_path(path, (100, 100, 255))

    clock.tick(24)
    pygame.display.flip()

if __name__ == "__main__":
    import_maze()