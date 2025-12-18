import pygame
import os

def play_background_music(volume=0.5):
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    bgm_path = os.path.join(
        base_dir,
        "assets",
        "audio",
        "bgm",
        "background theme.mp3"
    )

    pygame.mixer.music.load(bgm_path)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1)  # -1 = loop selamanya
