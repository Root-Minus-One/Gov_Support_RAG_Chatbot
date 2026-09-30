from app.db.postgres import get_pool

import uuid

async def get_or_create_session(session_id: str | None = None) -> str:
    pool = get_pool()
    
    async with pool.acquire() as conn:
        # 1. If a valid UUID string was passed, try to update existing session
        if session_id:
            try:
                valid_uuid = uuid.UUID(session_id)
                status = await conn.execute(
                    "UPDATE conversations SET last_active = NOW() WHERE session_id = $1",
                    valid_uuid
                )
                # Check if a row was actually updated
                if status != "UPDATE 0":
                    return str(valid_uuid)
            except (ValueError, TypeError):
                pass  # Fallback to creating a new row if invalid UUID passed

        # 2. If no valid session exists, insert without providing session_id so PostgreSQL uses gen_random_uuid()
        new_session_id = await conn.fetchval("""
            INSERT INTO conversations DEFAULT VALUES 
            RETURNING session_id;
        """)

        return str(new_session_id)


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

