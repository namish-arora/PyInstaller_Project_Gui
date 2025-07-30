import os
from PIL import Image, ImageTk




def load_image(filename, size):
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'assets'))
    image_path = os.path.join(base_path, filename)
    image = Image.open(image_path).resize(size, Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(image)
