import uuid
from models import query
import json
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
        return (401, {'Success' : False, 'payload': 'Forbidden'})
    if int(is_user) != int(user_id):
        return (403, {'Success' : False, 'payload': 'Forbidden'})

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

    return (201, {'Success' : True, 'payload': 'Cart created'})

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

    return (200, {'Success' : True, 'payload': 'Cart updated'})

def clear_cart(auth, user_id):
    is_user = auth.is_authentificate()
    if not is_user:
        return (401, {'Success': False, 'payload': 'Forbidden'})
    if int(is_user) != int(user_id):
        return (403, {'Success': False, 'payload': 'Forbidden'})

    response = query('''DELETE FROM user_cart WHERE user_id = ? ''', (int(user_id),), True)

    return (200, {'Success' : True, 'payload': 'Cart cleared'})





