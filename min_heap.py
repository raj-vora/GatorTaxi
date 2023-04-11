from ride import Ride
import math

class MinHeap:
    def __init__(self):
        self.heap = []

    def parent(self, i):
        return (i - 1) // 2

    def left_child(self, i):
        return 2 * i + 1

    def right_child(self, i):
        return 2 * i + 2

    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

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

    def decrease_key(self, i, new_val):
        self.heap[i] = new_val
        while i != 0 and self.heap[self.parent(i)] < self.heap[i]:
            self.swap(i, self.parent(i))
            i = self.parent(i)

    def delete(self, key):
        i = 0
        while i < len(self.heap):
            if self.heap[i].rideNumber == key:
                self.decrease_key(i, Ride(100000, 100000, 100000))
                self.extract_min()
            else:
                i += 1

    def min_heapify(self, i):
        l = self.left_child(i)
        r = self.right_child(i)
        smallest = i
        if l < len(self.heap) and self.heap[l] < self.heap[smallest]:
            smallest = l
        if r < len(self.heap) and self.heap[r] < self.heap[smallest]:
            smallest = r
        if smallest != i:
            self.swap(i, smallest)
            self.min_heapify(smallest)

    def update(self, rideNumber, new_tripDuration):
        for i in range(len(self.heap)):
            if self.heap[i].rideNumber == rideNumber:
                existing_tripDuration = self.heap[i].tripDuration
                if new_tripDuration <= existing_tripDuration:
                    self.heap[i].tripDuration = new_tripDuration
                elif existing_tripDuration < new_tripDuration <= 2* existing_tripDuration:
                    new_rideCost = self.heap[i].rideCost+10
                    self.delete(rideNumber)
                    self.insert(Ride(rideNumber, new_rideCost, new_tripDuration))
                else:
                    self.delete(rideNumber)
                break