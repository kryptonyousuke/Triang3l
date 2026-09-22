#
# Copyright 2026 Krypton Yousuke.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import aiosqlite

# Triang3l database.
class Database:
    def __init__(self, connection: aiosqlite.Connection):
        self.connection = connection
                  
    async def __aenter__(self):
        return self
    async def __aexit__(self, exc_type, exc_value, traceback):
        if self.connection:
             await self.connection.close()

    # Class constructor.
    @classmethod
    async def create(cls, database_name):
        connection = await aiosqlite.connect(database_name)
        instance = cls(connection)
        await instance.execute("""
                        CREATE TABLE IF NOT EXISTS servers (
                            id INTEGER PRIMARY KEY,
                            name TEXT
                        );
                    """)
        await instance.execute("""
                        CREATE TABLE IF NOT EXISTS groups (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            owner_id INTEGER,
                            members TEXT,
                            invite_hash CHAR(32)
                        );
                    """)

        return instance

    # Execute a SQL query, returns None.
    async def execute(self, query: str, parameters: tuple = ()):
        await self.connection.execute(query, parameters)
        await self.connection.commit()

    # Execute a SQL query, returns the first match.
    async def execute_and_fetch(self, query: str, parameters: tuple = ()):
        async with self.connection.execute(query, parameters) as cursor:
            await self.connection.commit()
            return await cursor.fetchone()

    # Execute a SQL query, returns all the matched results.
    async def execute_and_fetch_all(self, query: str, parameters: tuple = ()):
        async with self.connection.execute(query, parameters) as cursor:
            await self.connection.commit()
            return await cursor.fetchall()
