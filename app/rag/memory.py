from app.db.postgres import get_pool

async def get_or_create_session(session_id: str | None) -> str:
    # if session_id is None, create new conversation row, return new session_id
    pool = get_pool()
    
    if session_id is None:
        async with pool.acquire() as conn:
            new_id = await conn.fetch("INSERT INTO conversations DEFAULT VALUES RETURNING session_id")
        return str(new_id)
    else:
        async with pool.acquire() as conn:
            await conn.execute("UPDATE conversations SET last_active = NOW() WHERE session_id = $1",
                session_id)
        return session_id


    # if session_id exists, update last_active, return it

async def save_message(session_id: str, role: str, content: str) -> None:
    # insert into messages table
    pool = get_pool()

    async with pool.acquire() as conn:
        save_message_query = "INSERT INTO messages(session_id, role, content) " \
            "VALUES ($1, $2, $3);"

        await conn.execute(save_message_query, session_id, role, content)

async def get_history(session_id: str, limit: int = 10) -> list[dict]:
    # fetch last N messages for session
    # return list of {role, content}
    pool = get_pool()
    
    async with pool.acquire() as conn:
        query = "SELECT role, content FROM messages " \
            "WHERE session_id = $1 " \
            "ORDER BY created_at ASC " \
            "LIMIT $2"

        rows = await conn.fetch(query, session_id, limit)

    return [{"role": row["role"], "content": row["content"]} for row in rows] 

