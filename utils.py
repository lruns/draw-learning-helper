from PIL import Image

class Manager:
    def __init__(self):
        pass

    def load_folder_configs(self, main_folder_path):
        pass

    def save_folder_configs(self):
        pass


def open_image(image):
    image = Image.open(image)
    image.show()

def get_next_id(data, ID_POSITION):
    id = 0
    if len(data) > 0:
        last = data[-1]
        id = int(last[ID_POSITION]) + 1
    return id
