def Overlap(e1 , e2):
    return not(e1.end <= e2.start or e2.end <= e1.start)

def IsIncompatible(newEvent , existingEvents):
    for event in existingEvents:
        if(Overlap(newEvent , event)):
            print("No se puede reservar")
            return True
    return False






