class DatabaseRouter:
    def __init__(self, primary_db, replica_dbs):
        self.primary_db = primary_db # 메인 DB (White 용)
        self.replica_db = replica_dbs # 복제 DB 리스트 (Read Only 용)
        self.replica_index = 0
        self.replica_count = len(replica_dbs)

    def get_primary_db(self):
        """Primary DB (Write operation)"""
        return self.primary_db

    def get_replica_db(self):
        """Replica DB (Read operation) with simple round-robin load balancing"""
        db = self.replica_db[self.replica_index]
        # 읽기 DB를 가져갈 때마다 인덱스 번호 1씩 올리면서 라운드로빈 방식으로 읽기 분배
        # 가중치를 부여해 특정 서버에 집중 가능
        self.replica_index = (self.replica_index + 1) % self.replica_count
        return db

class Database:
    def __init__(self, name):
        self.name = name

    def execute(self, query, write=False):
        """Execute a query on the database"""
        print(f"Executing query on {self.name}: {query}")

class Repository:
    def __init__(self, db_router):
        self.db_router = db_router

    def write_query(self, query):
        """White operations go to the primary database"""
        self.db_router.get_primary_db().execute(query, write=True)

    def read_query(self, query):
        """Read operations go to a replica database"""
        self.db_router.get_replica_db().execute(query, write=False)

primary_db = Database("primary")
replica_dbs = [Database("replica1"), Database("replica2")]

db_router = DatabaseRouter(primary_db, replica_dbs)
repository = Repository(db_router)

# 메인 DB에 쓰기
repository.write_query("INSERT INTO users (id) VALUES (1)")

# 라운드로빈 방식으로 읽기 복제본으로부터 읽기
repository.read_query("SELECT * FROM users WHERE id=1")
repository.read_query("SELECT * FROM users WHERE id=2")
repository.read_query("SELECT * FROM users WHERE id=3")


