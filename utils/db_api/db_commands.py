from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
        )

    async def execute(
        self,
        command,
        *args,
        fetch: bool = False,
        fetchval: bool = False,
        fetchrow: bool = False,
        execute: bool = False,
    ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    # async def create_table_users(self):
    #     sql = """
    #     CREATE TABLE IF NOT EXISTS products_user (
    #     id SERIAL PRIMARY KEY,
    #     full_name VARCHAR(255) NOT NULL,
    #     username varchar(255) NULL,
    #     telegram_id BIGINT NOT NULL UNIQUE
    #     );
    #     """
    #     await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    async def add_user(self, full_name, username, telegram_id,state):
        sql = "INSERT INTO products_user (full_name, username, telegram_id,state) " \
              "VALUES($1, $2, $3,$4) returning *"
        return await self.execute(sql, full_name, username, telegram_id,state, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT telegram_id FROM products_user"
        return await self.execute(sql, fetch=True)

    async def update_user_state(self,telegram_id,state):
        sql="UPDATE products_user SET state=$1 WHERE telegram_id=$2"
        return await self.execute(sql,state,telegram_id,execute=True)
    # async def update_user_real_name(self,telegram_id,real_name):
    #     sql="UPDATE products_user SET real_name=$1 WHERE telegram_id=$2"
    #     return await self.execute(sql,real_name,telegram_id,execute=True)

    async def update_user_status(self,telegram_id,status):
        sql="UPDATE products_user SET status=$1 WHERE telegram_id=$2"
        return await self.execute(sql,status,telegram_id,execute=True)
    async def delete_user_result(self,telegram_id):
        sql="UPDATE products_contract SET result=0 WHERE telegram_id=$1"
        return await self.execute(sql,telegram_id,execute=True)
    async def increment_user_result(self,telegram_id):
        sql="UPDATE products_contract SET result=result+1 WHERE telegram_id=$1"
        return await self.execute(sql,telegram_id,execute=True)

    async def get_user_result(self,telegram_id):
        sql="SELECT result FROM products_contract WHERE telegram_id=$1"
        return await self.execute(sql,telegram_id,fetchval=True)

    async def update_user_phone(self,telegram_id,phone):
        sql="UPDATE products_user SET phone=$1 WHERE telegram_id =$2"
        return await self.execute(sql,phone,telegram_id,execute=True)

    async def update_user_passport(self,telegram_id,passport):
        sql="UPDATE products_user SET passport=$1 WHERE telegram_id=$2"
        return await self.execute(sql,passport,telegram_id,execute=True)

    async def create_user_contract(self,telegram_id,fakultet_id,result):
        sql = "INSERT INTO products_contract (telegram_id, fakultet_id, state, result, full_name, phone, extra_phone, address, passport, passport_photo, jshshir) " \
              "SELECT $1, $2, 'registered', $3, real_name, phone, extra_phone, address, passport, photo_id, jshshir " \
              "FROM products_user " \
              "WHERE telegram_id = $1"
        await self.execute(sql, telegram_id, fakultet_id, result, execute=True)

    async def create_new_user_contract(self,telegram_id,fakultet_id,full_name):
        # Check if a record with the given telegram_id and state exists
        select_sql = "SELECT COUNT(*) FROM products_contract WHERE telegram_id=$1 AND state='new'"
        record_count = await self.execute(select_sql, telegram_id,fetchval=True)
        if record_count > 0:
            # Update the existing record
            update_sql = "UPDATE products_contract SET fakultet_id=$1, full_name=$2 WHERE telegram_id=$3 AND state='new' returning id"
            return await self.execute(update_sql, fakultet_id, full_name, telegram_id, fetchrow=True)
        else:
            # Insert a new record
            insert_sql = "INSERT INTO products_contract (telegram_id, fakultet_id, full_name, state,result,contract_link,dtm) VALUES ($1, $2, $3, 'new',0,'0',0) returning id"
            return await self.execute(insert_sql, telegram_id, fakultet_id, full_name, fetchrow=True)
    async def update_contract_field(self,contract_id,field,value,telegram_id):
        sql = f"UPDATE products_contract SET {field}=$1 WHERE telegram_id=$2 AND state='new' AND id=$3"
        return await self.execute(sql, value, telegram_id,contract_id, execute=True)

    async def get_contract_users_by_state(self,state):
        sql="SELECT telegram_id FROM products_contract WHERE state=$1"
        return await self.execute(sql,state,fetch=True)
    async def get_new_contracts(self):
        sql="SELECT products_contract.id,full_name,phone,extra_phone,f.name,f.time,f.lang,address,passport,jshshir,passport_photo," \
            "dtm,result,created,contract_link,diplom " \
            " FROM products_contract INNER JOIN products_fakultet AS f " \
            "ON f.id=fakultet_id  WHERE state='registered'"
        return await self.execute(sql,fetch=True)

    async def get_contract_by_id(self,id):
        sql="SELECT products_contract.id,full_name,phone,extra_phone,f.name,f.time,f.lang,address,passport,jshshir,passport_photo," \
            "dtm,result,created,contract_link,diplom " \
            " FROM products_contract INNER JOIN products_fakultet AS f " \
            "ON f.id=fakultet_id  WHERE state !='new' AND products_contract.id=$1"
        return await self.execute(sql,id,fetch=True)

    async def get_contract_full_info(self,contract_id):
        sql = "SELECT c.id,c.full_name,c.phone,c.extra_phone,f.name,f.time,f.summa," \
              "f.summa_text,f.lang,c.address,c.passport,c.jshshir" \
              " FROM products_contract AS c INNER JOIN products_fakultet AS f " \
              "ON f.id=c.fakultet_id  WHERE c.id=$1"
        return await self.execute(sql,contract_id,fetchrow=True)

    async def get_user_telegram_id_by_contract(self,contract_id):
        sql="SELECT telegram_id FROM products_contract WHERE id=$1"
        return await self.execute(sql,contract_id,fetchval=True)

    async def remove_contract_user_result(self,telegram_id):
        sql="UPDATE products_contract SET result=0 WHERE telegram_id=$1 AND state='new'"
        return await self.execute(sql,telegram_id,execute=True)
    async def get_archived_contracts(self):
        sql = "SELECT products_contract.id,full_name,phone,extra_phone,f.name,f.time,f.lang,address,passport,jshshir,passport_photo,dtm,result " \
              " FROM products_contract INNER JOIN products_fakultet AS f " \
              "ON f.id=fakultet_id  WHERE state='archive'"
        return await self.execute(sql, fetch=True)

    async def update_contract_state(self,id,state):
        sql="UPDATE products_contract SET state=$1 WHERE id=$2"
        return await self.execute(sql,state,id,execute=True)

    async def delete_contract(self,id):
        sql="DELETE products_contract WHERE id=$1 AND state='archive'"
        return await self.execute(sql,id,execute=True)

    async def update_contract_created_time(self,id,created):
        sql="UPDATE products_contract SET created=$1 WHERE id=$2"
        return await self.execute(sql,created,id,execute=True)
    async def get_accepted_contracts(self):
        sql = "SELECT products_contract.id,full_name,phone,extra_phone,f.name,f.time,f.lang," \
              "address,passport,jshshir,passport_photo,dtm,result,created,contract_link" \
              " FROM products_contract  INNER JOIN products_fakultet AS f " \
              "ON f.id=fakultet_id WHERE state='accepted'"
        return await self.execute(sql, fetch=True)
    async def get_students(self):
        sql = "SELECT products_contract.id,full_name,phone,extra_phone,f.name,f.time,f.lang,address,passport,jshshir,dtm,result,created" \
              " FROM products_contract  INNER JOIN products_fakultet AS f " \
              "ON f.id=fakultet_id WHERE state='accepted' ORDER BY created"
        return await self.execute(sql, fetch=True)
    async def update_user_photo(self,telegram_id,photo_id):
        sql="UPDATE products_contract SET passport_photo=$1 WHERE telegram_id=$2"
        return await self.execute(sql,photo_id,telegram_id,execute=True)

    async def update_user_jshshir(self, telegram_id, jshshir):
        sql = "UPDATE products_user SET jshshir =$1 WHERE telegram_id=$2"
        return await self.execute(sql,jshshir, telegram_id,  execute=True)
    async def update_user_address(self,telegram_id,address):
        sql="UPDATE products_user SET address=$1 WHERE telegram_id=$2"
        return await self.execute(sql,address,telegram_id,execute=True)

    async def update_user_extra_phone(self,telegram_id,phone):
        sql="UPDATE products_user SET extra_phone=$1 WHERE telegram_id=$2"
        return await self.execute(sql,phone,telegram_id,execute=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM products_user WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)
    async def get_user_by_telegram_id(self,id):
        sql = "SELECT * FROM products_user WHERE telegram_id=$1"
        return await self.execute(sql,id,fetchrow=True)
    async def get_user_phone_by_telegram_id(self,telegram_id,phone):
        sql="SELECT COUNT(*) FROM products_contract WHERE telegram_id=$1 AND phone=$2"
        return await self.execute(sql,telegram_id,phone,fetchval=True)


    async def get_user_state_by_telegram_id(self, id):
        sql = "SELECT state FROM products_user WHERE telegram_id=$1"
        return await self.execute(sql, id, fetchval=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM products_user"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE products_user SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM products_user WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE products_user", execute=True)

    async def get_fakultets(self,language,time):
        sql="SELECT name FROM products_fakultet WHERE lang=$1 AND time=$2"
        return await self.execute(sql,language,time,fetch=True)

    async def get_test(self,number):
        sql = "SELECT question FROM products_test WHERE number=$1"
        return await self.execute(sql,number,fetchval=True)

    async def get_question_with_answer(self, number):
        sql = "SELECT answer FROM products_test WHERE number=$1 "
        answer=await self.execute(sql,number,fetchval=True)
        sql="SELECT question,number FROM products_test WHERE number=$1+1"
        res=await self.execute(sql,number,fetchrow=True)
        if res is None:
            return (answer,None,None)
        question=res[0]
        number=res[1]
        return (answer,question,number)

    async def get_contract_by_telefone(self,telefon):
        sql="SELECT * FROM products_contract WHERE phone=$1 AND state='registered'"
        return await self.execute(sql,telefon,fetchrow=True)

    async def get_fakultet_id_by_name(self, name):
        sql = "SELECT id FROM products_fakultet WHERE name=$1"
        return await self.execute(sql, name, fetchrow=True)
    async def check_for_phone_exists(self,phone):
        sql="SELECT id FROM products_contract WHERE phone=$1 AND state='new'"
        return await self.execute(sql,phone,fetchval=True)
    async def check_for_passport_exists(self,phone):
        sql="SELECT COUNT(*) FROM products_contract WHERE passport=$1 AND state IN ('accepted','registered','archive')"
        return await self.execute(sql,phone,fetchval=True)
