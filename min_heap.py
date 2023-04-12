from ride import Ride

class MinHeap:
    #  initializes an empty list called heap which will store the Ride objects in the min-heap.
    def __init__(self):
        self.heap = []

    # helper methods to calculate the indices of the parent, left child, and right child nodes of a given index.
    def parent(self, index):
        return (index - 1) // 2

    def left_child(self, index):
        return 2 * index + 1

    def right_child(self, index):
        return 2 * index + 2

    # helper method to swap the positions of two elements in the heap list.
    def swap(self, firstIndex, secondIndex):
        self.heap[firstIndex], self.heap[secondIndex] = self.heap[secondIndex], self.heap[firstIndex]

    #  takes a ride object as input and adds it to the heap. It then reorders the heap to maintain the min-heap property by swapping the added element with its parent if the parent is larger.
    def insert(self, ride):
        self.heap.append(ride)
        i = len(self.heap) - 1
        while i != 0 and self.heap[self.parent(i)] > self.heap[i]:
            self.swap(i, self.parent(i))
            i = self.parent(i)

    # returns the minimum ride from the heap, which is the root node of the min-heap. It then replaces the root node with the last element in the heap and reorders the heap to maintain the min-heap property.
    def extract_min(self):
        if len(self.heap) == 0:
            return None
        min_ride = self.heap[0]
        self.heap[0] = self.heap[-1]
        del self.heap[-1]
        self.min_heapify(0)
        return min_ride

    # updates the value of an element in the heap at a given index and reorders the heap to maintain the min-heap property.
    def decrease_key(self, index, new_val):
        self.heap[index] = new_val
        while index != 0 and self.heap[index] < self.heap[self.parent(index)]:
            self.swap(index, self.parent(index))
            index = self.parent(index)

    # deletes a ride from the heap with a given ride number. 
    def delete(self, key):
        i = 0
        while i < len(self.heap):
            if self.heap[i].rideNumber == key:
                self.decrease_key(i, Ride(-1, -1, -1))
                self.extract_min()
            else:
                i += 1

    # reorders the heap to maintain the min-heap property.
    def min_heapify(self, index):
        l = self.left_child(index)
        r = self.right_child(index)
        smallest = index
        if l < len(self.heap) and self.heap[l] < self.heap[smallest]:
            smallest = l
        if r < len(self.heap) and self.heap[r] < self.heap[smallest]:
            smallest = r
        if smallest != index:
            self.swap(index, smallest)
            self.min_heapify(smallest)

    '''
    updates the duration of a ride with the given ride number to a new duration. 
    If the new duration is less than or equal to the current duration, then the ride is updated with the new duration. 
    If the new duration is greater than current duration then the ride cost is increased by 10 and the ride is removed and reinserted into the heap with the new cost and duration. 
    If the new duration is greater than twice the current duration, then the ride is removed from the heap.
    '''
    def update(self, rideNumber, newTripDuration):
        for i in range(len(self.heap)):
            if self.heap[i].rideNumber == rideNumber:
                currentTripDuration = self.heap[i].tripDuration
                if newTripDuration <= currentTripDuration:
                    self.heap[i].tripDuration = newTripDuration
                elif currentTripDuration < newTripDuration <= 2* currentTripDuration:
                    newRideCost = self.heap[i].rideCost+10
                    self.delete(rideNumber)
                    self.insert(Ride(rideNumber, newRideCost, newTripDuration))
                else:
                    self.delete(rideNumber)
                break