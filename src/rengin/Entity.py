import pygame #pygame-ce

from .Vector import Vector2
from .Display import Display

class Object:
    """Object Class: Base class that adds position vector"""
    x:float = 0.0
    y:float = 0.0

    position:Vector2 = Vector2(x, y)


class Entity(Object):
    """Entity Class: It intherits the Object class and adds Scale vector and functions dictionary"""
    x2:float = 0.0
    y2:float = 0.0

    scale:Vector2 = Vector2(x2, y2)

    funcs:dict

    def AddFunc(self, function:str) -> None:
        """Adds a function to the entity functions dictionary"""
        eval(function, self.funcs)

    def ExcFunc(self, function:str) -> None:
        """Deletes the function from the entity functions dictionary"""
        self.funcs.__delitem__(function)

    def ExecFunc(self, function:str) -> None:
        """Executes a function from the entity functions dictionary"""
        self.funcs[function]()

class Rect(Entity):
    """Rect Class (Entity): Inherits the Entity Class and Bridges to Pygame Rect"""
    Name:str
    RectObj:pygame.rect.FRect
    color:tuple[int, int, int, int]

    def __init__(self, name:str, rectAtt:tuple[float,float,float,float], color:tuple[int, int, int, int]|None):
        self.position = Vector2(rectAtt[0], rectAtt[1])
        self.scale = Vector2(rectAtt[2], rectAtt[3])
        self.Name = name

        self.RectObj = pygame.rect.FRect(self.position.x, self.position.y, self.scale.x, self.scale.y) # Sets the RectObj

        if not color:
            self.color = (255, 255, 255, 255)
        else:
            self.color = color

        self.AddToScreen()

    def __call__(self):
        return self.RectObj

    def AddToScreen(self):
        """Add the Object to the Object Screen List"""
        Display.ScreenObjects.append(self)

    def Move(self, x:float, y:float):
        """Moves the Entity to Direction (Vector2)"""
        self.position += Vector2(x, y)
        self.RectObj.x = self.position.x
        self.RectObj.y = self.position.y

        Display.ScreenObjects[Display.ScreenObjects.index(self)].position = self.position

    def Draw(self):
        """Draws the Entity"""
        pygame.draw.rect(Display.GetScreen(), pygame.Color(self.color[0], self.color[1], self.color[2], self.color[3]), self.RectObj)
