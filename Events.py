class Events:
    def __init__(self , eventName ,  start , finish , resources , clients = 0):
        self.eventName = eventName
        self.start = start
        self.finish = finish
        self.resources = resources
        self.clientes = clients
