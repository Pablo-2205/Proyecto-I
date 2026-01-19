class Resource :
    def __init__(self , type , id ):
        self.id = id
        self.type = type
        
class PS5(Resource):
    quantity = 5
    def __init__(self, type, id):
        super().__init__(type, id )

class PS4(Resource):
    quantity = 5
    def __init__(self, type, id):
        super().__init__(type, id)

class PS5Controller(Resource):
    quantity = 10
    def __init__(self, type, id):
        super().__init__(type, id)

class PS4Controller(Resource):
    quantity = 10
    def __init__(self, type, id):
        super().__init__(type, id)

class PC(Resource):
    quantity = 32
    def __init__(self, type, id ):
        super().__init__(type, id)

class Xbox360Controller(Resource):
    quantity = 10
    def __init__(self, type, id):
        super().__init__(type, id)

class Xbox360(Resource):
    quantity = 5
    def __init__(self, type, id ):
        super().__init__(type, id)

class XboxOne(Resource):
    quantity = 5
    def __init__(self, type, id):
        super().__init__(type, id)

class XboxOneController(Resource):
    quantity = 10
    def __init__(self, type, id):
        super().__init__(type, id)

class TV(Resource):
    quantity = 12
    def __init__(self, type, id):
        super().__init__(type, id)

class HeadPhones(Resource):
    quantity = 32
    def __init__(self, type, id):
        super().__init__(type, id)

class VRGlasses(Resource):
    quantity = 6
    def __init__(self, type, id):
        super().__init__(type, id)
     



