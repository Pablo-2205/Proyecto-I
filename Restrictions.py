def Overlap(e1 , e2):
    return not(e1.finish <= e2.start or e2.finish <= e1.start)

def IsIncompatible(newEvent , existingEvents):
    for event in existingEvents:
        if(Overlap(newEvent , event)):
            for resource in newEvent.resource:
                if(resource in event.resource):
                    return True
    return False

