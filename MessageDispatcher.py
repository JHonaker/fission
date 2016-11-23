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
            print("Nobody responds to " + str(messageType) + " messages")
        else:
            for callback in self._messageTypes[messageType]:
                callback(*args, **kargs)
