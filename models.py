import sqlite3


def db_init():
    conn = sqlite3.connect('demo.db')
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
                                                    email TEXT UNIQUE NOT NULL,
                                                    hashed_password TEXT NOT NULL,
                                                    role TEXT CHECK(role IN ('admin', 'buyer', 'seller')) DEFAULT 'buyer' )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS tshirts (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                    title TEXT NOT NULL,
                                                    price REAL NOT NULL,
                                                    image TEXT,
                                                    color TEXT CHECK(color IN ('red', 'green', 'blue', 'yellow', 'black', 'white')),
                                                    size TEXT CHECK(size IN ('XS', 'S', 'M', 'L', 'XL', 'XXL')),
                                                    shop_id INTEGER NOT NULL, FOREIGN KEY (shop_id) REFERENCES shops (id))''')

    # cur.execute('''CREATE TABLE IF NOT EXISTS sellers (user_id INTEGER PRIMARY KEY,
    #                                                 shop_name TEXT,
    #                                                 hero_banner TEXT,
    #                                                 avatar TEXT,
    #                                                 description TEXT,
    #                                                 FOREIGN KEY (user_id) REFERENCES users (id) )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS shops (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                    shop_name TEXT,
                                                    hero_banner TEXT,
                                                    avatar TEXT,
                                                    description TEXT,
                                                    seller_id INTEGER,
                                                    FOREIGN KEY (seller_id) REFERENCES users (id))''')
    # items_id хранится словарь json формата с ключом: tshirts id и значением кол-во товара '{'2':5}' '2' - id, 5 - quantity,
    cur.execute('''CREATE TABLE IF NOT EXISTS user_cart (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                    items TEXT NOT NULL,
                                                    user_id INTEGER NOT NULL, FOREIGN KEY (user_id) REFERENCES users (id))''')

    cur.execute('''CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                        order_id TEXT UNIQUE,
                                                        total_amount REAL,
                                                        status TEXT CHECK(status IN ('pending', 'paid', 'canceled')) DEFAULT 'pending',
                                                        payment_id TEXT,
                                                        user_id INTEGER NOT NULL, FOREIGN KEY (user_id) REFERENCES users (id))''')
    # cur.execute(''' CREATE TABLE IF NOT EXISTS nonAuthUserCart (id INTEGER PRIMARY KEY AUTOINCREMENT,
    #                                                             items TEXT NOT NULL,
    #                                                             session_id TEXT UNIQUE NOT NULL) ''')



    # cur.execute('CREATE TABLE IF NOT EXISTS comments (id INTEGER PRIMARY KEY AUTOINCREMENT, '
    #                                                 'text TEXT NOT NULL, t-shirt_id INTEGER NOT NULL, user_id INTEGER NOT NULL,'
    #                                                 ' FOREIGN KEY (user_id) REFERENCES users (id) FOREIGN KEY (t-shirt_id) REFERENCES tshirts (id) )')
    #
    # cur.execute('CREATE TABLE IF NOT EXISTS likes (id INTEGER PRIMARY KEY AUTOINCREMENT, '
    #                                                 'comment_id INTEGER NOT NULL, user_id INTEGER NOT NULL, '
    #                                                 'FOREIGN KEY (user_id) REFERENCES users (id) FOREIGN KEY (comment_id) REFERENCES comments (id) )')



    conn.commit()
    conn.close()

def query(request, params=(), fetch_one=False):
    conn = sqlite3.connect('demo.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(request, params)

    if fetch_one:
        result = cur.fetchone()
    else:
        result = cur.fetchall()
    conn.commit()
    conn.close()
    return result


