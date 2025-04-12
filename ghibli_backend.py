from PIL import Image

def apply_ghibli_style(input_image: Image.Image) -> Image.Image:
    return input_image.transpose(Image.FLIP_LEFT_RIGHT)
