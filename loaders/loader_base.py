from abc import ABC, abstractmethod


class LoaderBase(ABC):
    @abstractmethod
    def method(self):
        return None
