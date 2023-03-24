import aiomysql
import ast



class DateBase:
    def __init__(self):
        self.pool = None
    async def create(self):
        pool = await aiomysql.create_pool(host='localhost', port=3306,
                                        user='Nursyka', password='1234',
                                        db='new_inspire_pars')
        self.pool = pool
