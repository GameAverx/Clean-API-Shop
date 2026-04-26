from models import query
import os
import uuid
import base64
import json
from .save_img import save_images


def new_seller(auth):
    # проверка авторизацции
    user_id = auth.is_authentificate()
    if not user_id:
        return (401, {'error': 'Unauthorized'})
    # проверка роли
    current_role = query('''SELECT role FROM users WHERE id = ?''', (user_id,), True)
    if current_role[0] == "seller":
        return (400, {'error': 'You are already seller'})

    # sql

    sql_request = '''UPDATE users SET role = "seller" WHERE id = ?'''
    query(sql_request, (user_id,), True)

    return (200, {'message': 'The role has changed'})

# без проверки привязанности магазина к селеру
def new_shop(auth, body):
    # проверка авторизацции
    user_id = auth.is_authentificate()
    if not user_id:
        return (401, {'error': 'Unauthorized'})
    # проверка роли
    current_role = query('''SELECT role FROM users WHERE id = ?''', (user_id,), True)
    if current_role[0] != "seller":
        return (403, {'error': 'You are not a seller'})

    # body
    shop_name = body.get('shop_name').strip()
    hero_banner = save_images('static/shop_img/banners', body.get('hero_banner', []))
    avatar = save_images('static/shop_img/avatars', body.get('avatar', []))
    description = body.get('description').strip()

    # sql
    sql_request = '''INSERT INTO shops (shop_name, hero_banner, avatar, description, seller_id) VALUES (?,?,?,?,?)'''
    query(sql_request, (shop_name, hero_banner, avatar, description, user_id), True)

    return (201, {'message': f'The {shop_name} was created'})




































