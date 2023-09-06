from ride import Ride
from min_heap import MinHeap
from red_black_tree import RedBlackTree
import sys, os

class RideManager:
    def __init__(self):
        self.min_heap = MinHeap()
        self.red_black_tree = RedBlackTree()

    # retrieves a ride by its rideNumber from the Red-Black Tree.
    def get_ride_by_number(self, rideNumber):
        ride = self.red_black_tree.search(rideNumber)
        if ride:
            print(ride.val, file=open("output_file.txt", "a"))
        else:
            print("(0,0,0)", file=open("output_file.txt", "a"))

    # retrieves a list of rides with rideNumbers between two given values from the Red-Black Tree
    def get_rides_by_range(self, min_rideNumber, max_rideNumber):
        rides = []
        self._inorder_traversal(self.red_black_tree.root, rides, min_rideNumber, max_rideNumber)
        if rides:
            output_str = ",".join([str(rides[i]) for i in range(len(rides))])
            print(output_str, file=open("output_file.txt", "a"))
        else:
            print("(0,0,0)", file=open("output_file.txt", "a"))

    # helper method that performs an inorder traversal of the Red-Black Tree and adds rides with rideNumbers between two given values to a list.
    def _inorder_traversal(self, node, rides, min_rideNumber, max_rideNumber):
        if node == self.red_black_tree.nil:
            return
        self._inorder_traversal(node.left, rides, min_rideNumber, max_rideNumber)
        if min_rideNumber <= node.val.rideNumber <= max_rideNumber:
            rides.append(node.val)
        self._inorder_traversal(node.right, rides, min_rideNumber, max_rideNumber)

    #  adds a new ride to the Min Heap and the Red-Black Tree.
    def add_ride(self, rideNumber, rideCost, tripDuration):
        if self.red_black_tree.search(rideNumber):
            print("Duplicate RideNumber", file=open("output_file.txt", "a")) 
            sys.exit()
        ride = Ride(rideNumber, rideCost, tripDuration)
        self.min_heap.insert(ride)
        self.red_black_tree.insert(ride)

    # retrieves the ride with the lowest rideCost from the Min Heap and deletes it from the Red-Black Tree.
    def get_next_ride(self):
        ride = self.min_heap.extract_min()
        if ride == None:
            print("No active ride requests", file=open("output_file.txt", "a"))
        else:
            self.red_black_tree.delete(ride.rideNumber)
            print(f"({ride.rideNumber}, {ride.rideCost}, {ride.tripDuration})", file=open("output_file.txt", "a"))

    #  removes a ride from both the Min Heap and the Red-Black Tree.
    def delete_ride(self, rideNumber):
        self.min_heap.delete(rideNumber)
        self.red_black_tree.delete(rideNumber)

    # updates the tripDuration of a ride in both the Min Heap and the Red-Black Tree.
    def update_ride(self, rideNumber, new_tripDuration):
        self.min_heap.update(rideNumber, new_tripDuration)
        self.red_black_tree.update(rideNumber, new_tripDuration)

input_file = sys.argv[1]
file_path = "./output_file.txt"

# check if file exists
if os.path.isfile(file_path):
    # if file exists, delete its contents
    open(file_path, 'w').close()
else:
    # if file does not exist, create it
    open(file_path, 'a').close()

ride_service = RideManager()
with open(input_file) as f:
    for command in f:
        action, params = command.split('(', 1)
        params = params.strip(')\n ')
        if len(params) > 0 and params != " ":
            action_params = [int(x) for x in params.split(',')]

        if action == "Insert":
            rideNumber, rideCost, tripDuration = action_params
            ride_service.add_ride(rideNumber, rideCost, tripDuration)
        elif action == "Print":
            if len(action_params) == 1:
                rideNumber = action_params[0]
                ride_service.get_ride_by_number(rideNumber)
            elif len(action_params) == 2:
                rideNumber1, rideNumber2 = action_params
                ride_service.get_rides_by_range(rideNumber1, rideNumber2)
        elif action == "UpdateTrip":
            rideNumber, new_tripDuration = action_params
            ride_service.update_ride(rideNumber, new_tripDuration)
        elif action == "GetNextRide":
            ride_service.get_next_ride()
        elif action == "CancelRide":
            ride_service.delete_ride(action_params[0])