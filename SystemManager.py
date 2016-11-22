class SystemManager:

    def __init__(self, entityManager):
        self._systems = {}
        self._entityManager = entityManager

    @property
    def systems(self):
        return(self._systems)

    def addSystem(self, system):
        systemType = type(system)
        self._systems[systemType] = system

    def removeSystem(self, system):
        pass

    def update(self, delta):
        for t, system in self._systems.items():
            system.update(delta)
