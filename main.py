import pygame

from src.rengin.Display import Display
from src.rengin.Entity import Rect

def main():
    Display(800, 600, "Rengin")

    from src.rengin.Input import Event

    Event.Init()

    player = Rect("Player", (30, 40, 50, 50), (15, 90, 30, 255))

    player.AddFunc("d", "Move", (0.1, 0.0))
    player.AddFunc("a", "Move", (-0.1, 0.0))
    player.AddFunc("s", "Move", (0.0, 0.1))
    player.AddFunc("w", "Move", (0.0, -0.1))

    while not Event.quitvar:
        Event.Update()

        Display.Update()

        if Event.quitvar:
            break

    pygame.quit()


if __name__ == "__main__":
    main()
