import pygame
from rengin.Entity import Entity #pygame-ce

from .Display import Display

class Event:
    """General Event Class: Holds the main Event listenera and window updates"""

    Initialized:bool = False

    Evnt:list[pygame.event.Event]
    
    @staticmethod
    def Init():
        Event.Initialized = True

    @staticmethod
    def Update():
        """General Event Updater"""

        Event.Evnt = pygame.event.get()

        Event.WindowEvent.Update()

        Event.InputEvent.Update()

        for keys in Event.InputEvent.GetPressedKeys():
            if Event.InputEvent.FiniteStateMachineListDebug is True:
                print(f"Objects in Input Update: {str(Event.InputEvent.ObjectInputUpdate)}")
            for Obj in Event.InputEvent.ObjectInputUpdate:
                if Event.InputEvent.FiniteStateMachineListDebug is True:
                    print("Updating Input for Object: " + str(Obj))
                Obj.UpdateInput()

    quitvar:bool = False

    class InputEvent:
        # Finite State Machine Implementation
        FiniteStateMachineListDebug:bool = False

        ObjectInputUpdate:list[Entity] = []
        InputList:list[tuple[pygame.Event, bool]] = []

        Initialized:bool = False

        @staticmethod
        def GetPressedKeys():
            PressedKeys = []

            for keys in Event.InputEvent.InputList:
                if keys[1] is True:
                    PressedKeys.append(keys)
            return PressedKeys

        @staticmethod
        def IsKeyPressed(key:str):
            pressedKeys = Event.InputEvent.GetPressedKeys()

            for keys in pressedKeys:
                if keys == key:
                    return True
            return False

        @staticmethod
        def Update() -> None:
            for Object in Display.ScreenObjects:
                if Object.GetParentClass().__name__ == "Entity": # Gets the name of the parent class of the object and checks if it is an Entity
                    if Event.InputEvent.FiniteStateMachineListDebug is True:
                        print('Object is an Entity: ' + str(Object))
                    if Object not in Event.InputEvent.ObjectInputUpdate: # if it's not in the list, add it
                        if Event.InputEvent.FiniteStateMachineListDebug is True:
                            print("Adding Object to Input Update: " + str(Object))
                        Event.InputEvent.ObjectInputUpdate.append(Object)

            for event in Event.Evnt:
                match event.type:
                    case pygame.KEYDOWN:
                        for ev in Event.InputEvent.InputList:
                            if ev[0] == event.unicode:
                                Event.InputEvent.InputList[Event.InputEvent.InputList.index(ev)] = (event.unicode, True)
                                break
                        else:
                            Event.InputEvent.InputList.append((event.unicode, True))
                        if Event.InputEvent.FiniteStateMachineListDebug:
                            print("Keys: " + str(Event.InputEvent.InputList))
                    case pygame.KEYUP:
                        for ev in Event.InputEvent.InputList:
                            if ev[0] == event.unicode:
                                Event.InputEvent.InputList[Event.InputEvent.InputList.index(ev)] = (event.unicode, False)
                                if Event.InputEvent.FiniteStateMachineListDebug:
                                    print("Keys: " + str(Event.InputEvent.InputList))
                    case _:
                        pass


    class WindowEvent:
        """Window Event Class: Holds the window event listener and actual functions"""

        QuitInput:str = "q"

        @staticmethod
        def Update():
            """Update Window Events"""
            for event in Event.Evnt:
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.unicode == Event.WindowEvent.QuitInput):
                    Event.quitvar = True

        @staticmethod
        def ChangeQuitInput(new_key:str):
            """Changes the quit input to a different key"""
            Event.WindowEvent.QuitInput = new_key
