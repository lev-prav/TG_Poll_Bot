import asyncio
import sqlite3
import threading
import json

#TODO make this stuff async 
class DBClient:
    def connect(self):
        self.conn = sqlite3.connect('polls.db')
        self.cursor = self.conn.cursor()
        #self.table_coroutine = asyncio.create_task(self.create_table("guitar_store"))
    
    def disconnect(self):
        del self.conn
        del self.cursor
    
    def insert_poll_into(self, table_name, answers: dict):
        # if self.table_coroutine is not None:
        #     self.table_coroutine
        #     self.table_coroutine = None

        self.connect()

        self.create_table(table_name)

        self.cursor.execute(f"insert into {table_name} values (?, ?)", 
            [answers["user_id"], json.dumps(answers["answers"], ensure_ascii=False)])
        self.conn.commit()
        print(f"Insertion done in {table_name}")

        self.disconnect()
        

    def create_table(self, table_name : str):
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (id NUMERIC, data json)")
        self.conn.commit()


if __name__ == '__main__':
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS countries (id INT, data json)")
    
    countries = [
        {'adminregion': {'id': '', 'value': ''},
 'capitalCity': 'Oranjestad',
 'id': 'ABW',
 'incomeLevel': {'id': 'HIC', 'value': 'High income'},
 'iso2Code': 'AW',
 'latitude': '12.5167',
 'lendingType': {'id': 'LNX', 'value': 'Not classified'},
 'longitude': '-70.0167',
 'name': 'Aruba',
 'region': {'id': 'LCN', 'value': 'Latin America & Caribbean '}}
 ]
    
    for country in countries:
        cursor.execute("insert into countries values (?, ?)", 
            [country['id'], json.dumps(country)])
        conn.commit()
    conn.close()

