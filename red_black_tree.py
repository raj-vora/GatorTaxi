from ride import Ride

# Node class for Red-Black Tree
class Node:
    def __init__(self, val, color="Red"):
        self.val = val
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

# Red-Black Tree class
class RedBlackTree:
    def __init__(self):
        self.nil = Node(None, "Black")
        self.root = self.nil

    # Rotate left
    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.nil:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == self.nil:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    # Rotate right
    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.nil:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == self.nil:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    # Insert a node into the tree
    def insert(self, ride):
        z = Node(ride, 'Red')
        z.parent = self.nil
        z.left = self.nil
        z.right = self.nil
        y = self.nil
        x = self.root

        while x != self.nil:
            y = x
            if z.val.rideNumber < x.val.rideNumber:
                x = x.left
            else:
                x = x.right

        z.parent = y
        if y == self.nil:
            self.root = z
        elif z.val.rideNumber < y.val.rideNumber:
            y.left = z
        else:
            y.right = z

        z.left = self.nil
        z.right = self.nil
        z.color = "Red"
        self.fix_insert(z)

    # Fix the tree after an insert
    def fix_insert(self, z):
        while z.parent.color == "Red":
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y.color == "Red":
                    z.parent.color = "Black"
                    y.color = "Black"
                    z.parent.parent.color = "Red"
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self.left_rotate(z)
                    z.parent.color = "Black"
                    z.parent.parent.color = "Red"
                    self.right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.color == "Red":
                    z.parent.color = "Black"
                    y.color = "Black"
                    z.parent.parent.color = "Red"
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self.right_rotate(z)
                    z.parent.color = "Black"
                    z.parent.parent.color = "Red"
                    self.left_rotate(z.parent.parent)
        self.root.color = "Black"

    # Delete a node from the tree
    def delete(self, val):
        z = self.search(val)
        if z == None:
            return
        y = z
        y_original_color = y.color
        if z.left == self.nil:
            x = z.right
            self.transplant(z, z.right)
        elif z.right == self.nil:
            x = z.left
            self.transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self.transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == "Black":
            self.fix_delete(x)

    # Fix the tree after a delete
    def fix_delete(self, x):
        while x != self.root and x.color == "Black":
            if x == x.parent.left:
                w = x.parent.right
                if w.color == "Red":
                    w.color = "Black"
                    x.parent.color = "Red"
                    self.left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color == "Black" and w.right.color == "Black":
                    w.color = "Red"
                    x = x.parent
                else:
                    if w.right.color == "Black":
                        w.left.color = "Black"
                        w.color = "Red"
                        self.right_rotate(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = "Black"
                    w.right.color = "Black"
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == "Red":
                    w.color = "Black"
                    x.parent.color = "Red"
                    self.right_rotate(x.parent)
                    w = x.parent.left
                if w.right.color == "Black" and w.left.color == "Black":
                    w.color = "Red"
                    x = x.parent
                else:
                    if w.left.color == "Black":
                        w.right.color = "Black"
                        w.color = "Red"
                        self.left_rotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = "Black"
                    w.left.color = "Black"
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = "Black"

    # Replace one subtree as a child of its parent with another subtree
    def transplant(self, u, v):
        if u.parent == self.nil:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    # Find the node with the minimum value in a subtree
    def minimum(self, x):
        while x.left != self.nil:
            x = x.left
        return x

    # Search for a node with a specific value
    def search(self, val):
        x = self.root
        if x.val != None:
            if x.val.rideNumber == val:
                return x
            while x != self.nil and x.val.rideNumber != val:
                if val < x.val.rideNumber:
                    x = x.left
                else:
                    x = x.right
            return x if x != self.nil else None

    # Update the value of a node
    def update(self, rideNumber, newTripDuration):
        node = self.search(rideNumber)
        if node is None:
            return False  # Node with old_val not found in tree
        if newTripDuration <= node.val.tripDuration:
            node.val.tripDuration = newTripDuration
        elif node.val.tripDuration< newTripDuration <= 2* node.val.tripDuration:
            self.delete(rideNumber)
            self.insert(Ride(node.val.rideNumber,node.val.rideCost+10,newTripDuration))
        elif newTripDuration > 2* node.val.tripDuration:
            self.delete(rideNumber)

# Example usage:
tree = RedBlackTree()
tree.insert
