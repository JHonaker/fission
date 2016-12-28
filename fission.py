from abc import ABC, abstractmethod


class Component(ABC):

    def __init__(self):
        pass


class System(ABC):

    def __init__(self, requiredComponents):
        self._entityManager = None
        self._systemManager = None
        self._messageDispatcher = None
        self._requiredComponents = requiredComponents
        self._entities = set()

    def register(self, systemManager):
        """
        Register the system with its controlling system manager.

        IMPORTANT: This must be called by the system manager before using the system.
        """
        self._systemManager = systemManager
        self._entityManager = systemManager._entityManager
        self._messageDispatcher = systemManager._messageDispatcher
        self._postRegistrationSetup()

    def _postRegistrationSetup(self):
        pass

    @property
    def requiredComponents(self):
        return self._requiredComponents

    @property
    def entities(self):
        return self._entities

    def refreshEntity(self, entity):
        inSystem = True
        for componentType in self._requiredComponents:
            inSystem = inSystem and self._entityManager.hasComponent(entity, componentType)

        if inSystem:
            self._entities.add(entity)
        else:
            self._entities.discard(entity)

    def refreshAllEntities(self):
        self._entities = self._entityManager.getEntitiesWithTypeList(self._requiredComponents)

    def components(self):
        return ({componentType: self._entityManager.getComponent(entity, componentType)
            for componentType in self._requiredComponents}
            for entity in self._entities)

    @abstractmethod
    def update(self, delta):
        pass


class EntityManager:

    def __init__(self, messageDispatcher):
        self._nextID = 0
        self._recycledIDs = []
        self._entities = []
        self._components = {}

        self._messageDispatcher = messageDispatcher

    @property
    def entities(self):
        return(self._entities)

    @property
    def components(self):
        return(self._components)

    def createEntity(self):
        entity = None
        if self._recycledIDs != []:
            entity = self._recycledIDs.pop()
        else:
            entity = self._nextID
            self._nextID += 1

        self._entities.append(entity)
        self._messageDispatcher.send("entityCreated", entity)
        return(entity)

    def removeEntity(self, entity):
        for componentType in list(self._components.keys()):
            self.removeComponentFrom(entity, componentType)

        self._recycledIDs.append(entity)
        self._entities.remove(entity)
        self._messageDispatcher.send("entityRemoved", entity)

    def addComponentTo(self, entity, component):
        componentType = type(component)
        if componentType not in self._components:
            self._components[componentType] = {}

        self._components[componentType][entity] = component
        self._messageDispatcher.send("componentAdded", entity, componentType)

    def removeComponentFrom(self, entity, componentType):
        try:
            del self._components[componentType][entity]
            self._messageDispatcher("componentRemoved", entity, componentType)
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

    def getAllEntityMapsWithType(self, componentType):
        """
        Returns a dictionary with the key-value pairs:
        key: Entity ID
        val: Entitiy's owned component of the requested type
        """
        return(self._components[componentType])

    def getAllEntityMapsWithTypes(self, types):
        componentList = [self.getAllEntitiesWithType(t) for t in types]
        keys = self._entities
        for componentType in componentList:
            keys &= componentType.keys()

        entities = {entity: {type(component[entity]): component[entity]
                             for component in componentList}
                    for entity in keys}

        return(entities)

    def getEntitiesWithType(self, componentType):
        """
        Returns a set of entity ids of entities with the component type.
        """
        try:
            return set(self._components[componentType].keys())
        except KeyError:
            return set()

    def getEntitiesWithTypeList(self, types):
        entities = set(self._entities)
        for componentType in types:
            entities &= self.getEntitiesWithType(componentType)

        return entities



class SystemManager:

    def __init__(self, entityManager):
        self._systems = {}
        self._entityManager = entityManager
        self._messageDispatcher = entityManager._messageDispatcher

        self._messageDispatcher.subscribe("entityRemoved", self.handleEntityRemoval)
        self._messageDispatcher.subscribe("componentAdded", self.handleComponentAddedOrRemoved)
        self._messageDispatcher.subscribe("componentRemoved", self.handleComponentAddedOrRemoved)


    @property
    def systems(self):
        return(self._systems)

    def addSystem(self, system):
        print("adding")
        print(type(system))
        systemType = type(system)
        system.register(self)
        self._systems[systemType] = system


    def removeSystem(self, system):
        try:
            del self._systems[type(system)]
        except:
            pass

    def handleEntityRemoval(self, entity):
        for systemType in self._systems:
            system = self._systems[systemType]
            if entity in system.entities:
                system.refreshEntity(entity)

    def handleComponentAddedOrRemoved(self, entity, componentType):
        for systemType in self._systems:
            system = self._systems[systemType]
            if componentType in system.requiredComponents:
                system.refreshEntity(entity)

    def update(self, delta):
        for t, system in self._systems.items():
            system.update(delta)


class MessageDispatcher:

    def __init__(self):
        self._messageTypes = {}

    def subscribe(self, messageType, callback):
        if messageType not in self._messageTypes:
            self._messageTypes[messageType] = [callback]
        else:
            self._messageTypes[messageType].append(callback)

    def unsubscribe(self, messageType, callback):
        if messageType in self._messageTypes:
            try:
                self._messageTypes[messageType].remove(callback)
            except ValueError:
                print(str(callback) +
                      " was not subscribed to " +
                      str(messageType))

    def send(self, messageType, *args, **kargs):
        if messageType not in self._messageTypes:
            pass
        else:
            for callback in self._messageTypes[messageType]:
                callback(*args, **kargs)
