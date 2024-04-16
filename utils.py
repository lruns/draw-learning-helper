from PIL import Image


def open_image(image):
    image = Image.open(image)
    image.show()
