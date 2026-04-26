import os
import uuid
import base64
import json




def save_images(dir_path,image):
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
        filepath = f"{dir_path}/{filename}"

        os.makedirs(f"{dir_path}", exist_ok=True)
        with open(filepath, 'wb') as f:
            f.write(image_bytes)
        saved_images.append(filepath)

    return json.dumps(saved_images)