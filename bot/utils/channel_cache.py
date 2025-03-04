import asyncio, time
from channels import ChannelQueries

# Сборщик кэша (если записей становится слишком много)
class ChannelCacheManager:
    def __init__(self, update_interval: int = 60, db: ChannelQueries = None):
        self.allowed_channels = set()
        self.update_interval = update_interval
        self.db = db
        self.last_update = 0
        self._task = None

    async def _update_cache(self):
        while True:
            new_channels = set(i[0] for i in await self.db.get_all_channels())
            self.allowed_channels = new_channels
            self.last_update = time.time()
            print(f"[Cache] Updated at {self.last_update}: {self.allowed_channels}")
            await asyncio.sleep(self.update_interval)

    def start(self):
        if self._task is None or self._task.done():
            self._task = asyncio.create_task(self._update_cache())

channel_cache_manager = ChannelCacheManager(update_interval=60)
channel_cache_manager.start()