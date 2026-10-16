import pygame

class Display:
    """Display Class: Holds functions to draw and manipulate the screen and it's objects"""
    width: int
    height: int
    screen: pygame.Surface

    color: tuple[int, int, int, int]

    ScreenObjects:list

    @staticmethod
    def __init__(width:int, height:int, caption:str):
        pygame.init()

        Display.width = width
        Display.height = height
        Display.screen = pygame.display.set_mode((width, height))
        Display.ScreenObjects = []
        pygame.display.set_caption(caption)

        Display.SetBackgroundColor((90, 90, 90, 255))

    @staticmethod
    def Update():
        """Updates The Screen Surface"""
        Display.DrawBackground()

        Display.DrawObjects()

        pygame.display.flip()

    @staticmethod
    def DrawObjects():
        """Draws Objects from the Screen Object List"""
        try:
            for obj in Display.ScreenObjects:
                obj.Draw()
        except Exception as e:
            print(e)

    @staticmethod
    def GetScreen():
        """Get The Pygame Screen Surface"""
        return Display.screen

    @staticmethod
    def GetWidth():
        """Get The Screen Width"""
        return Display.width

    @staticmethod
    def GetHeight():
        """Get The Screen Height"""
        return Display.height

    @staticmethod
    def GetSize():
        """Get The Screen Area"""
        return (Display.width, Display.height)

    @staticmethod
    def SetSize(width:int, height:int):
        """The only method that modifies the display width and height also updates the screen"""
        Display.width = width
        Display.height = height
        Display.screen = pygame.display.set_mode((width, height))

    @staticmethod
    def SetCaption(caption:str):
        """Set Window Title"""
        pygame.display.set_caption(caption)

    @staticmethod
    def SetBackgroundColor(color:tuple[int, int, int, int]):
        """Set Background Color"""
        Display.color = color

    @staticmethod
    def DrawBackground():
        Display.screen.fill(Display.color)

    @staticmethod
    def SetIcon(icon:pygame.Surface):
        """Set Window Icon"""
        pygame.display.set_icon(icon)
