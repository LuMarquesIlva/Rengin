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
    player2 = Rect("Player2", (200, 200, 80, 80), (255, 50, 0, 255))

    player.SetFrames([
        LoadImage(f"{DefaultAssetsDir}/Images/Materials/TilePlaceholder/R_TileMaterial.png"),
        LoadImage(f"{DefaultAssetsDir}/Images/Materials/TilePlaceholder/N_TileMaterial.png"),
        LoadImage(f"{DefaultAssetsDir}/Images/Materials/TilePlaceholder/A_TileMaterial.png")
    ])

    player.AddFunc("d", "Move", (0.1, 0.0))
    player.AddFunc("a", "Move", (-0.1, 0.0))
    player.AddFunc("s", "Move", (0.0, 0.1))
    player.AddFunc("w", "Move", (0.0, -0.1))

    player.AddFunc("f", "SetScale", (0.1, 0.1))
    player.AddFunc("1", "SetCurrentFrame", (2,))

    while not Event.quitvar:
        Event.Update()

        Display.Update()

        if Event.quitvar:
            break

    pygame.quit()


if __name__ == "__main__":
    main()
