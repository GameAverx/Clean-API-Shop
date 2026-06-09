import uuid
from ..models import query
import json
# оплата
import logging
from yookassa import Configuration, Payment


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


# не актуально если в url всегда есть данные о user  /user/:userId/cart/product/:productId
def get_session_id(handler):
    cookies = handler.headers.get('Cookie', '')
    session_id = None

    for cookie in cookies.split(';'):
        if 'session_id=' in cookie:
            session_id = cookie.split('=')[1].strip()
            break

    if not session_id:
        session_id = str(uuid.uuid4())
        handler.send_header('Set-Cookie', f'session_id={session_id}; Path=/')

    return session_id


#
# {"data": [
#   {
#     "productId": "2",
#     "quantity": 1
#   },
#   {
#     "productId": "4",
#     "quantity": 2
#   },
#   {
#     "productId": "5",
#     "quantity": 3
#   }
# ]}

def add_to_cart(auth, body, user_id, product_id=False):
    is_user = auth.is_authentificate()
    if not is_user:
        # user_session_id = get_session_id()
        # is_cart_exist = query('''SELECT id FROM nonAuthUserCart WHERE session_id = ?''', (user_session_id,),True)
        # if is_cart_exist:
        #     cart_items_json = query('''SELECT items FROM nonAuthUserCart WHERE id = ? ''', (is_cart_exist,), True)
        # else:
        #     cart_items_json = query('''SELECT items FROM nonAuthUserCart WHERE id = ? ''', (is_user,), True)
        return (401, {'Success': False, 'payload': 'Forbidden'})
    if int(is_user) != int(user_id):
        return (403, {'Success': False, 'payload': 'Forbidden'})

    data = body.get("data")
    cart_items_json = "{}"
    cart_dict = json.loads(cart_items_json)
    if product_id is not False:
        quantity = int(data[0]['quantity'])
        cart_dict[product_id] = quantity
    else:

        for product in data:
            product_id = product['productId']
            quantity = int(product['quantity'])
            cart_dict[product_id] = quantity

    new_cart = json.dumps(cart_dict)
    is_cart_exist = query('''SELECT id FROM user_cart WHERE user_id = ? ''', (int(user_id),), True)
    if is_cart_exist:
        response = query('''UPDATE user_cart SET items = ?''', (new_cart,), True)
    else:
        response = query('''INSERT INTO user_cart (items, user_id) VALUES (?,?)''', (new_cart, int(user_id)), True)

    return (201, {'Success': True, 'payload': 'Cart created'})


def update_cart(auth, body, user_id, product_id=False):
    is_user = auth.is_authentificate()
    if not is_user:
        return (401, {'Success': False, 'payload': 'Forbidden'})
    if int(is_user) != int(user_id):
        return (403, {'Success': False, 'payload': 'Forbidden'})
    is_cart_exist = query('''SELECT id FROM user_cart WHERE user_id = ? ''', (int(user_id),), True)
    if not is_cart_exist:
        return (400, {'Success': False, 'payload': 'Cart is not exist'})

    cart_items = query('''SELECT items FROM user_cart WHERE user_id = ?''', (int(user_id),), True)

    data = body.get("data")
    cart_dict = json.loads(*cart_items)
    print(cart_dict)

    if product_id is not False:
        quantity = int(data[0]['quantity'])
        if product_id in cart_dict:
            cart_dict[product_id] = int(cart_dict[product_id]) + quantity
        else:
            cart_dict[product_id] = quantity
    else:

        for product in data:
            product_id = product['productId']
            quantity = int(product['quantity'])
            if product_id in cart_dict:
                cart_dict[product_id] = int(cart_dict[product_id]) + quantity
            else:
                cart_dict[product_id] = quantity
    print(cart_dict, 'updated')
    updated_cart = json.dumps(cart_dict)

    response = query('''UPDATE user_cart SET items = ?''', (updated_cart,), True)

    return (200, {'Success': True, 'payload': 'Cart updated'})


def clear_cart(auth, user_id):
    is_user = auth.is_authentificate()
    if not is_user:
        return (401, {'Success': False, 'payload': 'Forbidden'})
    if int(is_user) != int(user_id):
        return (403, {'Success': False, 'payload': 'Forbidden'})

    response = query('''DELETE FROM user_cart WHERE user_id = ? ''', (int(user_id),), True)

    return (200, {'Success': True, 'payload': 'Cart cleared'})


def payment(handler, user_id):
    is_user = handler.is_authentificate()
    if not is_user:
        return (401, {'Success': False, 'payload': 'Forbidden'})
    if int(is_user) != int(user_id):
        return (403, {'Success': False, 'payload': 'Forbidden'})

    # проверка существования корзины
    is_cart_exist = query('''SELECT id FROM user_cart WHERE user_id = ? ''', (int(user_id),), True)
    if not is_cart_exist:
        return (400, {'Success': False, 'payload': 'Cart is not exist'})

    cart_items = query('''SELECT items FROM user_cart WHERE user_id = ?''', (int(user_id),), True)
    cart_dict = json.loads(*cart_items)

    # Подсчет суммы корзины
    product_ids = list(cart_dict.keys())
    place_holders = ','.join('?' * len(product_ids))
    print(12321378901321109)
    print(tuple(product_ids))
    print(place_holders)
    products = query(f'''SELECT id, price FROM tshirts WHERE id IN ({place_holders})''', tuple(product_ids))
    total = 0

    for product in products:
        quantity = int(cart_dict[f'{product['id']}'])
        total+= int(product['price']) * quantity
    print(total, "total amount")
    # Cоздаём заказ в бд
    order_id = generate_short_uuid()
    order = query('''INSERT INTO orders (order_id, total_amount, user_id)
            VALUES (?,?,?) ''', (order_id, total, user_id), True)



    # API к юкассе
    # Идентификатор магазина
    Configuration.account_id = "1367462"
    Configuration.secret_key =  "test_suF_3p4DHT9P13ezF8vcLmATJYwU7w0_h8KtlHMZljI"
    return_url = f"http://localhost:8080/user/{user_id}/order/{order_id}/complete"
    payment = Payment.create({
        "amount": {
            "value": f"{total}",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": f"{return_url}"
        },
        "capture": True,
        "description": "Заказ №1"
    }, uuid.uuid4())
    payment_url = payment['confirmation']['confirmation_url']
    payment_id = payment['id']
    # payment_status = payment['status']
    logging.info(f"payment_url {payment_url}")
    print(payment_url)
    print(payment_url)
    print(payment_url)
    print("order_id:", order_id)
    print("order_id:", order_id)
    print("order_id:", order_id)
    print("payment_id", payment_id)
    print("payment_id", payment_id)
    print("payment_id", payment_id)
    save_payment_to_order(order_id, payment_id)
    handler.send_response(303)
    handler.send_header('Location', payment_url)
    handler.end_headers()
    return (200, {'Success': True, 'payload': 'Redirect yookassa'})

def save_payment_to_order(order_id, payment_id):
    query('''
            UPDATE orders 
            SET payment_id = ?
            WHERE order_id = ?
        ''', (payment_id, order_id))

# генерация номера заказа
def generate_short_uuid():
    return uuid.uuid4().hex[:12].upper()

def complete_order(auth, user_id, order_id):
    is_user = auth.is_authentificate()
    if not is_user:
        return (401, {'Success': False, 'payload': 'Forbidden'})
    if int(is_user) != int(user_id):
        return (403, {'Success': False, 'payload': 'Forbidden'})
    # payment_id
    payment_id = query('''SELECT payment_id FROM orders WHERE order_id = ?''', (order_id,), True)
    Configuration.account_id = "1367462"
    Configuration.secret_key = "test_suF_3p4DHT9P13ezF8vcLmATJYwU7w0_h8KtlHMZljI"
    payment = Payment.find_one(payment_id[0])

    if payment.status == "succeeded":
        # обновление статуса заказа
        query('''
                    UPDATE orders 
                    SET status = ?
                    WHERE order_id = ?
                ''', ("paid", order_id), True)
        return (200, {'Success': True, 'payload': 'Payment successful'})
    elif payment.status == "canceled":
        query('''   UPDATE orders 
                            SET status = ?
                            WHERE order_id = ?
                        ''', ("canceled", order_id), True)
        return (400, {'Success': False, 'payload': 'Payment canceled'})
    else:
         return (400, {'Success': False, 'payload': 'Payment not completed'})
def yookassa_webhook(body):
    pass


# # Просто выполните в терминале:
# ssh -R 80:localhost:8080 serveo.net
#
# # Получите URL: https://subdomain.serveo.net