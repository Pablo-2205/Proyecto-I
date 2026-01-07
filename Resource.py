class Resource :
    def __init__(self , type , id ):
        self.id = id
        self.type = type
        

    
class PS5(Resource):
    def __init__(self, type, id):
        super().__init__(type, id)

class PS4(Resource):
    def __init__(self, type, id):
        super().__init__(type, id)

class PS5Controller(Resource):
    def __init__(self, type, id):
        super().__init__( type , id)

class PS4Controller(Resource):
    def __init__(self, type, id):
        super().__init__(type, id)

class PC(Resource):
    def __init__(self, type, id):
        super().__init__(type , id)
     



