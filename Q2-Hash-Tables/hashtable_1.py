import random

def hashfunction_1():
    return (((a*i)+b) % self.capacity)

def hashfunction_2():
    return math.floor(self.capacity * ((i * (a/b) % 1)))
class HashTable1:
    def __init__(self, size, a, b):
        self.size = size
        self.a = a
        self.b = b
        self.keys = [None] * size
        self.values = [None] * size

    def _hash(self, key):
        return (self.a * key + self.b) % self.size

    def put(self, key, value):
        index = self._hash(key)

        while self.keys[index] is not None:
            if self.keys[index] == key:
                self.values[index] = value
                return
            index = (index + 1) % self.size

        self.keys[index] = key
        self.values[index] = value

    def get(self, key):
        index = self._hash(key)

        while self.keys[index] is not None:
            if self.keys[index] == key:
                return self.values[index]
            index = (index + 1) % self.size

        return None

    def remove(self, key):
        index = self._hash(key)

        while self.keys[index] is not None:
            if self.keys[index] == key:
                self.keys[index] = None
                self.values[index] = None
                return
            index = (index + 1) % self.size

# Usage:
# hash_table = HashTable1(5500, a, b)

if __name__ == "__main__":
    hash_table = HashTable1(5500, 33, 33)
    # Python oneliner to generate a list of 5000 random integers
    # between 0 and 10000
    random_integers = [random.randint(0, 10000) for _ in range(5000)]