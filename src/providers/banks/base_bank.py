from abc import ABC, abstractmethod

class BaseBank(ABC):
    @abstractmethod
    def get_balance(self) -> float:
        pass
