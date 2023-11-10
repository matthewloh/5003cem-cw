from math import floor
import random


def hashfunction_1(a: int, b: int, i: int):
    """
    Hash Function 1: 
        h(k) = ((a*k + b)) mod m
        where:
            a and b are random numbers
            k is the key
            m is the size of the hash table
    """
    return (((a*i)+b) % self.capacity)


def hashfunction_2(a: int, b: int, i: int):
    """
    Hash Function 2:
        h(k) = floor(m * (
            (k * (a/b) mod 1)
            )
        )
        where:
            a and b are random numbers
            k is the key
            m is the size of the hash table
    """
    return math.floor(self.capacity * ((i * (a/b) % 1)))


def insert_key(self, key: int):
    """
    Insert a key into the hash table
    """
    i = 0
    while i < self.capacity:
        j = hashfunction_1(self.a, self.b, i)
        if self.table[j] == None:
            self.table[j] = key
            return j
        else:
            i += 1
    return None


class HashTable:
    def __init__(self, capacity: int, a: int, b: int) -> None:
        self.capacity = capacity
        self.a = a
        self.b = b
        self.keys = [None] * capacity
        self.values = [None] * capacity

    def get_capacity(self) -> int:
        return self._capacity

    def set_capacity(self, capacity: int) -> None:
        self._capacity = capacity

    def get_a(self) -> int:
        return self._a

    def set_a(self, a: int) -> None:
        self._a = a

    def get_b(self) -> int:
        return self._b

    def set_b(self, b: int) -> None:
        self._b = b

    def get_keys(self) -> list:
        return self._keys

    def set_keys(self, keys: list) -> None:
        self._keys = keys

    def get_values(self) -> list:
        return self._values

    def set_values(self, values: list) -> None:
        self._values = values

    def hash_function_1(self, key: int) -> int:
        """
        Args:
            key (int): The key to be hashed
        Returns:
            int: The hash value
        Hash Function 1: 
            h(k) = ((a*k + b)) mod m
            where:
                a and b are random numbers
                k is the key
                m is the size of the hash table
        """
        return (((self.get_a*key)+self.get_b) % self.get_capacity)

    def hash_function_2(self, key: int) -> int:
        """
        Args:
            key (int): The key to be hashed
        Returns:
            int: The hash value
        Hash Function 2:
            h(k) = floor(
                m * (
                    (k * (a/b) mod 1)
                )
            )
            where:
                a and b are random numbers
                k is the key
                m is the size of the hash table
        """
        return floor(self.get_capacity * ((key * (self.get_a/self.get_b) % 1)))    
    
    def put(self, key, value):
        index = self.hash_function_1(key)

        while self._keys[index] is not None:
            if self._keys[index] == key:
                self._values[index] = value
                return
            index = (index + 1) % self._capacity

        self._keys[index] = key
        self._values[index] = value

    def get(self, key):
        index = self.hash_function_1(key)

        while self._keys[index] is not None:
            if self._keys[index] == key:
                return self._values[index]
            index = (index + 1) % self._capacity

        return None

    def remove(self, key):
        index = self.hash_function_1(key)

        while self._keys[index] is not None:
            if self._keys[index] == key:
                self._keys[index] = None
                self._values[index] = None
                return
                index = (index + 1) % self._capacity

# Usage:
# hash_table = HashTable1(5500, a, b)


if __name__ == "__main__":
    hash_table = HashTable(5500, 33, 33)
    # Python oneliner to generate a list of 5000 random integers
    # between 0 and 10000
    random_integers = [random.randint(0, 10000) for _ in range(5000)]
