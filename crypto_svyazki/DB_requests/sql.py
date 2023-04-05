import aiomysql
import ast
import time
import datetime

class DateBase:
    def __init__(self):
        self.pool = None
    async def create(self):
        pool = await aiomysql.create_pool(host='localhost', port=3306,
                                        user='Nursyka', password='1234',
                                        db='crypto_bot')
        self.pool = pool

    async def check_user(self,user_id):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
               
                await cur.execute(f'SELECT `ID` FROM `user` WHERE `ID` = "{user_id}";')
                result = await cur.fetchall()
                if not result:
                    return True
    async def add_user(self,user_id,tag_user):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(f'INSERT INTO `user` (`ID`,`tag`) VALUES ("{user_id}","{tag_user}") ;')
                await conn.commit()                    
    
    async def get_status_subscribe(self , user_id):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
               
                await cur.execute(f'SELECT `subscribe` FROM `user` WHERE `ID` = "{user_id}";')
                result = await cur.fetchall()
                if result[0][0] == "Подписка не активна" or int(time.time()) > int(result[0][0]):
                    return False     
                return True
            
    async def get_user_info(self , user_id):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
               
                await cur.execute(f'SELECT `procent`,`reg_user` FROM `user` WHERE `ID` = "{user_id}";')
                result = await cur.fetchall()
                print(result)
                return result[0]
                
    async def full_info_subscribe(self , user_id):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(f'SELECT `subscribe` FROM `user` WHERE `ID` = "{user_id}";')
                result = await cur.fetchall()
                if result[0][0] == "Подписка не активна" or int(time.time()) > int(result[0][0])  :
                    return "❌","Подписка не активна"
                else:
                    return "✅",datetime.datetime.fromtimestamp(int(result[0][0])).strftime('%Y-%m-%d %H:%M')
                
    async def update_procent_user(self,user_id,text):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await conn.begin()
                    await cur.execute(f'UPDATE `user` SET `procent` = "'+str(text)+'" WHERE `ID` LIKE "'+str(user_id)+'";')
                    await conn.commit()
                except:
                    pass
     
    