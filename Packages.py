class Packages:
    """
    Custom hash table used to store and retrieve Package objects
    by their unique package ID.
    """

    def __init__(self, capacity):
        """
        Creates the hash table with the requested number of buckets.

        @param capacity: Number of buckets used by the hash table.
        """

        self.capacity = capacity
        self.table = []

        # Create an empty list for each bucket.
        # Separate chaining is used to handle hash collisions.
        for i in range(capacity):
            self.table.append([])

    def _hash(self, package_id):
        """
        Calculates the bucket index for a package ID.

        @param package_id: Unique package ID used as the key.
        @return: Integer index of the bucket where the package belongs.
        """

        return package_id % self.capacity

    def insert(self, package_id, package):
        """
        Inserts or updates a package in the hash table.

        @param package_id: Unique package ID used as the hash table key.
        @param package: Package object containing the required delivery data.
        """

        bucket_index = self._hash(package_id)
        bucket = self.table[bucket_index]

        # Search the bucket to determine whether the package
        # already exists. If found, update the stored package.
        for pair in bucket:
            if pair[0] == package_id:
                pair[1] = package
                return

        # If the package is not already stored, append a
        # new key/value pair to the bucket.
        bucket.append([package_id, package])

    def lookup(self, package_id):
        """
        Looks up a package using its unique package ID.

        @param package_id: Unique package ID to search for.
        @return: Matching Package object, or None if not found.
        """

        bucket_index = self._hash(package_id)
        bucket = self.table[bucket_index]

        # Search only the bucket produced by the hash function.
        for pair in bucket:
            if pair[0] == package_id:
                return pair[1]

        return None

    def get_all(self):
        """
        Returns every package stored in the hash table.

        @return: List containing all stored Package objects.
        """

        packages = []

        # Iterate through every bucket and collect the
        # Package object from each key/value pair.
        for bucket in self.table:
            for pair in bucket:
                packages.append(pair[1])

        return packages

    def remove(self, package_id):
        """
        Removes a package from the hash table.

        @param package_id: Unique package ID to remove.
        @return: True if removed, otherwise False.
        """

        bucket_index = self._hash(package_id)
        bucket = self.table[bucket_index]

        for pair in bucket:
            if pair[0] == package_id:
                bucket.remove(pair)
                return True

        return False

    def size(self):
        """
        Returns the number of packages currently stored.

        @return: Total number of Package objects in the hash table.
        """

        count = 0

        for bucket in self.table:
            count += len(bucket)

        return count