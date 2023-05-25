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
     
    async def get_all_users_info(self):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await conn.begin()
                    await cur.execute(f'SELECT `ID`,`procent`,`subscribe`,`last_svyazka`;')
                    result = await cur.fetchall()
                    return result[0]
                except:
                    pass        

    async def delete_subscribe(self , user_id ):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await conn.begin()
                    await cur.execute(f'UPDATE `user` SET `procent` = "'+str("Не установлен")+'" WHERE `ID` LIKE "'+str(user_id)+'";')
                    await conn.commit()

                    await conn.begin()
                    await cur.execute(f'UPDATE `user` SET `subscribe` = "'+str("Подписка не активна")+'" WHERE `ID` LIKE "'+str(user_id)+'";')
                    await conn.commit()
                except:
                    pass  
    async def get_all_users_info(self):
            pool = await aiomysql.create_pool(host='localhost', port=3306,
                                            user='Nursyka', password='1234',
                                            db='crypto_bot') 
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    try:
                        await conn.begin()
                        await cur.execute(f'SELECT `ID`,`procent`,`subscribe`,`last_svyazka`FROM `user` ;')
                        result = await cur.fetchall()
                        return result
                    except:
                        pass     

    async def add_lst_sv(self, user_id , svyazka):
            pool = await aiomysql.create_pool(host='localhost', port=3306,
                                            user='Nursyka', password='1234',
                                            db='crypto_bot') 
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    try:
                        await conn.begin()
                        await cur.execute(f'UPDATE `user` SET `last_svyazka` = "'+str(svyazka)+'" WHERE `ID` LIKE "'+str(user_id)+'";')
                        await conn.commit()
                    except:
                        pass      

    async def get_user_metod(self,user_id):
            pool = await aiomysql.create_pool(host='localhost', port=3306,
                                            user='Nursyka', password='1234',
                                            db='crypto_bot') 
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    try:
                        await conn.begin()
                        await cur.execute(f'SELECT `metod` FROM `user` WHERE `ID` = "{user_id}";')
                        result = await cur.fetchall()
                        return result[0][0]
                    except:
                        pass
    async def change_metod(self,user_id):
            pool = await aiomysql.create_pool(host='localhost', port=3306,
                                            user='Nursyka', password='1234',
                                            db='crypto_bot') 
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    try:
                        await conn.begin()
                        await cur.execute(f'SELECT `metod` FROM `user` WHERE `ID` = "{user_id}";')
                        result = await cur.fetchall()
                        result = result[0][0]
                        if result == ["M","V"][0]:
                            result = "V"
                        else:
                            result = "M"
                        await cur.execute(f'UPDATE `user` SET `metod` = "'+str(result)+'" WHERE `ID` LIKE "'+str(user_id)+'";')
                        await conn.commit()
                        print(result)
                        # return result[0][0]
                    except:
                        pass
    async def add_ban_token(self,user_id,token_name):
            pool = await aiomysql.create_pool(host='localhost', port=3306,
                                            user='Nursyka', password='1234',
                                            db='crypto_bot') 
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    try:
                        await cur.execute(f'SELECT `ban_token` FROM `user` WHERE `ID` = "{user_id}";')
                        tokens_last = await cur.fetchall()  
                        tokens_last = tokens_last[0][0]
                        if tokens_last == ():
                            tokens_last = ""
                        token = tokens_last + token_name.upper()+","
                        await cur.execute(f'UPDATE `user` SET `ban_token` = "{token}" WHERE `ID` LIKE "'+str(user_id)+'";')
                        await conn.commit()   
                    except Exception as E:
                        print(E)
                        
    async def get_ban_token(self,user_id):
            pool = await aiomysql.create_pool(host='localhost', port=3306,
                                            user='Nursyka', password='1234',
                                            db='crypto_bot') 
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    try:
                        await cur.execute(f'SELECT `ban_token` FROM `user` WHERE `ID` = "{user_id}";')
                        tokens_last = await cur.fetchall()  
                        tokens_last = tokens_last[0][0]
                        if tokens_last == ():
                            return []
                        tokens_ban = tokens_last.split(",")[:-1]
                        return tokens_ban
                    except:
                        pass
    
    async def return_token(self,user_id,token_name):
            pool = await aiomysql.create_pool(host='localhost', port=3306,
                                            user='Nursyka', password='1234',
                                            db='crypto_bot') 
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    try:
                        await cur.execute(f'SELECT `ban_token` FROM `user` WHERE `ID` = "{user_id}";')
                        tokens_last = await cur.fetchall()  
                        tokens_last = tokens_last[0][0]
                        if tokens_last == ():
                            tokens_last = ""
                        token = tokens_last.replace(f"{token_name.upper()},","")
                        await cur.execute(f'UPDATE `user` SET `ban_token` = "{token}" WHERE `ID` LIKE "'+str(user_id)+'";')
                        await conn.commit()   
                    except Exception as E:
                        print(E)