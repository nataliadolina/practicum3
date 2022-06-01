import pygame

field_length = 300
screen_size_x, screen_size_y = 700, 700
size = screen_size_x, screen_size_y
fps = 10

num_cells = 10
middle_x_cell = num_cells / 2
default_size_y = screen_size_y / num_cells
default_size_x = screen_size_x / num_cells

obstacles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
safe_area_group = pygame.sprite.Group()

LemonChiffon1 = (255, 250, 205)
LemonChiffon3 = (205, 201, 165)
IndianRed = (205, 92, 92)


class GameObjectArgs:
    # num_center_cell_x, num_center_cell_y - в какой клетке находится центр объекта, отсчёт клеток начинается с 0
    # size_cell_x - длина объекта в клетках
    # speed_cell - сколько клеток проходит объект за один фрейм, по умолчанию 0
    def __init__(self, num_center_cell_x, num_center_cell_y, size_cell_x, speed_cell=0.0):
        self.num_center_cell_x = num_center_cell_x
        self.num_center_cell_y = num_center_cell_y
        self.size_cell_x = size_cell_x
        self.speed_cell = speed_cell

        self.row = self.count_center_row_in_pixels(num_center_cell_x)
        self.col = self.count_center_col_in_pixels(num_center_cell_y)
        self.size_x = self.count_size_x_in_pixels(size_cell_x)
        self.speed_x = self.count_speed_x_in_pixels_per_frame(speed_cell)

    def count_center_row_in_pixels(self, num_center_cell_x):
        return num_center_cell_x * default_size_x

    def count_center_col_in_pixels(self, num_center_cell_y):
        return num_center_cell_y * default_size_y

    def count_size_x_in_pixels(self, size_cell_x):
        return size_cell_x * default_size_x

    def count_speed_x_in_pixels_per_frame(self, speed_cell):
        return default_size_x * speed_cell / fps

    def row(self):
        return self.row

    def col(self):
        return self.col

    def size_x(self):
        return self.size_x

    def speed_x(self):
        return self.speed_x


class BaseSprite(pygame.sprite.Sprite):
    def __init__(self, screen, game_object_args: GameObjectArgs, color):
        super().__init__()
        row, col, size_x, speed_x = game_object_args.row, game_object_args.col, game_object_args.size_x, game_object_args.speed_x

        self.col = col
        self.row = row
        self.size_x = size_x
        self.speed_x = speed_x

        self.pos = row, col
        self.image = pygame.Surface((size_x, default_size_y))
        self.rect = pygame.Rect(row, col, size_x, default_size_y)
        self.vel = 0
        self.game_area = screen
        self.image.fill(pygame.Color(color))

    def remove_game_object(self):
        self.kill()


class SafeRow(BaseSprite):
    def __init__(self, screen, game_object_args: GameObjectArgs):
        super().__init__(screen, game_object_args, LemonChiffon3)
        safe_area_group.add(self)


class Obstacle(BaseSprite):
    def __init__(self, screen, game_object_args: GameObjectArgs):
        super().__init__(screen, game_object_args, LemonChiffon1)
        obstacles_group.add(self)

    def update_position(self, row):
        self.pos = row, self.col
        self.row = row
        self.rect = pygame.Rect(row, self.col, self.size_x, default_size_y)

    def update(self):
        row = self.row + self.speed_x
        right_border_position_x = row + self.size_x
        if row > screen_size_x:
            row = 0
        self.update_position(row)


def generate_level(screen):
    return [{0: [SafeRow(screen, GameObjectArgs(0, 0, num_cells))]}, {
        1: [Obstacle(screen, GameObjectArgs(num_center_cell_x=1, num_center_cell_y=1, size_cell_x=1, speed_cell=1)),
            Obstacle(screen, GameObjectArgs(3, 1, 0.5, 1)), Obstacle(screen, GameObjectArgs(5, 1, 1, 1)),
            Obstacle(screen, GameObjectArgs(7, 1, 0.5, 1))]},
            {2: [Obstacle(screen, GameObjectArgs(1, 2, 3, 0.5)), Obstacle(screen, GameObjectArgs(7, 2, 3, 0.5))]},
            {3: [SafeRow(screen, GameObjectArgs(0, 3, num_cells))]}, {4: [
            Obstacle(screen, GameObjectArgs(num_center_cell_x=1, num_center_cell_y=4, size_cell_x=1, speed_cell=1.5)),
            Obstacle(screen, GameObjectArgs(3, 4, 1, 1.5)), Obstacle(screen, GameObjectArgs(5, 4, 1, 1.5))]},
            {5: [Obstacle(screen, GameObjectArgs(1, 5, 3, 0.5)), Obstacle(screen, GameObjectArgs(6, 5, 1, 0.5))]},
            {6: Obstacle(screen, GameObjectArgs(5, 6, 3, 2))}, {7: [SafeRow(screen, GameObjectArgs(0, 7, num_cells))]},
            {8: [
                Obstacle(screen, GameObjectArgs(num_center_cell_x=1, num_center_cell_y=8, size_cell_x=1, speed_cell=1)),
                Obstacle(screen, GameObjectArgs(5, 8, 1, 1))]}, {9: [SafeRow(screen, GameObjectArgs(0, 9, num_cells))]}]


def update_groups(screen):
    safe_area_group.draw(screen)

    obstacles_group.draw(screen)
    obstacles_group.update()


def launch():
    screen = pygame.display.set_mode(size)
    screen.fill((0, 0, 0))

    generate_level(screen)
    clock = pygame.time.Clock()

    while True:
        screen.fill(0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                quit()

        update_groups(screen)
        clock.tick(fps)
        pygame.display.flip()


launch()
