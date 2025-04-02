import sqlite3

def create_table():
    cursor = sqlite3.connect('database/database_login.db')
    conn = cursor.cursor()


    conn.execute('CREATE TABLE IF NOT EXISTS login (username TEXT, password TEXT)')
    conn.execute('INSERT INTO login (username, password) VALUES (?, ?)', ('admin', '123'))

    cursor.commit()
    cursor.close()

if __name__ == '__main__':
    create_table()