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

class Xbox360Controller(Resource):
    def __init__(self, type, id):
        super().__init__(type, id) 

class Xbox360(Resource):
    def __init__(self, type, id):
        super().__init__(type, id)

class XboxOne(Resource):
    def __init__(self, type, id):
        super().__init__(type, id)

class XboxOneController(Resource):
    def __init__(self, type, id):
        super().__init__(type, id)

class TV(Resource):
    def __init__(self, type, id , size = 32):
        super().__init__(type, id)
        self.size = size        

class HeadPhones(Resource):
    def __init__(self, type, id):
        super().__init__(type, id)

class VRGlasses(Resource):
    def __init__(self, type, id):
        super().__init__(type, id)

     



