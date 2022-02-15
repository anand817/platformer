from enum import Enum
import pygame
from pygame.sprite import Sprite

from platformer.config.constants import GRAVITY, SCREEN_WIDTH


# Enum for states of the player
class playerState(Enum):
    walking = "walk"
    jumping = "jump"
    standing = "stand"


class Player(Sprite):

    def __init__(self) -> None:
        super().__init__()

        # player state
        self.state = playerState.standing

        # player assets
        from ..config.assets import player_standing, player_jumping, player_walking
        self.player_standing = player_standing
        self.player_walking = player_walking
        self.player_jumping = player_jumping

        # player dynamic
        self.walking_index = 0
        self.speed_x = 0
        self.speed_y = 0
        self.gravity = GRAVITY
        self.direction = 1  # can be only 1 or -1
        self.x = 300
        self.y = 300

        # player rendering
        self.image = self.player_standing
        self.rect = self.image.get_rect()

    def draw(self):
        screen = pygame.display.get_surface()
        screen.blit(self.image, (self.x, self.y))

    def update(self):

        # functions definition for different state
        def update_standing():
            self.image = self.player_standing

        def update_walking():

            if (self.direction == 1 and self.x > SCREEN_WIDTH - 70*5) or (self.direction == -1 and self.x < 70*5):
                pass
            else:
                self.x += self.speed_x*self.direction

            self.walking_index = (self.walking_index +
                                  1) % len(self.player_walking)
            self.image = self.player_walking[self.walking_index]

        def update_jumping():
            self.image = self.player_jumping
            if (self.direction != 1 or self.x < SCREEN_WIDTH - 70*5) and (self.direction != -1 and self.x > 70*5):
                pass
            else:
                self.x += self.speed_x*self.direction
            self.y -= self.speed_y
            self.speed_y -= self.gravity
            if self.y == 300:
                self.state = playerState.standing

        # calling functions in different state
        if(self.state == playerState.standing):
            update_standing()

        elif (self.state == playerState.walking):
            update_walking()

        elif (self.state == playerState.jumping):
            update_jumping()

        self.image = pygame.transform.flip(
            self.image, self.direction == -1, 0)
        self.rect = self.image.get_rect()

    def stop(self):
        if self.state != playerState.jumping:
            self.speed_x = 0
            self.state = playerState.standing

    def walk(self, direction):
        if self.state != playerState.jumping:
            self.direction = direction
            if self.speed_x < 25:
                self.speed_x += 10
            self.state = playerState.walking

    def jump(self):
        if self.state != playerState.jumping:
            self.speed_y = 20
            self.state = playerState.jumping
