from ..database.database import Database

class DataService:

    def __init__(self, db: Database):
        self.db = db

    @classmethod
    async def create(cls, db):
        self = cls(db)
        await self._init_table()
        await self._insert_comment()
        return self

    async def _init_table(self):
        await self.db.execute(
            """
            CREATE TABLE if NOT EXISTS channel (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                channel_id INTEGER UNIQUE,
                channel_name TEXT,
                channel_url TEXT,
                added_at INTEGER DEFAULT (strftime('%s', 'now'))
            );
            """,
            params=()
        )
        await self.db.execute(
            """
            CREATE TABLE if NOT EXISTS comment_text (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                comment TEXT DEFAULT 'example',
                added_at INTEGER DEFAULT (strftime('%s', 'now'))
            );
            """,
            params=()
        )

    async def _insert_comment(self):
        await self.db.execute(
            """
            INSERT INTO comment_text DEFAULT VALUES
            """,
            params=()
        )