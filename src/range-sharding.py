class Database:
    def __init__(self, name):
        self.name = name

    def execute(self, query):
        print(f"Executing query on {self.name}: {query}")

class RangeShardingRouter:
    def __init__(self, shard_ranges):
        # shard_ranges: [(shard, min_range, max_range)]
        self.shard_ranges = shard_ranges

    def get_shard(self, key):
        for shard, min_range, max_range in self.shard_ranges:
            if min_range <= key <= max_range:
                return shard
        raise ValueError(f"No shard found for key: {key}")

class Repository:
    def __init__(self, sharding_router):
        self.sharding_router = sharding_router

    def write_query(self, key, query):
        shard = self.sharding_router.get_shard(key)
        shard.execute(query)

    def read_query(self, key, query):
        shard = self.sharding_router.get_shard(key)
        shard.execute(query)

shard_1 = Database("shard_1")
shard_2 = Database("shard_2")
shard_3 = Database("shard_3")

sharding_router = RangeShardingRouter([
    (shard_1, 0, 1000),
    (shard_2, 1001, 2000),
    (shard_3, 2002, 3000)
])

repository = Repository(sharding_router)

repository.write_query(500, "INSERT INTO post(key, data) VALUES (500, '500')")
repository.write_query(1500, "INSERT INTO post(key, data) VALUES (1500, '1500')")
repository.write_query(2500, "INSERT INTO post(key, data) VALUES (2500, '2500')")

repository.read_query(500, "SELECT * FROM post WHERE key=500")
repository.read_query(1500, "SELECT * FROM post WHERE key=1500")
repository.read_query(2500, "SELECT * FROM post WHERE key=2500")

