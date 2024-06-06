import sys
import pygame
from interfaces.observer_interface import IObserver, IObservable

class EventHandler(IObservable):
    """Class to handle events."""

    def __init__(self):
        self.__observers = []

    def attach(self, observer: IObserver):
        """Add observer to the list of observers."""
        if observer not in self.__observers:
            self.__observers.append(observer)

    def dettach(self, observer: IObserver):
        """Remove observer from the list of observers."""
        if observer in self.__observers:
            self.__observers.remove(observer)

    def notify(self, event):
        """Notify all observers of an event."""
        self.__observers[-1].update(event=event)

    def handle_events(self):
        """Handle Pygame events and notify observers."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            self.notify(event)
