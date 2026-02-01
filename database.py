import aiosqlite
import os
from datetime import datetime
from typing import List, Dict, Optional

DATABASE_FILE = os.getenv('DATABASE_FILE', 'pyclaw.db')

class Database:
    def __init__(self, db_file=DATABASE_FILE):
        self.db_file = db_file
    
    async def init_db(self):
        """Initialize database with schema"""
        async with aiosqlite.connect(self.db_file) as db:
            with open('schema.sql', 'r') as f:
                await db.executescript(f.read())
            await db.commit()
    
    # KNOWLEDGE BASE
    async def store_knowledge(self, user_id: str, topic: str, content: str):
        """Store a fact for a user"""
        async with aiosqlite.connect(self.db_file) as db:
            await db.execute(
                "INSERT OR REPLACE INTO knowledge (user_id, topic, content) VALUES (?, ?, ?)",
                (user_id, topic.lower(), content)
            )
            await db.commit()
    
    async def recall_knowledge(self, user_id: str, topic: str) -> Optional[str]:
        """Retrieve a fact"""
        async with aiosqlite.connect(self.db_file) as db:
            async with db.execute(
                "SELECT content FROM knowledge WHERE user_id = ? AND topic = ?",
                (user_id, topic.lower())
            ) as cursor:
                row = await cursor.fetchone()
                return row[0] if row else None
    
    async def forget_knowledge(self, user_id: str, topic: str) -> bool:
        """Delete a fact"""
        async with aiosqlite.connect(self.db_file) as db:
            cursor = await db.execute(
                "DELETE FROM knowledge WHERE user_id = ? AND topic = ?",
                (user_id, topic.lower())
            )
            await db.commit()
            return cursor.rowcount > 0
    
    async def list_knowledge(self, user_id: str) -> List[str]:
        """List all topics user has stored"""
        async with aiosqlite.connect(self.db_file) as db:
            async with db.execute(
                "SELECT topic FROM knowledge WHERE user_id = ? ORDER BY created_at DESC",
                (user_id,)
            ) as cursor:
                rows = await cursor.fetchall()
                return [row[0] for row in rows]
    
    # CONVERSATION HISTORY
    async def add_message(self, user_id: str, role: str, content: str, agent: str = 'friendly'):
        """Add message to conversation history"""
        async with aiosqlite.connect(self.db_file) as db:
            await db.execute(
                "INSERT INTO conversations (user_id, role, content, agent) VALUES (?, ?, ?, ?)",
                (user_id, role, content, agent)
            )
            await db.commit()
            
            # Keep only last 20 messages per user
            await db.execute(
                """DELETE FROM conversations WHERE id IN (
                    SELECT id FROM conversations WHERE user_id = ?
                    ORDER BY created_at DESC LIMIT -1 OFFSET 20
                )""",
                (user_id,)
            )
            await db.commit()
    
    async def get_conversation_history(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Get recent conversation history"""
        async with aiosqlite.connect(self.db_file) as db:
            async with db.execute(
                """SELECT role, content, agent FROM conversations 
                   WHERE user_id = ? ORDER BY created_at DESC LIMIT ?""",
                (user_id, limit)
            ) as cursor:
                rows = await cursor.fetchall()
                return [{'role': r[0], 'content': r[1], 'agent': r[2]} for r in reversed(rows)]
    
    async def clear_conversation(self, user_id: str):
        """Clear user's conversation history"""
        async with aiosqlite.connect(self.db_file) as db:
            await db.execute("DELETE FROM conversations WHERE user_id = ?", (user_id,))
            await db.commit()
    
    # USER SETTINGS
    async def get_active_agent(self, user_id: str) -> str:
        """Get user's active agent"""
        async with aiosqlite.connect(self.db_file) as db:
            async with db.execute(
                "SELECT active_agent FROM user_settings WHERE user_id = ?",
                (user_id,)
            ) as cursor:
                row = await cursor.fetchone()
                return row[0] if row else 'friendly'
    
    async def set_active_agent(self, user_id: str, agent: str):
        """Set user's active agent"""
        async with aiosqlite.connect(self.db_file) as db:
            await db.execute(
                """INSERT INTO user_settings (user_id, active_agent) VALUES (?, ?)
                   ON CONFLICT(user_id) DO UPDATE SET active_agent = ?""",
                (user_id, agent, agent)
            )
            await db.commit()
    
    async def get_auto_post(self, user_id: str) -> bool:
        """Check if auto-post is enabled"""
        async with aiosqlite.connect(self.db_file) as db:
            async with db.execute(
                "SELECT auto_post_moltbook FROM user_settings WHERE user_id = ?",
                (user_id,)
            ) as cursor:
                row = await cursor.fetchone()
                return bool(row[0]) if row else False
    
    async def set_auto_post(self, user_id: str, enabled: bool):
        """Toggle auto-post to Moltbook"""
        async with aiosqlite.connect(self.db_file) as db:
            await db.execute(
                """INSERT INTO user_settings (user_id, auto_post_moltbook) VALUES (?, ?)
                   ON CONFLICT(user_id) DO UPDATE SET auto_post_moltbook = ?""",
                (user_id, int(enabled), int(enabled))
            )
            await db.commit()
    
    # MODERATION
    async def log_moderation(self, user_id: str, message: str, reason: str):
        """Log moderation event"""
        async with aiosqlite.connect(self.db_file) as db:
            await db.execute(
                "INSERT INTO moderation_log (user_id, message, flagged_reason) VALUES (?, ?, ?)",
                (user_id, message, reason)
            )
            await db.commit()
