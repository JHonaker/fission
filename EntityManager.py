class EntityManager:

    def __init__(self):
        self._nextID = 0
        self._entities = []
        self._components = {}

    @property
    def entities(self):
        return(self._entities)

    @property
    def components(self):
        return(self._components)

    def createEntity(self):
        entityID = self._nextID
        self._entities.append(entityID)

        self._nextID += 1

        return(entityID)

    def removeEntity(self, entity):
        for componentType in list(self._components.keys()):
            self.removeComponentFrom(entity, componentType)

        self._entities.remove(entity)

    def addComponentTo(self, entity, component):
        componentType = type(component)
        if componentType not in self._components:
            self._components[componentType] = {}

        self._components[componentType][entity] = component

    def removeComponentFrom(self, entity, componentType):
        try:
            del self._components[componentType][entity]
            if self._components[componentType] == {}:
                del self._components[componentType]
        except KeyError:
            pass

    def hasComponent(self, entity, componentType):
        if (componentType in self._components and
                entity in self._components[componentType]):

            return True
        else:
            return False

    def getComponent(self, entity, componentType):
        try:
            return(self._components[componentType][entity])
        except KeyError:
            pass

    def getAllComponentsOfType(self, componentType):
        try:
            return(self._components[componentType])
        except KeyError:
            pass

    def getAllComponentsInEntity(self, entity):
        components = {}
        for componentType, instances in self._components.items():
            if entity in instances:
                components[componentType] = instances[entity]
        return(components)

    def getAllEntitiesWithType(self, componentType):
        """
        Returns a dictionary with the key-value pairs:
        key: Entity ID
        val: Entitiy's owned component of the requested type
        """
        return(self._components[componentType])

    def getAllEntitiesWithTypes(self, types):
        componentList = [self.getAllEntitiesWithType(t) for t in types]
        keys = self._entities
        for componentType in componentList:
            keys &= componentType.keys()

        entities = {entity: {type(component[entity]): component[entity]
                             for component in componentList}
                    for entity in keys}

        return(entities)
