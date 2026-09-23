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
                  
    async def close(self):
        if self.connection:
            await self.connection.close()

    # Class constructor.
    @classmethod
    async def create(cls, database_name):
        connection = await aiosqlite.connect(database_name)
        instance = cls(connection)
        await instance.execute("PRAGMA foreign_keys = ON;")
        await instance.execute("""
                        CREATE TABLE IF NOT EXISTS server (
                            id INTEGER PRIMARY KEY NOT NULL,
                            name TEXT NOT NULL
                        );
                    """)
        await instance.execute("""
                        CREATE TABLE IF NOT EXISTS groups (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            group_hash CHAR(64) NOT NULL UNIQUE
                        );
                    """)
        await instance.execute("""
                        CREATE TABLE IF NOT EXISTS server_groups (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            server_id INTEGER NOT NULL,
                            server_owner_id INTEGER NOT NULL,
                            group_id INTEGER NOT NULL
                        );
                    """)
        await instance.execute("""
                        CREATE TABLE IF NOT EXISTS punishments (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            display_id INTEGER NOT NULL,
                            server_id INTEGER NOT NULL,
                            group_id INTEGER NOT NULL,
                            banned_user_id INTEGER NOT NULL
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
            return await cursor.fetchone()

    # Execute a SQL query, returns all the matched results.
    async def execute_and_fetch_all(self, query: str, parameters: tuple = ()):
        async with self.connection.execute(query, parameters) as cursor:
            return await cursor.fetchall()
    async def insert_server(self, server_name, server_id):
        await self.execute("""
                               INSERT INTO servers VALUES (?, ?)
                           """, (server_id, server_name))

    async def create_group(self, group_name: str, group_hash: str):
        await self.execute("""
                               INSERT INTO groups (name, group_hash) VALUES (?, ?)
                           """, (group_name, group_hash))
    async def create_punishment(self, display_id: int, user_id: int, server_id: int, group_id: int):
        await self.execute("""
                               INSERT INTO punishments (display_id, server_id, group_id, banned_user_id) VALUES (?, ?, ?, ?)
                           """, (display_id, server_id, group_id, user_id))
