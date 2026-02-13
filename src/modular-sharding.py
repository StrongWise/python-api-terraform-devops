import hashlib

class Database:
    def __init__(self, name):
        self.name = name

    def execute(self, query):
        print(f"Executing query on {self.name}: {query}")

class ModularShardingRouter:
    def __init__(self, shards):
        self.shards = shards
        self.num_shards = len(shards)

    def get_shard(self, key):
        # 해시 기반 샤딩: key(user_id 등)의 해시 값을 기반으로 샤드 선택
        shard_index = self.hash_key(key) % self.num_shards
        return self.shards[shard_index]

    def hash_key(self, key):
        # 해시 값을 계산하여 샤드 인덱스 결정
        return int(hashlib.md5(str(key).encode()).hexdigest(), 16)

class Repository:
    def __init__(self, sharding_router):
        self.sharding_router = sharding_router

    def write_query(self, key, query):
        shard = self.sharding_router.get_shard(key)
        shard.execute(query)

    def read_query(self, key, query):
        shard = self.sharding_router.get_shard(key)
        shard.execute(query)

shard_1 = Database("shardDB1")
shard_2 = Database("shardDB2")
shard_3 = Database("shardDB3")

sharding_router = ModularShardingRouter([shard_1,shard_2,shard_3])
repository = Repository(sharding_router)

repository.write_query(1001, "INSERT INTO post(key, data) VALUES (1001, '1001')")
repository.write_query(2003, "INSERT INTO post(key, data) VALUES (2003, '2003')")
repository.write_query(3007, "INSERT INTO post(key, data) VALUES (3007, '3007')")

repository.read_query(1001, "SELECT * FROM post WHERE key=1001")
repository.read_query(2003, "SELECT * FROM post WHERE key=2003")
repository.read_query(3007, "SELECT * FROM post WHERE key=3007")

