from Package import Package


class Packages:
    def __init__(self, capacity):
        self.capacity = capacity
        self.table = []

        # Create empty buckets for the hash table.
        for i in range(capacity):
            self.table.append([])

    def _hash(self, package_id):
        return package_id % self.capacity

    def insert(self, package_id, package):
        bucket_index = self._hash(package_id)
        bucket = self.table[bucket_index]

        # If the package already exists, update it.
        for pair in bucket:
            if pair[0] == package_id:
                pair[1] = package
                return

        # Otherwise, insert a new key/value pair.
        bucket.append([package_id, package])

    def lookup(self, package_id):
        bucket_index = self._hash(package_id)
        bucket = self.table[bucket_index]

        # Search the bucket for the matching package ID.
        for pair in bucket:
            if pair[0] == package_id:
                return pair[1]

        return None

    def get_all(self):
        packages = []

        # Collect all Package objects from every bucket.
        for bucket in self.table:
            for pair in bucket:
                packages.append(pair[1])

        return packages

    def remove(self, package_id):
        bucket_index = self._hash(package_id)
        bucket = self.table[bucket_index]

        for pair in bucket:
            if pair[0] == package_id:
                bucket.remove(pair)
                return True

        return False

    def size(self):
        count = 0

        for bucket in self.table:
            count += len(bucket)

        return count