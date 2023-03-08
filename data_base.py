import sqlite3 as sq


def sql_start():
    global base, cur
    base = sq.connect('compliment.db')
    cur = base.cursor()
    if base:
        print('Data base connected successfully')
    base.execute('CREATE TABLE IF NOT EXISTS compliments(compliment_text TEXT)')
    base.commit()


async def sql_add_data(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO compliments VALUES(?)', (data['compliment_text']))
        base.commit()


def sql_read():
    return cur.execute('SELECT * FROM compliments').fetchall()
