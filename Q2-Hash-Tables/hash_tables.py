from typing import Iterable
from number_theory.prime_numbers import next_prime


class HashTable:
    """
    Basic Hash Table example with open addressing and linear probing
    """

    def __init__(
        self,
        size_table: int,
        charge_factor: int | None = None,
        lim_charge: float | None = None,
    ) -> None:
        self.size_table = size_table
        self.values = [None] * self.size_table
        self.lim_charge = 0.75 if lim_charge is None else lim_charge
        self.charge_factor = 1 if charge_factor is None else charge_factor
        self.__aux_list: list = []
        self._keys: dict = {}

    def keys(self):
        """
        The keys function returns a dictionary containing the key value pairs.
        key being the index number in hash table and value being the data value.
        """
        return self._keys

    def balanced_factor(self):
        return sum(1 for slot in self.values if slot is not None) / (
            self.size_table * self.charge_factor
        )

    def hash_function(self, key):
        """
        Generates hash for the given key value
        """
        return key % self.size_table

    def _step_by_step(self, step_ord):
        print(f"step {step_ord}")
        print(list(range(len(self.values))))
        print(self.values)

    def bulk_insert(self, values: Iterable):
        """
        bulk_insert is used for entering more than one element at a time
        in the HashTable.
        """
        i = 1
        self.__aux_list = values
        for value in values:
            self.insert_data(value)
            self._step_by_step(i)
            i += 1

    def _set_value(self, key, data):
        """
        _set_value functions allows to update value at a particular hash
        """
        self.values[key] = data
        self._keys[key] = data

    def _collision_resolution(self, key, data=None):
        """
        This method is a type of open addressing which is used for handling collision.

        In this implementation the concept of linear probing has been used.

        The hash table is searched sequentially from the original location of the
        hash, if the new hash/location we get is already occupied we check for the next
        hash/location.
        """
        new_key = self.hash_function(key + 1)

        while self.values[new_key] is not None and self.values[new_key] != key:
            if self.values.count(None) > 0:
                new_key = self.hash_function(new_key + 1)
            else:
                new_key = None
                break

        return new_key

    def rehashing(self):
        survivor_values = [value for value in self.values if value is not None]
        self.size_table = next_prime(self.size_table, factor=2)
        self._keys.clear()
        # hell's pointers D: don't DRY ;/
        self.values = [None] * self.size_table
        for value in survivor_values:
            self.insert_data(value)

    def insert_data(self, data):
        """
        insert_data is used for inserting a single element at a time in the HashTable.

        Examples:

        >>> ht = HashTable(3)
        >>> ht.insert_data(5)
        >>> ht.keys()
        {2: 5}
        >>> ht = HashTable(5)
        >>> ht.insert_data(30)
        >>> ht.insert_data(50)
        >>> ht.keys()
        {0: 30, 1: 50}
        """
        key = self.hash_function(data)

        if self.values[key] is None:
            self._set_value(key, data)

        elif self.values[key] == data:
            pass

        else:
            collision_resolution = self._collision_resolution(key, data)
            if collision_resolution is not None:
                self._set_value(collision_resolution, data)
            else:
                self.rehashing()
                self.insert_data(data)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    ht = HashTable(5)
    ht.insert_data(10)
    ht.insert_data(20)
    ht.insert_data(30)
    ht.keys()
    ht.bulk_insert((10, 20, 30))
