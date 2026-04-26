from models import query
import os
import uuid
import base64
import json


def tshirts_list(handler):
    parse = handler.path.split('?')

    filter = {}
    if len(parse) > 1:
        for i in parse[1].split('&'):
            if '=' in i:
                key, val = i.split('=')
                filter[key] = val

    # настроить на поиск в таблице sellers а не users

    # request = '''SELECT t.*, s.shop_name FROM tshirts t
    #         INNER JOIN sellers s ON t.seller_id = s.user_id
    #         WHERE 1=1'''

    request = '''SELECT t.* FROM tshirts t
                INNER JOIN shops s ON t.shop_id = s.id
                WHERE 1=1'''

    request_params = []
    # конструктор фильтра запроса к бд
    if 'title' in filter:
        request += ' AND t.title LIKE = ?'
        request_params.append(f'{str(filter['title'])}')
    if 'color' in filter:
        request += ' AND t.color = ?'
        request_params.append(str(filter['color']))
    if 'size' in filter:
        request += ' AND t.size = ?'
        request_params.append(str(filter['size']))
    if 'min_price' in filter:
        request += ' AND t.price >= ?'
        request_params.append(float(filter['min_price']))
    if 'max_price' in filter:
        request += ' AND t.price <= ?'
        request_params.append(float(filter['max_price']))
    # if 'seller_id' in filter:
    #     request += ' AND t.seller_id = ?'
    #     request_params.append(int(filter['seller_id']))
    if 'shop_name' in filter:
        request += ' AND s.shop_name LIKE ?'
        request_params.append(f"%{str(filter['shop_name'])}%")

    # запрос в бд
    tshirts = query(request, request_params)

    response = []

    # получение картинки к каждому товару
    for tshirt in tshirts:
        p = dict(tshirt)
        p['image'] = json.loads(p['image']) if p['image'] else []
        response.append(p)
    return (200, response)

def add_product(auth, body):
    # проверка авторизацции
    user_id = auth.is_authentificate()
    if not user_id:
        return (401, {'error': 'Unauthorized'})
    # проверка прав
    # доработать, изменить таблицу
    is_seller = query('''SELECT id FROM users WHERE id = ? AND role = "seller" ''', (user_id,), True)
    if not is_seller:
        return (403, { 'error' : 'You are not a seller'})

    title = body.get('title').strip()
    shop_id = body.get('shop_id').strip()

    # shop_name = body.get('shop_name').strip()
    # user_to_shop = query('''SELECT id FROM shops
    #                     WHERE shop_name = ? and seller_id = ?''', (shop_name,))
    price = body.get('price').strip()
    img = save_images(body.get('images', []))
    color = body.get('color').strip()
    size = body.get('size').strip()
    # сохранение в бд
    query('''INSERT INTO  tshirts (title, price, image, color, size, shop_id)
            VALUES (?,?,?,?,?,?)''', (title, float(price), img, color, size, int(shop_id)), True)

    return (201, 'Product created')

# сохранение картинок
def save_images(image):
    saved_images = []
    if isinstance(image, str):
        image = [image]

    for idx, img_base64 in enumerate(image):
        if ',' in img_base64:
            img_base64 = img_base64.split(',')[1]

        try:
            image_bytes = base64.b64decode(img_base64)
        except base64.binascii.Error as e:
            return (400, {'error': f'Image #{idx+1} is corrupted: {str(e)}'})

        filename = f"img_{idx+1}_{uuid.uuid4()}.jpg"
        filepath = f"static/products/{filename}"

        os.makedirs("static/products", exist_ok=True)
        with open(filepath, 'wb') as f:
            f.write(image_bytes)
        saved_images.append(filepath)

    return json.dumps(saved_images)











