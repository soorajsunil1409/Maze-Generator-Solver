import pygame
import pickle
import board as b

from cell import Cell


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((b.WIDTH, b.WIDTH))



def generate_maze(draw, current_cell: Cell):
    global board
    stk = []
    current_cell.visited = True
    stk.append(current_cell)

    while stk:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    board = b.generate_board()
                    return

        current_cell = stk.pop()
        n_cell = b.get_neighbours(current_cell, board)
        if n_cell:
            stk.append(current_cell)
            n_cell.remove_wall(current_cell)
            n_cell.visited = True
            stk.append(n_cell)
        draw()


def export_maze():
    with open("maze.dat", "wb") as file:
        pickle.dump(board, file)
        file.flush()

board = b.generate_board()
starting_cell = board[0][0]


while True:
    b.draw(screen, board)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                board = b.generate_board()
                generate_maze(lambda: b.draw(screen, board), starting_cell)
            if event.key == pygame.K_c:
                board = b.generate_board()
            if event.key == pygame.K_e:
                export_maze()

    clock.tick(100)
    pygame.display.flip()

