from collections import Counter
from math import floor
from typing import Iterable, List
import numpy as np
from numpy.random import default_rng
import matplotlib.pyplot as plt


class HashTable:
    """
    Hash Table with open addressing and linear probing
    Args:
        capacity (int): The size of the hash table (default: 5500)
        a (int): Random number 1
        b (int): Random number 2
    """

    def __init__(
        self,
        a: int,
        b: int,
        capacity: int = 5500,
    ) -> None:
        self.capacity = capacity
        self.a = a
        self.b = b
        self.values = [None] * capacity
        self.numOfCollisions = 0

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
        return ((self.a * key) + self.b) % self.capacity

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
        return floor(self.capacity * ((key * (self.a / self.b) % 1)))

    def bulk_insert(self, values: Iterable, hash_function=hash_function_1):
        """
        bulk_insert is used for entering more than one element at a time
        in the HashTable.
        Time Complexity: O(n)
        """
        for value in values:
            self.insert_data(value, hash_function)
        print(f"Number of collisions: {self.numOfCollisions}")

    def isFull(self) -> bool:
        """
        isFull checks if the hash table is full.
        """
        return self.values.count(None) == 0

    def insert_data(self, data: int, hash_function=hash_function_1) -> None:
        """
        insert_data is used for entering a single element in the HashTable.
        Time Complexity: O(1)
        """
        if self.isFull():
            raise Exception("Hash Table is full")

        position = hash_function(data)
        if self.values[position] is None:
            self.values[position] = data
        else:
            self.numOfCollisions += 1
            while self.values[position] is not None:
                position += 1
                if position == self.capacity:
                    position = 0

            self.values[position] = data

    def remove(self, key):
        """
        This method removes the key from the hash table
        """
        self.values[key] = None

    def distribute(self, hash_function=hash_function_1):
        """
        This method returns the distribution of the hash table
        """
        counter = Counter(
            [hash_function(
                item) % self.capacity for item in self.values if item is not None])
        self.mean = np.mean(list(counter.values()))
        self.std_dev = np.std(list(counter.values()))
        print(f"Mean: {self.mean}, Standard Deviation: {self.std_dev}")
        return counter

    def test_distribute(self, nums: List[int], hash_function=hash_function_1):
        """
        This method returns the distribution of the hash table
        """
        counter = Counter(
            [hash_function(item) for item in nums if item is not None]
        )
        return counter

    def plot(self, histogram):
        """
        This method plots the distribution of the hash table
        """
        for key in sorted(histogram):
            count = histogram[key]
            padding = (max(histogram.values()) - count) * " "
            print(f"{key:1} {'■' * count}{padding} ({count})")


if __name__ == "__main__":
    finalMean_1 = 0
    finalMean_2 = 0
    finalStdDev_1 = 0
    finalStdDev_2 = 0
    final_numOfCollisions_1 = 0
    final_numOfCollisions_2 = 0
    for i in range(10):
        print(f"Running experiment {i+1}")
        CAPACITY = 5500
        NUMSIZE = 5000
        MAXRANGE = 100_000
        a, b = 0, 0
        a = np.random.randint(1,  10)
        b = np.random.randint(10, 100)
        print(f"a value: {a}, b value: {b}")
        hash_table_1 = HashTable(a=a, b=b, capacity=CAPACITY)
        hash_table_2 = HashTable(a=a, b=b, capacity=CAPACITY)
        rng = default_rng()
        nums = rng.choice(np.arange(0, MAXRANGE), size=NUMSIZE,
                          replace=False).tolist()
        print(f"{len(nums)} random integers generated")
        print("Hash Function 1 currently running")
        plt.figure(figsize=(15, 5))
        plt.subplot(1, 2, 1)
        hash_table_1.bulk_insert(nums, hash_table_1.hash_function_1)
        histogram_1 = hash_table_1.distribute(hash_table_1.hash_function_1)
        plt.bar(histogram_1.keys(), histogram_1.values())
        plt.title(
            f'Hash Function 1\nmean: {hash_table_1.mean.round(6)}, std deviation: {hash_table_1.std_dev.round(6)}\nno. of collisions: {hash_table_1.numOfCollisions}\na: {a}, b: {b}')

        plt.subplot(1, 2, 2)
        print("Hash Function 2 currently running")
        hash_table_2.bulk_insert(nums, hash_table_2.hash_function_2)
        histogram_2 = hash_table_2.distribute(hash_table_2.hash_function_2)
        plt.bar(histogram_2.keys(), histogram_2.values())
        plt.title(
            f'Hash Function 2\nmean: {hash_table_2.mean.round(6)}, std deviation: {hash_table_2.std_dev.round(6)}\nno. of collisions: {hash_table_2.numOfCollisions}\na: {a}, b: {b}')
        plt.tight_layout()

        finalMean_1 += hash_table_1.mean
        finalMean_2 += hash_table_2.mean
        finalStdDev_1 += hash_table_1.std_dev
        finalStdDev_2 += hash_table_2.std_dev
        final_numOfCollisions_1 += hash_table_1.numOfCollisions
        final_numOfCollisions_2 += hash_table_2.numOfCollisions
    print(f"Final mean for Hash Function 1: {finalMean_1/10}")
    print(f"Final mean for Hash Function 2: {finalMean_2/10}")
    print(f"Final standard deviation for Hash Function 1: {finalStdDev_1/10}")
    print(f"Final standard deviation for Hash Function 2: {finalStdDev_2/10}")
    print(
        f"Final number of collisions for Hash Function 1: {final_numOfCollisions_1/10}")
    print(
        f"Final number of collisions for Hash Function 2: {final_numOfCollisions_2/10}")

    plt.show()
