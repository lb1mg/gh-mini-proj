from abc import ABC, abstractmethod

class BaseListener(ABC):
    
    @classmethod
    @abstractmethod
    async def connect(cls, app):
        pass
    
    @classmethod
    @abstractmethod
    async def disconnect(cls, app):
        pass