from abc import ABC, abstractmethod


class BaseRisk(ABC):
    @abstractmethod
    def get_risk(self) -> dict:
        pass
