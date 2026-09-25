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
                        CREATE TABLE IF NOT EXISTS servers (
                            id INTEGER PRIMARY KEY NOT NULL UNIQUE
                        );
                    """)
        await instance.execute("""
                        CREATE TABLE IF NOT EXISTS groups (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            server_owner_id INTEGER NOT NULL,
                            greater_punishment_display_id INTEGER NOT NULL,
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
                            display_name TEXT,
                            username TEXT,
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

    async def insert_server(self, server_id: int):
        await self.execute("""
                               INSERT INTO servers VALUES (?)
                           """, (server_id,))

    async def create_group(self, group_name: str, server_id: int, group_hash: str):
        row_id = await self.execute("""
                               INSERT INTO groups (name, server_owner_id, greater_punishment_display_id, group_hash) VALUES (?, ?, ?, ?)
                           """, (group_name, server_id, 0, group_hash))
        await self.execute("""
                               INSERT INTO server_groups (server_id, group_id) VALUES (?, ?)
                           """, (server_id, row_id))

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
            "name": result[1] ,
            "server_owner_id": result[2],
            "greater_punishment_display_id": result[3],
            "group_hash": result[4]
        }
        return formatted_result



    async def create_punishment(self, user_id: int, display_name: str, username: str, reason: str, server_id: int, group_id: int):
        await self.execute("""
                               INSERT INTO punishments (display_id, server_id, group_id, display_name, username, reason, banned_user_id) VALUES (?, ?, ?, ?, ?, ?, ?)
                           """, ((await self.fetch_group_by_id(group_id))["greater_punishment_display_id"] + 1, server_id, group_id, display_name, username, reason, user_id))

