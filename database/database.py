#
# Copyright 2026 Krypton Yousuke.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import aiosqlite

class Database:
    def __init__(self, connection: aiosqlite.Connection):
        self.connection = connection
    async def __aenter__(self):
        return self
    async def __aexit__(self, exc_type, exc_value, traceback):
        if self.connection:
             await self.close()

    @classmethod
    async def create(cls, database_name):
        connection = await aiosqlite.connect(database_name)
        return cls(connection)

    async def execute(self, query: str, parameters: tuple):
        await self.connection.execute(query, parameters)
        await self.connection.commit()


    async def execute_and_fetch(self, query: str, parameters: tuple):
        async with self.connection.execute(query, parameters) as cursor:
            await self.connection.commit()
            return await cursor.fetchall()
    
    async def execute_and_fetch_one(self, query: str, parameters: tuple):
        async with self.connection.execute(query, parameters) as cursor:
            await self.connection.commit()
            return await cursor.fetchone()
    


    async def close(self):
        await self.cursor.close()
        await self.connection.close()
