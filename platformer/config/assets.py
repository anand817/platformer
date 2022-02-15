from typing import List, Optional
from pygame import Surface
from pygame.image import load
from os import listdir, path
from .constants import JUMPING, STATIC, WALKING

player_walking: List[Surface] = []
player_jumping: Optional[Surface] = None
player_standing: Optional[Surface] = None


def init_assets():
    global player_jumping, player_standing, player_walking

    for i in range(1, 3):
        player_walking.append(
            load(f'{WALKING}{i}.png').convert_alpha()
        )

    player_jumping = load(JUMPING).convert_alpha()

    player_standing = load(STATIC).convert_alpha()
