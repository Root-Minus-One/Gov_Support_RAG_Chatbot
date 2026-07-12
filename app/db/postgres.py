import asyncpg
import asyncio
from app.core.config import settings


async def main():
    connection = await asyncpg.connect(dsn=settings.DATABASE_URL.get_secret_value())
    
    try:
        result = await connection.fetchval("SELECT NOW()")
        print(result)


    finally:
        await connection.close()


_pool = None


async def init_pool():
    global _pool
    _pool = await asyncpg.create_pool(
        dsn=settings.DATABASE_URL.get_secret_value(),
        min_size=5,
        max_size=10
    )
         
    return _pool


async def close_pool():
    global _pool
    if _pool is not None:
        await _pool.close()
    _pool = None



def get_pool():
    global _pool
    if _pool is None:
        raise RuntimeError("Pool not initialized")
    return _pool




if __name__ == "__main__":
    asyncio.run(main())