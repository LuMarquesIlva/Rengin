import pygame

from .Display import Display
from .Entity import Rect

def main():
    Display(800, 600, "Rengin")

    from .Input import Event

    player = Rect("Player", (30, 40, 50, 50), (15, 90, 30, 255))

    while not Event.quitvar:
        Event.Update()

        player.Move(0.1, 0.1)

        Display.Update()

        if Event.quitvar:
            break

    pygame.quit()


if __name__ == "__main__":
    main()
