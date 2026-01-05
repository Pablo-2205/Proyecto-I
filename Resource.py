class Resource :
    def __init__(self , type , id):
        self.id = id
        self.type = type


class PlayController(Resource):
    def __init__(self, type, id):
        super().__init__(type, id)


    

