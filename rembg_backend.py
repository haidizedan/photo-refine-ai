from rembg import remove
from PIL import Image
import io

def remove_background(image: Image.Image) -> Image.Image:
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    input_bytes = img_byte_arr.getvalue()
    output_bytes = remove(input_bytes)
    return Image.open(io.BytesIO(output_bytes)).convert("RGBA")
