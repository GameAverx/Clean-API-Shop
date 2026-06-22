from PIL import Image, ImageFilter
import base64
from io import BytesIO
def process_image(image_base64, sizes):
    image = base64_to_pil(image_base64)
    for size in sizes:
        width, height = size
        cropped = crop_to_viewport(image, width, height)
        print("1232132132134wtf")
        cropped.save(f'static/images/output{width}.jpg', format='JPEG', quality=85)
    # generate_skeleton(f"static/images/output{max(sizes)[0]}.jpg")
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
    return image.resize((target_width, target_height), Image.Resampling.LANCZOS) #PIL Image


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

    # 3. Применяем сильное размытие по Гауссу
    img = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))

    # 4. Сохраняем в буфер с сильным сжатием (низкое качество)
    buffer = BytesIO()
    img.save(buffer, format='JPEG', quality=quality)
    img_bytes = buffer.getvalue()

    # 5. Кодируем в base64
    base64_string = base64.b64encode(img_bytes).decode('utf-8')
    print(f"data:image/jpeg;base64,{base64_string}")
    return f"data:image/jpeg;base64,{base64_string}"

# Использование
skeleton_data_uri = generate_skeleton('static/images/output240.jpg')
print(skeleton_data_uri)