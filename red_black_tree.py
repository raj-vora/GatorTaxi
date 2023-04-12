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
    def left_rotate(self, current):
        rightChild = current.right
        current.right = rightChild.left
        if rightChild.left != self.nil:
            rightChild.left.parent = current
        rightChild.parent = current.parent
        if current.parent == self.nil:
            self.root = rightChild
        elif current == current.parent.left:
            current.parent.left = rightChild
        else:
            current.parent.right = rightChild
        rightChild.left = current
        current.parent = rightChild

    # Rotate right
    def right_rotate(self, current):
        leftChild = current.left
        current.left = leftChild.right
        if leftChild.right != self.nil:
            leftChild.right.parent = current
        leftChild.parent = current.parent
        if current.parent == self.nil:
            self.root = leftChild
        elif current == current.parent.right:
            current.parent.right = leftChild
        else:
            current.parent.left = leftChild
        leftChild.right = current
        current.parent = leftChild

    # Insert a node into the tree
    def insert(self, ride):
        newNode = Node(ride, 'Red')
        newNode.parent = self.nil
        newNode.left = self.nil
        newNode.right = self.nil
        temp = self.nil
        root = self.root

        while root != self.nil:
            temp = root
            if newNode.val.rideNumber < root.val.rideNumber:
                root = root.left
            else:
                root = root.right

        newNode.parent = temp
        if temp == self.nil:
            self.root = newNode
        elif newNode.val.rideNumber < temp.val.rideNumber:
            temp.left = newNode
        else:
            temp.right = newNode

        newNode.left = self.nil
        newNode.right = self.nil
        newNode.color = "Red"
        self.fix_insert(newNode)

    # Fix the tree after an insert
    def fix_insert(self, newNode):
        while newNode.parent.color == "Red":
            if newNode.parent == newNode.parent.parent.left:
                rightChild = newNode.parent.parent.right
                if rightChild.color == "Red":
                    newNode.parent.color = "Black"
                    rightChild.color = "Black"
                    newNode.parent.parent.color = "Red"
                    newNode = newNode.parent.parent
                else:
                    if newNode == newNode.parent.right:
                        newNode = newNode.parent
                        self.left_rotate(newNode)
                    newNode.parent.color = "Black"
                    newNode.parent.parent.color = "Red"
                    self.right_rotate(newNode.parent.parent)
            else:
                rightChild = newNode.parent.parent.left
                if rightChild.color == "Red":
                    newNode.parent.color = "Black"
                    rightChild.color = "Black"
                    newNode.parent.parent.color = "Red"
                    newNode = newNode.parent.parent
                else:
                    if newNode == newNode.parent.left:
                        newNode = newNode.parent
                        self.right_rotate(newNode)
                    newNode.parent.color = "Black"
                    newNode.parent.parent.color = "Red"
                    self.left_rotate(newNode.parent.parent)
        self.root.color = "Black"

    # Delete a node from the tree
    def delete(self, val):
        current = self.search(val)
        if current == None:
            return
        temp = current
        y_original_color = temp.color
        if current.left == self.nil:
            root = current.right
            self.transplant(current, current.right)
        elif current.right == self.nil:
            root = current.left
            self.transplant(current, current.left)
        else:
            temp = self.minimum(current.right)
            y_original_color = temp.color
            root = temp.right
            if temp.parent == current:
                root.parent = temp
            else:
                self.transplant(temp, temp.right)
                temp.right = current.right
                temp.right.parent = temp
            self.transplant(current, temp)
            temp.left = current.left
            temp.left.parent = temp
            temp.color = current.color
        if y_original_color == "Black":
            self.fix_delete(root)

    # Fix the tree after a delete
    def fix_delete(self, root):
        while root != self.root and root.color == "Black":
            if root == root.parent.left:
                rightUncle = root.parent.right
                if rightUncle.color == "Red":
                    rightUncle.color = "Black"
                    root.parent.color = "Red"
                    self.left_rotate(root.parent)
                    rightUncle = root.parent.right
                if rightUncle.left.color == "Black" and rightUncle.right.color == "Black":
                    rightUncle.color = "Red"
                    root = root.parent
                else:
                    if rightUncle.right.color == "Black":
                        rightUncle.left.color = "Black"
                        rightUncle.color = "Red"
                        self.right_rotate(rightUncle)
                        rightUncle = root.parent.right
                    rightUncle.color = root.parent.color
                    root.parent.color = "Black"
                    rightUncle.right.color = "Black"
                    self.left_rotate(root.parent)
                    root = self.root
            else:
                rightUncle = root.parent.left
                if rightUncle.color == "Red":
                    rightUncle.color = "Black"
                    root.parent.color = "Red"
                    self.right_rotate(root.parent)
                    rightUncle = root.parent.left
                if rightUncle.right.color == "Black" and rightUncle.left.color == "Black":
                    rightUncle.color = "Red"
                    root = root.parent
                else:
                    if rightUncle.left.color == "Black":
                        rightUncle.right.color = "Black"
                        rightUncle.color = "Red"
                        self.left_rotate(rightUncle)
                        rightUncle = root.parent.left
                    rightUncle.color = root.parent.color
                    root.parent.color = "Black"
                    rightUncle.left.color = "Black"
                    self.right_rotate(root.parent)
                    root = self.root
        root.color = "Black"

    # Replace one subtree as a child of its parent with another subtree
    def transplant(self, first, second):
        if first.parent == self.nil:
            self.root = second
        elif first == first.parent.left:
            first.parent.left = second
        else:
            first.parent.right = second
        second.parent = first.parent

    # Find the node with the minimum value in a subtree
    def minimum(self, min):
        while min.left != self.nil:
            min = min.left
        return min

    # Search for a node with a specific value
    def search(self, val):
        root = self.root
        if root.val != None:
            if root.val.rideNumber == val:
                return root
            while root != self.nil and root.val.rideNumber != val:
                if val < root.val.rideNumber:
                    root = root.left
                else:
                    root = root.right
            return root if root != self.nil else None

    # Update the value of a node
    def update(self, rideNumber, newTripDuration):
        node = self.search(rideNumber)
        if node is None:
            return False  # Node with old_val not found in tree
        if newTripDuration <= node.val.tripDuration:
            node.val.tripDuration = newTripDuration
        elif node.val.tripDuration< newTripDuration <= 2* node.val.tripDuration:
            newRideCost = node.val.rideCost+10
            self.delete(rideNumber)
            self.insert(Ride(node.val.rideNumber,newRideCost,newTripDuration))
        elif newTripDuration > 2* node.val.tripDuration:
            self.delete(rideNumber)

# Example usage:
tree = RedBlackTree()
tree.insert
