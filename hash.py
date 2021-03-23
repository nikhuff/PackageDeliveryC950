# simple hash table class to be used to carry packages with a unique id
# used Ch. 7.8 in zyBooks as reference
class HashTable:
    """
    Hash Table to facilitate storage and lookup of packages
    Can assume unique ids and correct size since its a specialized hash used only for this purpose
    """
    def __init__(self, size=40):
        # assume unique ids and size of hash is exact number of packages
        self.table = [None]*size

    def insert(self, id, package):
        # get the bucket
        bucket = id % len(self.table)

        # insert the package into the bucket
        self.table[bucket] = package

    def search(self, key):
        # get the bucket
        bucket = key % len(self.table)

        # return item
        return self.table[bucket]

    def remove(self, key):
        # get the bucket
        bucket = key % len(self.table)

        # remove item
        del self.table[bucket]
