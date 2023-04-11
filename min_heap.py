from ride import Ride

class MinHeap:
    def __init__(self):
        self.heap = []

    def parent(self, index):
        return (index - 1) // 2

    def left_child(self, index):
        return 2 * index + 1

    def right_child(self, index):
        return 2 * index + 2

    def swap(self, firstIndex, secondIndex):
        self.heap[firstIndex], self.heap[secondIndex] = self.heap[secondIndex], self.heap[firstIndex]

    def insert(self, ride):
        self.heap.append(ride)
        i = len(self.heap) - 1
        while i != 0 and self.heap[self.parent(i)] > self.heap[i]:
            self.swap(i, self.parent(i))
            i = self.parent(i)

    def extract_min(self):
        if len(self.heap) == 0:
            return None
        min_ride = self.heap[0]
        self.heap[0] = self.heap[-1]
        del self.heap[-1]
        self.min_heapify(0)
        return min_ride

    def decrease_key(self, index, new_val):
        self.heap[index] = new_val
        while index != 0 and self.heap[index] < self.heap[self.parent(index)]:
            self.swap(index, self.parent(index))
            index = self.parent(index)

    def delete(self, key):
        i = 0
        while i < len(self.heap):
            if self.heap[i].rideNumber == key:
                self.decrease_key(i, Ride(-1, -1, -1))
                self.extract_min()
            else:
                i += 1

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