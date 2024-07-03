import sqlite3

DATABASE = 'support_bot.db'

async def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT,
        last_name TEXT,
        phone_number TEXT
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        message_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        message TEXT,
        response TEXT,
        answered INTEGER DEFAULT 0,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )
    ''')
    conn.commit()
    conn.close()

async def add_user(user_id, phone_number, first_name, last_name):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT OR IGNORE INTO users (user_id, phone_number, first_name, last_name) VALUES (?, ?, ?, ?)
    ''', (user_id, phone_number, first_name, last_name))
    conn.commit()
    conn.close()

async def add_message(user_id, message):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO messages (user_id, message) VALUES (?, ?)
    ''', (user_id, message))
    conn.commit()
    conn.close()

async def get_unanswered_messages():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT message_id, user_id, message FROM messages WHERE answered = 0
    ''')
    rows = cursor.fetchall()
    conn.close()
    return rows

async def respond_to_message(message_id, response):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE messages SET response = ?, answered = 1 WHERE message_id = ?
    ''', (response, message_id))
    conn.commit()
    conn.close()

async def get_all_users():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()
    conn.close()
    return rows
