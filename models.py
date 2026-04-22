import sqlite3


def db_init():
    conn = sqlite3.connect('demo.db')
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
                                                    email TEXT UNIQUE NOT NULL,
                                                    hashed_password TEXT NOT NULL,
                                                    role TEXT CHECK(role IN ('admin', 'buyer', 'seller')) DEFAULT 'buyer' )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS t-shirts (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                    title TEXT NOT NULL,
                                                    price REAL NOT NULL,
                                                    image TEXT,
                                                    color TEXT CHECK(color IN ('red', 'green', 'blue', 'yellow', 'black', 'white')),
                                                    size TEXT CHECK(size IN ('XS', 'S', 'M', 'L', 'XL', 'XXL')),
                                                    seller_id INTEGER NOT NULL, FOREIGN KEY (seller_id) REFERENCES users (id) )''')

    cur.execute(''' CREATE TABLE IF NOT EXISTS sellers (user_id INTEGER PRIMARY KEY,
                                                    shop_name TEXT,
                                                    hero_banner TEXT,
                                                    avatar TEXT,
                                                    description TEXT,
                                                    FOREIGN KEY (user_id) REFERENCES users (id) ''')

    cur.execute('''CREATE TABLE IF NOT EXISTS cart (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                    text TEXT NOT NULL,
                                                    hashed_password TEXT NOT NULL)''')

    # cur.execute('CREATE TABLE IF NOT EXISTS comments (id INTEGER PRIMARY KEY AUTOINCREMENT, '
    #                                                 'text TEXT NOT NULL, t-shirt_id INTEGER NOT NULL, user_id INTEGER NOT NULL,'
    #                                                 ' FOREIGN KEY (user_id) REFERENCES users (id) FOREIGN KEY (t-shirt_id) REFERENCES t-shirts (id) )')
    #
    # cur.execute('CREATE TABLE IF NOT EXISTS likes (id INTEGER PRIMARY KEY AUTOINCREMENT, '
    #                                                 'comment_id INTEGER NOT NULL, user_id INTEGER NOT NULL, '
    #                                                 'FOREIGN KEY (user_id) REFERENCES users (id) FOREIGN KEY (comment_id) REFERENCES comments (id) )')



    conn.commit()
    # conn.close()

def query(request, fetch_one=False):
    conn = sqlite3.connect('demo.db')
    cur = conn.cursor()
    try:
        cur.execute(f'{request}')
        users = cur.fetchall()
        print(users)
    except error as e:
        return e


