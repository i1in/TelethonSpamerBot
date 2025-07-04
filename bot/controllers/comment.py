from typing import Union
from ..database.database import Database


class CommentQueries:

    def __init__(self, db: Database):
        self.db = db

    async def add_comment_text(self, comment_text: str) -> bool:
        result = await self.db.fetch_one("SELECT EXISTS(SELECT 1 FROM comment_text WHERE comment = ?)", (comment_text, ))
        
        if result[0] == 1 and result is not None:
            return False
        
        await self.db.execute(
            """
            UPDATE comment_text SET comment = ? WHERE id = 1
            """,
            params=(
                comment_text,
            )
        )

        return True

    async def get_comment_text(self) -> Union[bool, str]:
        result = await self.db.fetch_one(
            "SELECT comment FROM comment_text WHERE id = 1", 
            params=())
        
        if result is None:
            return False
        
        return result[0]