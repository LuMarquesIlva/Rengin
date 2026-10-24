from sys import argv

import pygame #pygame-ce
from PIL import Image

from .Vector import Vector2
from .Display import Display

def LoadImage(path:str) -> pygame.surface.Surface|None:
    """Loads an Image and returns a Pygame Surface"""
    try:
        image = pygame.image.load(path)
        return image
    except Exception as e:
        print(f"Error loading image: {path} - {e}")
        return None
    

class Object:
    """Object Class: Base class that adds position vector"""
    x:float = 0.0
    y:float = 0.0

    position:Vector2 = Vector2(x, y)


class Entity(Object):
    """Entity Class: It intherits the Object class and adds Scale vector and functions dictionary"""
    x2:float = 0.0
    y2:float = 0.0

    EntDebug:bool = False
    EntityInputDebug:bool = False

    scale:Vector2 = Vector2(x2, y2)

    funcs:dict[str, tuple[str, tuple]] = {}

    def UpdateInput(self):
        """Updates The Entity Input"""
        from .Input import Event
        PressedKeys = Event.InputEvent.GetPressedKeys()

        for keys in PressedKeys:
            for func in self.funcs:
                if self.EntityInputDebug is True:
                    print(f"Executing function for key: {keys[0]}")
                self.ExecFunc(keys[0])

    def IsFuncExecuting(self, key:str) -> bool:
        """Checks if the function is executing for the given key"""
        from .Input import Event
        PressedKeys = Event.InputEvent.GetPressedKeys()

        for keys in PressedKeys:
            if keys[0] == key:
                return True
        return False

    def AddFunc(self, key:str, functionName:str, functionArgs:tuple) -> None:
        """Adds a function to the entity functions dictionary"""
        self.funcs[key] = (functionName, functionArgs)
        if self.EntDebug is True:
            print(f"Linked function: '{functionName}({functionArgs[0]}, {functionArgs[1]})' >> '{key}'")

    def DelFunc(self, key:str) -> None:
        """Deletes the function from the entity functions dictionary"""
        self.funcs.__delitem__(key)

    def ExecFunc(self, key:str) -> None:
        """Executes a function from the entity functions dictionary"""

        try:
            functionName, functionArgs = self.funcs[key]
        except KeyError:
            if self.EntDebug is True:
                print(f"Function not found for key: {key}")
            return

        if self.EntDebug is True:
            print(f"Current Function: self.{functionName}({functionArgs[0]}, {functionArgs[1]})")
        ev = eval(f"self.{functionName}({functionArgs[0]}, {functionArgs[1]})")


class Rect(Entity):
    """Rect Class (Entity): Inherits the Entity Class and Bridges to Pygame Rect"""
    Name:str
    RectObj:pygame.rect.FRect
    color:tuple[int, int, int, int]|pygame.surface.Surface

    def __init__(self, name:str, rectAtt:tuple[float,float,float,float], color:tuple[int, int, int, int]|pygame.surface.Surface|None):
        super().__init__()
        self.position = Vector2(rectAtt[0], rectAtt[1])
        self.scale = Vector2(rectAtt[2], rectAtt[3])
        self.Name = name

        self.RectObj = pygame.rect.FRect(self.position.x, self.position.y, self.scale.x, self.scale.y) # Sets the RectObj

        if not color:
            self.color = (255, 255, 255, 255)
        elif isinstance(color, pygame.surface.Surface):
            if color.get_size() != (self.scale.x, self.scale.y):
                color = pygame.transform.scale(color, (int(self.scale.x), int(self.scale.y)))
            self.color = color.convert_alpha()
        else:
            self.color = color

        self.AddToScreen()

    def __call__(self):
        return self.RectObj

    def GetParentClass(self) -> type:
        """Returns the Parent Class of the Object"""
        return self.__class__.__bases__[0]

    def UpdateInput(self):
        super().UpdateInput()

    def AddToScreen(self):
        """Add the Object to the Object Screen List"""
        Display.ScreenObjects.append(self)

    def Move(self, x:float, y:float):
        """Moves the Entity to Direction (Vector2)"""
        self.position += Vector2(x, y)
        self.RectObj.x = self.position.x
        self.RectObj.y = self.position.y

        Display.ScreenObjects[Display.ScreenObjects.index(self)].position = self.position
        if self.EntDebug is True:
            return "Moved to: " + str(self.position)

    def Draw(self):
        """Draws the Entity"""
        if isinstance(self.color, pygame.surface.Surface):
            Display.GetScreen().blit(self.color, self.RectObj)
        else:
            pygame.draw.rect(Display.GetScreen(), pygame.Color(self.color[0], self.color[1], self.color[2], self.color[3]), self.RectObj)
