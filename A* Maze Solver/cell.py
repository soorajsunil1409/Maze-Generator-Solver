import pygame

class Cell:
    def __init__(self, x, y, width) -> None:
        self.walls              = [1, 1, 1, 1]                  # left right top bottom
        self.width              = width
        self.x                  = x * self.width
        self.y                  = y * self.width
        self.unvisited_color    = 255, 255, 255
        self.visited_color      = 255, 255, 255
        self.visited            = False
        self.line_width         = 1

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.unvisited_color if not self.visited else self.visited_color, (self.x, self.y, self.width, self.width))
        if self.walls[0]: pygame.draw.line(screen, (0, 0, 0), (self.x, self.y), (self.x, self.y+self.width), self.line_width)
        if self.walls[1]: pygame.draw.line(screen, (0, 0, 0), (self.x+self.width, self.y), (self.x+self.width, self.y+self.width), self.line_width)
        if self.walls[2]: pygame.draw.line(screen, (0, 0, 0), (self.x, self.y), (self.x+self.width, self.y), self.line_width)
        if self.walls[3]: pygame.draw.line(screen, (0, 0, 0), (self.x, self.y+self.width), (self.x+self.width, self.y+self.width), self.line_width)

    def get_grid_coords(self):
        return self.x // self.width, self.y // self.width
    
    def remove_wall(self, adjacent_cell):
        xdiff = self.get_grid_coords()[0] - adjacent_cell.get_grid_coords()[0]
        ydiff = self.get_grid_coords()[1] - adjacent_cell.get_grid_coords()[1]
        
        if xdiff == -1:
            self.walls[1] = 0
            adjacent_cell.walls[0] = 0
        elif xdiff == 1:
            self.walls[0] = 0
            adjacent_cell.walls[1] = 0

        if ydiff == -1:
            self.walls[3] = 0
            adjacent_cell.walls[2] = 0
        elif ydiff == 1:
            self.walls[2] = 0
            adjacent_cell.walls[3] = 0



class AStarCell(Cell):
    def __init__(self, x, y, width) -> None:
        self.g = 99999999
        self.h = 0
        self.f = 0
        self.previous = None

        super().__init__(x, y, width)

    def is_connected(self, other) -> bool:
        xdiff = self.get_grid_coords()[0] - other.get_grid_coords()[0]
        ydiff = self.get_grid_coords()[1] - other.get_grid_coords()[1]

        if xdiff == -1:
            return self.walls[1] == 0 and other.walls[0] == 0
        elif xdiff == 1:
            return self.walls[0] == 0 and other.walls[1] == 0

        if ydiff == -1:
            return self.walls[3] == 0 and other.walls[2] == 0
        elif ydiff == 1:
            return self.walls[2] == 0 and other.walls[3] == 0