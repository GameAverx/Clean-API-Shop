from .save_img import save_images
import redis
def avatar(auth, body, user_id):
    is_user = auth.is_authentificate()
    if not is_user:
        return (401, {'Success': False, 'payload': 'Forbidden'})
    if int(is_user) != int(user_id):
        return (403, {'Success': False, 'payload': 'Forbidden'})
    # фото
    img = save_images('static/products', body.get('images', []))
    # форматирование в 3 разных размера
    # сохранение

    