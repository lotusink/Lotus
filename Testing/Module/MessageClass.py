from abc import ABC, abstractmethod

class Message(ABC):

    @abstractmethod
    def get_value(self):
        """
        Get the value of the class object.
        """
        pass

    @abstractmethod
    def set_value(self):
        """
        Set the value of the class object
        """
        pass