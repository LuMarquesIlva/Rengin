import pygame

from src.rengin.Display import Display
from src.rengin.Entity import Rect, LoadImage

DefaultAssetsDir = "src/rengin/Assets"

def main():
    Display(800, 600, "Rengin")

    from src.rengin.Input import Event

    Event.Init()

    tile_material = LoadImage(f"{DefaultAssetsDir}/Images/Materials/TilePlaceholder/R_TileMaterial.png")

    player = Rect("Player", (30, 40, 80, 80), tile_material)
    player2 = Rect("Player2", (200, 200, 80, 80), (255, 0, 0, 255))

    

    player.AddFunc("d", "Move", (0.1, 0.0))
    player.AddFunc("a", "Move", (-0.1, 0.0))
    player.AddFunc("s", "Move", (0.0, 0.1))
    player.AddFunc("w", "Move", (0.0, -0.1))

    #TODO: Fix the AddFunc method to work with player2, currently it doesn't work because of the way the function is defined in the Entity class,
    # every object of the same class shares the same dictionary of functions, so when you add a function to one object, it will be added to all objects of that class.

    print(player2.funcs)

    while not Event.quitvar:
        Event.Update()

        Display.Update()

        if Event.quitvar:
            break

    pygame.quit()


if __name__ == "__main__":
    main()
