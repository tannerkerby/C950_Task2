class HashTable:
    def __init__(self, size=40):
        # create empty list table
        self.table = []
        # create empty buckets in the table
        for i in range(size):
            self.table.append([])

    # insert a new value into the hash table
    def insert(self, key, value):
        # calculate a hash function for which bucket this value will be inserted into
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # if the key is found in the list, update it.
        #  If a collision occurs (i.e., if the key already exists in the bucket list), the new key-value pair
        #  is appended to the end of the list.
        for key_value in bucket_list:
            if key_value[0] == key:
                key_value[1] = value
                return True
        # if they key isn't found in the list already, append the key value pair to the bucket
        key_value = [key, value]
        bucket_list.append(key_value)

    def search(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # search for the key in the buckets. If the key isn't found, return None
        for key_value in bucket_list:
            if key_value[0] == key:
                return key_value[1]
        return None

    def delete(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        # if they key is found in a bucket, remove the list with that key.
        for i, key_value in enumerate(bucket_list):
            if key_value[0] == key:
                deleted_item = bucket_list.pop(i)
                return deleted_item
        return None  # return None if the item is not found

    def as_list(self):
        all_items = []
        for entry in self.table:
            if entry is not None:
                all_items.extend(entry)
        return all_items

# myHash = HashTable()
# p1arr = ['Tanner', 'Kerby', 'New York']
# myHash.insert(1, p1arr)
# print(myHash.table)