class Ride:
    def __init__(self, rideNumber, rideCost, tripDuration):
        self.rideNumber = rideNumber
        self.rideCost = rideCost
        self.tripDuration = tripDuration

    def __lt__(self, other):
        if self.rideCost != other.rideCost:
            return self.rideCost < other.rideCost
        else:
            return self.tripDuration < other.tripDuration
    
    def __repr__(self): 
        return "(% s,% s,% s)" % (self.rideNumber, self.rideCost, self.tripDuration) 