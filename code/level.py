from operator import truediv
import pygame
from tiles import Tile, Board
from settings import tile_size


class Level:
    def __init__(self, display_surface, board_dimensions, tiles_map, exit_point):

        self.display_surface = display_surface

        self.selected_tile = None

        # keyboard input
        self.delay = 400
        self.allow_keyboard_input = True
        self.last_key_timer = pygame.time.get_ticks()

        # make board borders
        border_thickness = 20
        self.board = pygame.sprite.GroupSingle()
        self.board.add(Board(border_thickness, board_dimensions))

        # tiles placement
        self.tiles = pygame.sprite.Group()
        for w, h, x, y, goal in tiles_map:
            tile = Tile(w, h, x, y, goal)
            self.tiles.add(tile)

        # exit point
        self.exit_point = (
            border_thickness + exit_point[0] * tile_size,
            border_thickness + exit_point[1] * tile_size
            )

        # offset all tiles and exit_point
        for tile in self.tiles.sprites():
            tile.offset(border_thickness,border_thickness)

    def input(self):
        # mouse selection
        button1, _button2, button3 = pygame.mouse.get_pressed()
        if button1:
            click_pos = pygame.mouse.get_pos()
            for tile in self.tiles.sprites():
                if tile.rect.collidepoint(click_pos):
                    self.selected_tile = tile
        if button3:
            self.selected_tile = None

        # keyboard mouvement
        if not self.allow_keyboard_input:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_key_timer >= self.delay:
                self.last_key_timer = pygame.time.get_ticks()
                self.allow_keyboard_input = True

        keys = pygame.key.get_pressed()
        if self.selected_tile and self.allow_keyboard_input:
            moved = False
            if keys[pygame.K_UP]:
                move_dir = 'up'
                moved = True
            elif keys[pygame.K_DOWN]:
                move_dir = 'down'
                moved = True
            elif keys[pygame.K_LEFT]:
                move_dir = 'left'
                moved = True
            elif keys[pygame.K_RIGHT]:
                move_dir = 'right'
                moved = True

            if moved:
                self.move_selected_tile(move_dir)
                self.allow_keyboard_input = False
                self.last_key_timer = pygame.time.get_ticks()

    def move_selected_tile(self, dir):
        x, y = self.transform_dir(dir)
        if self.check_move(dir):
            self.selected_tile.rect.move_ip(x, y)

    def check_move(self, dir):
        
        x, y = self.transform_dir(dir)

        can_move = True

        # board collision
        if self.selected_tile.goal_tile:
            walls = self.board.sprite.collision_rects
        else:
            walls = self.board.sprite.collision_rects + [self.board.sprite.exit_rect]

        if self.selected_tile.rect.move(x, y).collidelist(walls) != -1:
            can_move = False

        # tiles collision
        next_tile_pos = self.selected_tile.rect.move(x, y)
        tile_rect_list = [sprite.rect for sprite in self.tiles.sprites()]
        tile_rect_list.remove(self.selected_tile.rect)
        if next_tile_pos.collidelist(tile_rect_list) != -1:
            can_move = False

        return can_move

    def transform_dir(self, dir):
        if dir == 'up':
            x = 0
            y = -1
        elif dir == 'down':
            x = 0
            y = 1
        elif dir == 'left':
            x = -1
            y = 0
        elif dir == 'right':
            x = 1
            y = 0

        x = x * tile_size
        y = y * tile_size
                
        return x, y

    def check_win(self):
        for tile in self.tiles.sprites():
            if tile.goal_tile is True:
                if tile.rect.topleft == self.exit_point:

                    print('WON')

    # DEBUG
    def display_exit_point(self, color='green'):
        pygame.draw.circle(self.display_surface, color, self.exit_point, 5)
    def display_walls(self, color='red'):
        for rect in self.board.sprite.collision_rects:
            pygame.draw.rect(self.display_surface, color, rect)

    def run(self):

        self.board.draw(self.display_surface)
        self.tiles.draw(self.display_surface)

        self.input()
        self.check_win()