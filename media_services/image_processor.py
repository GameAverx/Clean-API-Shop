from PIL import Image
import base64
from io import BytesIO
def process_image(image_base64, sizes):
    image = base64_to_pil(image_base64)
    for size in sizes:
        width, height = size
        crop_to_viewport(image, width, height)
#     тут по идеи должно быть сохранение байтов в сетевую бд  типо s3

# Превращаем base64 в PIL Image
def base64_to_pil(base64_string):
    # Убираем префикс, если есть
    if 'base64,' in base64_string:
        base64_string = base64_string.split('base64,')[1]

    # Декодируем base64 в байты
    image_bytes = base64.b64decode(base64_string)

    # Превращаем байты в PIL Image
    image = Image.open(BytesIO(image_bytes))
    return image
# target_width, target_height это желаемый размер
def crop_to_viewport(image: Image, target_width: int, target_height: int) -> Image:
    """
    Обрезает картинку до точного размера по алгоритму из ТЗ:
    1. Сохраняем аспект
    2. Докручиваем до ближайшей границы
    3. Обрезаем лишнее симметрично
    """
    target_ratio = target_width / target_height
    current_ratio = image.width / image.height

    if current_ratio > target_ratio:
        # Картинка шире — обрезаем по ширине
        new_width = int(image.height * target_ratio)
        left = (image.width - new_width) // 2
        image = image.crop((left, 0, left + new_width, image.height))
    else:
        # Картинка выше — обрезаем по высоте
        new_height = int(image.width / target_ratio)
        top = (image.height - new_height) // 2
        image = image.crop((0, top, image.width, top + new_height))

    # Финальный ресайз до нужного размера
    return image.resize((target_width, target_height), Image.Resampling.LANCZOS)