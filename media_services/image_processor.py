from PIL import Image, ImageFilter
import base64
from io import BytesIO
import os



def process_image(image_base64, sizes, type, id): #id для папки
    image = base64_to_pil(image_base64)

    config = IMAGE_TYPES[type]
    if not config:
        raise ValueError(f"Unknown image type: {type}")
    print('1232132qdqdewvvqw')
    for size in sizes:
        width, height = size
        cropped = crop_to_viewport(image, width, height)


        os.makedirs(config['base_path'].format(id=id), exist_ok=True)
        cropped.save(config['base_path'].format(id=id) + f'/{width}.jpg', format=config['img_format'], quality=config['img_quality'])
    print('w1iknqw')
        # if type == 'avatar':
        #     os.makedirs(f"static/images/profiles/{id}", exist_ok=True)
        #     cropped.save(f'static/images/profiles/{id}/{width}.jpg', format='JPEG', quality=85)
        #
        # elif type == 'product':
        #     os.makedirs(f"static/images/product/{id}", exist_ok=True)
        #     cropped.save(f'static/images/product/{id}/{width}.jpg', format='JPEG', quality=85)

    # skeleton = generate_skeleton(f"static/images/profiles|product/{id}/{max(sizes)[0]}.jpg")
    skeleton = generate_skeleton(config['base_path'].format(id=id) + f'/{max(sizes)[0]}.jpg')
    # skeleton.save(f'static/images/profiles/{id}/skeleton.jpg', format='JPEG', quality=30)
    skeleton.save( config['skeleton_path'].format(id=id), format= config['skeleton_format'],quality=config['skeleton_quality'])

# Варианты типов
IMAGE_TYPES = {'avatar': {'base_path': 'static/images/profiles/{id}',
                        'skeleton_path': 'static/images/profiles/{id}/skeleton.jpg',
                        'img_format': 'JPEG',
                        'skeleton_format' : 'JPEG',
                        'skeleton_quality': 30,
                        'img_quality': 85},
            'product': {'base_path': 'static/images/product/{id}',
                        'skeleton_path': 'static/images/product/{id}/skeleton.jpg',
                        'img_format': 'JPEG',
                        'skeleton_format' : 'JPEG',
                        'skeleton_quality': 30,
                        'img_quality': 85}}

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
    return image.resize((target_width, target_height), Image.Resampling.LANCZOS)  # PIL Image


def generate_skeleton(image_path, blur_width=20, blur_radius=2, quality=30):
    """
    Генерирует base64-строку скелетона.
    """
    # 1. Открываем оригинальное изображение
    img = Image.open(image_path)

    # 2. Изменяем размер до очень маленького (например, 20px по ширине)
    #    Сохраняем пропорции, чтобы не искажать содержимое.
    width, height = img.size
    ratio = blur_width / width
    new_size = (blur_width, int(height * ratio))
    img.thumbnail(new_size, Image.Resampling.LANCZOS)

    # сильное размытие по Гауссу
    img = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))

    # 4.Сохраняем в буфер с сильным сжатием
    buffer = BytesIO()
    img.save(buffer, format='JPEG', quality=quality)
    img_bytes = buffer.getvalue()


    # 5. Кодируем в base64
    # base64_string = base64.b64encode(img_bytes).decode('utf-8')
    # return f"data:image/jpeg;base64,{base64_string}"
    return img

# Сохранение файлов в облачное храниище
def save_to_minio():
    pass
