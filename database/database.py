#
# Copyright 2026 Krypton Yousuke.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import aiosqlite
import aioconsole
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
                        CREATE TABLE IF NOT EXISTS servers (
                            id INTEGER PRIMARY KEY NOT NULL,
                            name TEXT NOT NULL
                        );
                    """)
        await instance.execute("""
                        CREATE TABLE IF NOT EXISTS groups (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            server_owner_id INTEGER NOT NULL,
                            group_hash CHAR(64) NOT NULL UNIQUE,
                            FOREIGN KEY (server_owner_id) REFERENCES servers (id) ON DELETE CASCADE
                        );
                    """)
        await instance.execute("""
                        CREATE TABLE IF NOT EXISTS server_groups (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            server_id INTEGER NOT NULL,
                            group_id INTEGER NOT NULL,
                            FOREIGN KEY (group_id) REFERENCES groups (id) ON DELETE CASCADE,
                            FOREIGN KEY (server_id) REFERENCES servers (id) ON DELETE CASCADE,
                            UNIQUE (server_id, group_id)
                        );
                    """)
        await instance.execute("""
                        CREATE TABLE IF NOT EXISTS punishments (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            display_id INTEGER NOT NULL,
                            server_id INTEGER NOT NULL,
                            group_id INTEGER NOT NULL,
                            banned_user_id INTEGER NOT NULL,
                            reason TEXT NOT NULL,
                            FOREIGN KEY (group_id) REFERENCES groups (id) ON DELETE CASCADE,
                            FOREIGN KEY (server_id) REFERENCES servers (id) ON DELETE CASCADE
                        );
                    """)
        

        return instance


    #########################################################
    #             Internal Database Handling                #
    #########################################################
    # Execute a SQL query, returns None.
    async def execute(self, query: str, parameters: tuple = ()):
        async with await self.connection.execute(query, parameters) as cursor:
            await self.connection.commit()
            return cursor.lastrowid

    # Execute a SQL query, returns the first match.
    async def execute_and_fetch(self, query: str, parameters: tuple = ()):
        async with self.connection.execute(query, parameters) as cursor:
            return await cursor.fetchone()

    # Execute a SQL query, returns all the matched results.
    async def execute_and_fetch_all(self, query: str, parameters: tuple = ()):
        async with self.connection.execute(query, parameters) as cursor:
            return await cursor.fetchall()

    #########################################################
    #                  Application Queries                  #
    #########################################################

    async def insert_server(self, server_name: str, server_id: int):
        await self.execute("""
                               INSERT INTO servers VALUES (?, ?)
                           """, (server_id, server_name))

    async def create_group(self, group_name: str, server_id: int, group_hash: str):
        row_id = await self.execute("""
                               INSERT INTO groups (name, server_owner_id, group_hash) VALUES (?, ?, ?)
                           """, (group_name, server_id, group_hash))
        await self.execute("""
                               INSERT INTO server_groups (server_id, group_id) VALUES (?, ?)
                           """, (server_id, row_id))

    async def fetch_server_by_id(self, server_id: int) -> dict :
        result = await self.execute_and_fetch("""
                                                SELECT * FROM servers WHERE id = (?)
                                            """, (server_id,))
        formatted_result = {
            "id": result[0],
            "name": result[1]
        }
        
        return formatted_result
    
    async def fetch_groups(self, server_id: int) -> dict:
        results = await self.execute_and_fetch_all("""
                                                    SELECT * FROM server_groups WHERE server_id = (?)
                                                """, (server_id,))
        formatted_results = []
        for result in results:
            result = {
                "id": result[0],
                "server_id": result[1],
                "group_id": result[2]
            }
            formatted_results.append(result)
        return formatted_results


    async def fetch_group_by_id(self, group_id: int):
        result = await self.execute_and_fetch("""
                                                SELECT * FROM groups WHERE id = (?)
                                            """, (group_id,))
        formatted_result = {
            "id": result[0],
            "name": result[1],
            "server_owner_id": result[2],
            "group_hash": result[3]
        }
        return formatted_result


    async def create_punishment(self, display_id: int, user_id: int, server_id: int, group_id: int):
        await self.execute("""
                               INSERT INTO punishments (display_id, server_id, group_id, banned_user_id) VALUES (?, ?, ?, ?)
                           """, (display_id, server_id, group_id, user_id))
