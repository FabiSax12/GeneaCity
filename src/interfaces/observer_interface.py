from abc import ABC, abstractmethod

class IObserver(ABC):
    @abstractmethod
    def update(self, *args, **kwargs):
        pass

class IObservable(ABC):
    @abstractmethod
    def attach(self, observer: IObserver):
        pass

    @abstractmethod
    def dettach(self, observer: IObserver):
        pass

    @abstractmethod
    def notify(self):
        pass