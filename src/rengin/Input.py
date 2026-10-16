import pygame #pygame-ce


class Event:
    """General Event Class: Holds the main Event listenera and window updates"""
    Evnt:list

    @staticmethod
    def Update():
        """General Event Updater"""
        Event.Evnt = pygame.event.get()

        Event.WindowEvent.Update()

    EvntList:list[tuple[pygame.event.Event, bool]]

    quitvar:bool = False

    class InputEvent:
        # Finite State Machine Implementation


        def InputListener(self):
            pass

        def InputHandler(self):
            pass

    class WindowEvent:
        """Window Event Class: Holds the window event listener and actual functions"""

        def EventListener(self):
            for event in Event.Evnt:
                match event.type:
                    case pygame.KEYDOWN:
                        if Event.EvntList.find(lambda x: x[0].type == pygame.KEYDOWN and x[0].key == event.key):
                            continue
                        Event.EvntList.append((event, True))
                    case pygame.KEYUP:
                        Event.EvntList.append((event, False))

        @staticmethod
        def Update():
            """Update Window Events"""
            for event in Event.Evnt:
                if event.type == pygame.QUIT:
                    Event.quitvar = True
