import time
from typing import Tuple
import pygame
from .config.constants import SCREEN_HEIGHT, SCREEN_WIDTH, SIZE
from .config.assets import init_assets
from .sprites.player import Player
from pytmx.util_pygame import load_pygame
import pytmx

clock: pygame.time.Clock
tilemap: pytmx.TiledMap


class TiledMap:
    def __init__(self, filename):
        tm = load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        tile = pygame.transform.smoothscale(
                            tile, (70, 70))
                        surface.blit(
                            tile, (x * 70, y * 70))

    def make_map(self):
        temp_surface = pygame.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface


def pygame_init():
    global clock, tilemap
    pygame.init()
    pygame.display.set_caption("Platformer")
    pygame.display.set_mode(SIZE)
    init_assets()
    clock = pygame.time.Clock()
    tilemap = TiledMap('platformer/assets/levels/level_01.tmx').make_map()

# paint background


def fill_bg(world_offset):
    screen = pygame.display.get_surface()
    screen.fill((0, 0, 0))
    screen.blit(tilemap, world_offset)


if __name__ == "__main__":
    pygame_init()
    running = True
    player = Player()
    world_offset: Tuple[int, int] = (0, SCREEN_HEIGHT + (-50*70))
    while running:
        clock.tick(25)
        fill_bg(world_offset)
        player.draw()
        player.update()
        if player.x > (SCREEN_WIDTH - 70*5):
            world_offset = (world_offset[0] - player.speed_x, world_offset[1])
        if player.x < (70*5):
            world_offset = (world_offset[0] + player.speed_x, world_offset[1])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:

                if event.key in [pygame.K_RIGHT, pygame.K_d]:
                    player.walk(1)

                if event.key in [pygame.K_LEFT, pygame.K_a]:
                    player.walk(-1)

                if event.key in [pygame.K_UP, pygame.K_w]:
                    player.jump()

            elif event.type == pygame.KEYUP:
                player.stop()

        pygame.display.flip()
