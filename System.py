from abc import ABC, abstractmethod


class System(ABC):

    def __init__(self, entityManager, systemManager, messageDispatcher, requiredComponents):
        self._entityManager = entityManager
        self._systemManager = systemManager
        self._messageDispatcher = messageDispatcher
        self._requiredComponents = requiredComponents

    @property
    def requiredComponents(self):
        return self._requiredComponents

    def components(self):
        return(self._entityManager
               .getAllEntitiesWithTypes(self.requiredComponents))

    @abstractmethod
    def update(self, delta):
        pass
