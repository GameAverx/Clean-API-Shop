import redis
import json
from image_processor import process_image
# from storage import save_to_s3

redis_client = redis.Redis(host='localhost', port=8067, db=0)



def process_media_worker():
    """Бесконечный цикл обработки задач из очереди"""
    while True:
        # Берем задачу из очереди
        _, task_json = redis_client.brpop('media_tasks')
        task = json.loads(task_json)

        if task['type'] == 'process_product_image':
            # Обрабатываем картинку
            results = process_image(
                task['image_data'],
                task['sizes']
            )

            # Сохраняем в S3/MinIO
            urls = save_to_s3(results, task['product_id'])

            # Обновляем статус в БД (через API основного сервиса)
            update_product_images(task['product_id'], urls)

            # Или через прямую запись в БД (если общая БД)
            # update_db_directly(task['product_id'], urls)