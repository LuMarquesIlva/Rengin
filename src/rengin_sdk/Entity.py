from sys import argv

import pygame #pygame-ce
from PIL import Image

from .Vector import Vector2
from .Display import Display

from typing import overload

def LoadImage(path:str) -> pygame.surface.Surface|None:
    """Loads an Image and returns a Pygame Surface"""
    try:
        image = pygame.image.load(path)
        return image
    except Exception as e:
        print(f"Error loading image: {path} - {e}")
        return None

class Animation:
    Frames:list[pygame.surface.Surface]
    FrameDuration:float
    CurrentFrameIndex:int
    TimeSinceLastFrame:float

    def __init__(self, frames:list[pygame.surface.Surface], frame_duration:float):
        self.Frames = frames
        self.FrameDuration = frame_duration
        self.CurrentFrameIndex = 0
        self.TimeSinceLastFrame = 0.0

    def Update(self, delta_time:float):
        self.TimeSinceLastFrame += delta_time
        if self.TimeSinceLastFrame >= self.FrameDuration:
            self.CurrentFrameIndex = (self.CurrentFrameIndex + 1) % len(self.Frames)
            self.TimeSinceLastFrame = 0.0

    def GetCurrentFrame(self) -> pygame.surface.Surface:
        return self.Frames[self.CurrentFrameIndex]

    def Reset(self):
        self.CurrentFrameIndex = 0
        self.TimeSinceLastFrame = 0.0

    def SetFrameDuration(self, frame_duration:float):
        self.FrameDuration = frame_duration

    def SetFrames(self, frames:list[pygame.surface.Surface|None]):
        if not frames:
            raise ValueError("Frames list cannot be empty")
        
        self.Frames = frames
        self.CurrentFrameIndex = 0
        self.TimeSinceLastFrame = 0.0

    def GetFrameDuration(self) -> float:
        return self.FrameDuration

    def GetFrames(self) -> list[pygame.surface.Surface]:
        return self.Frames

    def GetCurrentFrameIndex(self) -> int:
        return self.CurrentFrameIndex

    def GetTimeSinceLastFrame(self) -> float:
        return self.TimeSinceLastFrame

    def SetCurrentFrameIndex(self, index:int):
        if 0 <= index < len(self.Frames):
            self.CurrentFrameIndex = index
            self.TimeSinceLastFrame = 0.0
        else:
            raise IndexError("Frame index out of range")

    def SetCurrentFrame(self, frame:int):
        if 0 <= frame < len(self.Frames):
            self.SetCurrentFrameIndex(frame)
            self.SetColor(self.Frames[frame])
        else:
            print(f"Frame not found in frames list: {self.Frames}")
            raise ValueError("Frame not found in frames list")

class Object:
    """Object Class: Base class that adds position vector"""
    x:float = 0.0
    y:float = 0.0

    position:Vector2 = Vector2(x, y)


class Entity(Object, Animation):
    """Entity Class: It intherits the Object class and adds Scale vector and functions dictionary"""
    x2:float = 0.0
    y2:float = 0.0

    angle:float = 0.0

    EntDebug:bool = False
    EntityInputDebug:bool = False

    scale:Vector2 = Vector2(x2, y2)
    rotation:float = 0.0

    funcs:dict[str, tuple[str, tuple]]

    Name:str

    def __init__(self):
        super().__init__([], 1.0)

        self.funcs = {} # Declares the funcs dict here so it does not get shared between instances of the Entity class
        self.position = Vector2(self.x, self.y)
        self.scale = Vector2(self.x2, self.y2)

    def UpdateInput(self):
        """Updates The Entity Input"""
        from .Input import Event
        PressedKeys = Event.InputEvent.GetAllPressedKeys()

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

        if not hasattr(self, functionName):
            if self.EntDebug is True:
                print(f"Function '{functionName}' not found in Entity class")
            return

        # Execute the function with the provided arguments while handling the case where functionArgs is not a tuple
        if not isinstance(functionArgs, tuple):
            eval(f"self.{functionName}({functionArgs})")
        else:
            if len(functionArgs) == 1:
                eval(f"self.{functionName}({functionArgs[0]})")
            elif len(functionArgs) == 2:
                eval(f"self.{functionName}({functionArgs[0]}, {functionArgs[1]})")

    def AddToScreen(self):
        """Add the Object to the Object Screen List"""
        Display.ScreenObjects.append(self)

    def GetParentClass(self) -> type:
        """Returns the Parent Class of the Object"""
        return self.__class__.__bases__[0]

    def SetColor(self, color:tuple[int, int, int, int]|pygame.surface.Surface):
        """Sets the Entity Color"""
        if isinstance(color, pygame.surface.Surface):
            if color.get_size() != (self.scale.x, self.scale.y):
                color = pygame.transform.scale(color, (int(self.scale.x), int(self.scale.y)))
            self.color = color.convert_alpha()
        else:
            self.color = color

    def GetColor(self) -> pygame.color.Color|pygame.surface.Surface:
        if not isinstance(self.color, pygame.surface.Surface):
            return pygame.color.Color(self.color[0], self.color[1], self.color[2], self.color[3])
        else:
            return self.color
    
    def GetColorValue(self) -> tuple[int, int, int, int]:
        if not isinstance(self.color, pygame.surface.Surface):
            return self.color
        else:
            return (255, 255, 255, 255)


class Rect(Entity):
    """Rect Class (Entity): Inherits the Entity Class and Bridges to Pygame Rect"""
    RectObj:pygame.rect.FRect

    color:tuple[int, int, int, int] | pygame.surface.Surface

    def __init__(self, name:str, rectAtt:tuple[float,float,float,float], color:tuple[int, int, int, int]|pygame.surface.Surface|None):
        super().__init__()
        self.color = (255, 255, 255, 255)
        if not isinstance(color, pygame.surface.Surface):
            self.color = color
        elif isinstance(color, pygame.surface.Surface):
            if color.get_size() != (self.scale.x, self.scale.y):
                color = pygame.transform.scale(color, (int(self.scale.x), int(self.scale.y)))
                self.color = color.convert_alpha()
        else:
            self.color = color

        self.position = Vector2(rectAtt[0], rectAtt[1])
        self.scale = Vector2(rectAtt[2], rectAtt[3])
        self.Name = name

        self.RectObj = pygame.rect.FRect(self.position.x, self.position.y, self.scale.x, self.scale.y) # Sets the RectObj

        self.AddToScreen()

    def __call__(self):
        return self.RectObj    

    def UpdateInput(self):
        super().UpdateInput()

    def Move(self, x:float, y:float):
        """Moves the Entity to Direction (Vector2)"""
        self.position += Vector2(x, y)
        self.RectObj.x = self.position.x
        self.RectObj.y = self.position.y

        Display.ScreenObjects[Display.ScreenObjects.index(self)].position = self.position
        if self.EntDebug is True:
            return "Moved to: " + str(self.position)

    def Scale(self, x:float, y:float):
        """Scales the Entity to Direction (Vector2)"""
        self.scale += Vector2(x, y)
        self.RectObj.width = self.scale.x
        self.RectObj.height = self.scale.y

        Display.ScreenObjects[Display.ScreenObjects.index(self)].scale = self.scale
        if self.EntDebug is True:
            return "Scaled to: " + str(self.scale)

    def SetScale(self, x:float, y:float):
        """Sets the Entity Scale to Direction (Vector2)"""
        self.scale = Vector2(x, y)
        self.RectObj.width = self.scale.x
        self.RectObj.height = self.scale.y

        print(self.RectObj)

        Display.ScreenObjects[Display.ScreenObjects.index(self)].RectObj.width = self.RectObj.width
        Display.ScreenObjects[Display.ScreenObjects.index(self)].RectObj.height = self.RectObj.height
        if self.EntDebug is True:
            return "Scale Set to: " + str(self.scale)

    def SetPosition(self, x:float, y:float):
        """Sets the Entity Position to Direction (Vector2)"""
        self.position = Vector2(x, y)
        self.RectObj.x = self.position.x
        self.RectObj.y = self.position.y

        Display.ScreenObjects[Display.ScreenObjects.index(self)].position = self.position
        if self.EntDebug is True:
            return "Position Set to: " + str(self.position)

    def Draw(self):
        """Draws the Entity"""
        if isinstance(self.color, pygame.surface.Surface):
            Display.GetScreen().blit(self.color, self.RectObj)
        else:
            pygame.draw.rect(Display.GetScreen(), pygame.Color(self.color[0], self.color[1], self.color[2], self.color[3]), self.RectObj)


class Line(Entity):

    width:int
    color:tuple[int, int, int, int]

    def __init__(self, name:str, posX:float, posY:float, posX2:float, posY2:float, width:int, color:tuple[int, int, int, int]|None):
        super().__init__()
        if not color == None:
            self.color = color
        else:
            self.color = (255, 255, 255, 255)
        self.width = width

        self.x, self.y = posX, posY
        self.position = Vector2(self.x, self.y)

        self.x2, self.y2 = posX2, posY2
        self.scale = Vector2(self.x2, self.y2)

        self.Name = name

        self.funcs = {}

        self.AddToScreen()

    def Draw(self):
        pygame.draw.line(Display.GetScreen(), self.GetColor(), (self.x, self.y), (self.x2, self.y2), self.width)
