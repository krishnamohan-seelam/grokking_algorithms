# Implement single linked list in Python

import copy

class Node:
    def __init__(self, data, next=None):
        """
        Initialize a new node with data and an optional next node.

        Args:
            data: The data to store in the node.
            next (Node, optional): The next node in the list. Defaults to None.
        """
        self._data = data
        self._next = next       

    @property
    def data(self):
        """
        Get the data stored in the node.

        Returns:
            The data stored in the node.
        """
        return self._data
    
    @data.setter
    def data(self, value):
        """
        Set the data stored in the node.

        Args:
            value: The new data to store.
        """
        self._data = value

    @property
    def next(self):
        """
        Get the next node.

        Returns:
            Node or None: The next node in the list.
        """
        return self._next
    
    @next.setter
    def next(self, value):
        """
        Set the next node.

        Args:
            value (Node or None): The node to set as next.

        Raises:
            TypeError: If value is not a Node or None.
        """
        if not isinstance(value, Node) and value is not None:
            raise TypeError("next must be an instance of Node or None")
        self._next = value

    def __repr__(self):
        """
        Return a string representation of the node for debugging.

        Returns:
            str: The string representation of the node's data.
        """
        return repr(self.data)  
    
    def __str__(self):
        """
        Return a string representation of the node.

        Returns:
            str: The string representation of the node's data.
        """
        return str(self.data)
    
    def has_next(self):
        """
        Check if the node has a next node.

        Returns:
            bool: True if there is a next node, False otherwise.
        """
        return self._next is not None
    
    def append(self, next_node):
        """
        Set the next node.

        Args:
            next_node (Node): The node to set as next.
        """

        self._next = next_node

class SingleLinkedList:
    def __init__(self):
        """
        Initialize an empty single linked list.
        """
        self._head = None

    def is_empty(self):
        """
        Check if the list is empty.

        Returns:
            bool: True if the list is empty, False otherwise.
        """
        return self._head is None
    
    def traverse(self, functor):
        """
        Traverse the list, applying a function to each node's data.

        Args:
            functor (callable): A function to apply to each node's data.

        Yields:
            The result of applying functor to each node's data.
        """
        current = self._head
        while current is not None:
            yield functor(current.data)
            current = current.next

    def __iter__(self):
        """
        Iterate over the data in the list.

        Yields:
            The data of each node in the list.
        """
        current = self._head
        while current is not None:
            yield current.data
            current = current.next

    def __len__(self):
        """
        Return the number of elements in the list.

        Returns:
            int: The number of elements in the list.
        """
        count = 0
        current = self._head
        while current is not None:
            count += 1
            current = current.next
        return count
    
    def size(self):
        """
        Return the number of elements in the list.

        Returns:
            int: The number of elements in the list.
        """
        return self.__len__()
        
    def search(self, predicate):
        """
        Search for the first element matching a predicate.

        Args:
            predicate (callable): A function that returns True for the desired element.

        Returns:
            The data of the first matching node, or None if not found.
        """
        current = self._head
        while current is not None:
            if predicate(current.data):
                return current.data
            current = current.next
        return None
    
    def __contains__(self, item):
        """
        Check if an item is in the list.

        Args:
            item: The item to search for.

        Returns:
            bool: True if the item is in the list, False otherwise.
        """
        current = self._head
        while current is not None:
            if current.data == item:
                return True
            current = current.next
        return False
    
    def __repr__(self):
        """
        Return a string representation of the list for debugging.

        Returns:
            str: The string representation of the list.
        """
        return f'SingleLinkedList({" ->" .join(self.traverse(str))})'
    
    def __str__(self):
        """
        Return a string representation of the list.

        Returns:
            str: The string representation of the list.
        """
        return " -> ".join(self.traverse(str))

    def insert_to_front(self, data):
        """
        Insert a new element at the front of the list.

        Args:
            data: The data to insert.
        """
        if self.is_empty():
            self._head = Node(data)
            return
        
        old_head = self._head
        self._head = Node(data, old_head)



    def insert_to_back(self, data):
        """
        Insert a new element at the back of the list.

        Args:
            data: The data to insert.
        """
        new_node = Node(data)

        if not self._head:
            self._head = new_node
            return
        
        current = self._head
        while current.has_next():
            current = current.next
        current.append(new_node)

    def get(self, index):
        """
        Get the data at a specific index.

        Args:
            index (int): The index of the element to retrieve.

        Returns:
            The data at the specified index.

        Raises:
            IndexError: If the index is out of bounds.
        """
        if index < 0:
            raise IndexError("Index must be a non-negative integer")
        
        current = self._head
        for _ in range(index):
            if current is None:
                raise IndexError("Index out of bounds")
            current = current.next
        
        if current is None:
            raise IndexError("Index out of bounds")
        
        return copy.deepcopy(current.data)
    
    def delete(self, target):
        """
        Delete the first occurrence of a value from the list.

        Args:
            target: The value to delete.

        Raises:
            ValueError: If the value is not found in the list.
        """
        current = self._head
        previous = None
        while current is not None:
            if current.data == target:
                if previous is None:
                    self._head = current.next
                else:
                    previous.append(current.next)
                return
            previous = current
            current = current.next
        raise ValueError(f'No element with value {target} was found in the list.')
    
    def delete_from_front(self):
        """
        Delete the element at the front of the list and return its data.

        Returns:
            The data of the removed node.

        Raises:
            ValueError: If the list is empty.
        """
        if not self:
            raise ValueError("List is empty")
        data = self._head.data
        self._head = self._head.next
        return data


