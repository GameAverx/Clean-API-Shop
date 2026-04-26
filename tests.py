

# reg
# {
#     "email": "user@example.com",
#     "password": "mypassword123",
#     "name": "Иван",
#     "role": "seller"
# }

# {
#     "email": "averx@example.com",
#     "password": "mypassword123",
#     "name": "alex",
#     "role": "buyer"
# }


# {
#     "email": "user@example.com",
#     "password": "mypassword123",
#     "name": "Иван"
#     "role": "seller"
# }
# сайт для кодирования картинки в base64
# https://snipp.ru/tools/base64-img-decode

# {
#      "title": "Футболка спортивная",
#      "price": "5000",
#      "color": "red",
#      "size": "L",
#      "shop_id": "1",
#      "images": "base64code"
# }
# http://localhost:8080/products
# http://localhost:8080/products?size=L&min_price=4500&color=red
# http://localhost:8080/products?color=red

import sqlite3
# request = '''INSERT INTO  tshirts (title, price, image, color, size, seller_id)
#             VALUES (?,?,?,?,?,?)'''
#
# params = ("Лонгслив", 3000.0, "static/products/img_1_eqewqdsa.png", "blue", "XXL", 2)
conn = sqlite3.connect('demo.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()


# request = '''INSERT INTO  sellers (user_id, shop_name, hero_banner, avatar, description)
#             VALUES (?,?,?,?,?,?)'''
#
# params = ("Лонгслив", 3000.0, "static/products/img_1_eqewqdsa.png", "blue", "XXL", 2)


# cur.execute('DROP TABLE IF EXISTS sellers')
# cur.execute('DROP TABLE IF EXISTS tshirts')
#
# conn.commit()
# conn.close()
# print(f"Таблица sellers удалена")
# print(f"Таблица tshirts удалена")


# user
# {
#      "email": "Averx@example.com",
#      "password": "mypassword123",
#     "name": "Алексей",
#      "role": "seller"
# }
# список магазинов ['DNS']






