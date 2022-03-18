from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    @abstractmethod
    def get(self, pk: int):
        raise NotImplemented

    @abstractmethod
    def delete(self, pk: int):
        raise NotImplemented
