from .save_img import save_images
import redis
import redis
import json
import uuid

redis_client = redis.Redis(host='localhost', port=8067, db=0)


# from media_services.media_process import process_media_worker

def avatar(auth, body, user_id):
    is_user = auth.is_authentificate()
    if not is_user:
        return (401, {'Success': False, 'payload': 'Forbidden'})
    if int(is_user) != int(user_id):
        return (403, {'Success': False, 'payload': 'Forbidden'})

    sizes = [(240, 240), (160, 160), (64, 64)]

    task_data = upload_product_image(body, sizes, user_id)
    return (202, {'Success': True, 'payload': task_data})


def upload_product_image(body, sizes, user_id):
    """Пользователь загружает картинку"""
    image_base64 = body.get('image')

    # Генерируем задание
    task_id = str(uuid.uuid4())
    task = {
        'task_id': task_id,
        'type': 'process_product_image',
        # 'product_id': product_id,
        'user_id': user_id,
        'image_data': image_base64,  # или URL временного файла
        # 'sizes': [(500, 500), (240, 240), (160, 160), (64, 64)]
        'sizes': sizes
    }
    # Отправляем в очередь Redis
    redis_client.lpush('media_tasks', json.dumps(task))

    # Возвращаем task_id клиенту для отслеживания статуса
    # handler.send_json(202, {'task_id': task_id, 'status': 'processing'})
    return {'task_id': task_id, 'status': 'processing'}
