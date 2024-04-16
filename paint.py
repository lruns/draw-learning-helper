import csv
import os
import shutil

import utils
from utils import Manager, open_image

ID = 0
IMAGE_NAME = 1
TASK_ID = 2
STUDENT_ID = 3
UPLOAD_DATE = 4


class PaintManager(Manager):
    def __init__(self):
        super().__init__()
        self.main_folder_path = None
        self.image_data_filepath = ''
        self.image_data = []

    def load_folder_configs(self, main_folder_path):
        self.main_folder_path = main_folder_path
        self.image_data_filepath = os.path.join(main_folder_path, 'image_data.csv')
        if os.path.exists(self.image_data_filepath):
            with open(self.image_data_filepath, 'r', newline='') as file:
                reader = csv.reader(file)
                header = next(reader, None)
                for item in reader:
                    self.image_data.append(item)

    def save_folder_configs(self):
        with open(self.image_data_filepath, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Id', 'Image Name', 'Task Id', 'Student Id', 'Upload Date'])
            writer.writerows(self.image_data)
        pass

    def add_image(self, image_filepath, image_name, task_id, student_id, upload_date):
        id = utils.get_next_id(self.image_data, ID)

        image_data = [id, image_name, task_id, student_id, upload_date]
        self.image_data.append(image_data)

        # Copying the image to the destination folder
        destination_path = os.path.join(self.main_folder_path, id)
        shutil.copy(image_filepath, destination_path)

    # def delete_image(self, id):
    #     for row in self.image_data:
    #         if row[ID] == id:
    #             self.image_data.remove(row)
    #             break

    def view_student_works(self, student_id):
        student_image_data = []
        for row in self.image_data:
            if row[STUDENT_ID] == student_id:
                student_image_data.append(row)
        return student_image_data

    def view_task_works(self, task_id):
        task_image_data = []
        for row in self.image_data:
            if row[TASK_ID] == task_id:
                task_image_data.append(row)
        return task_image_data

    def view_image(self, id):
        for row in self.image_data:
            if row[ID] == id:
                open_image(row[ID])

    # def search_image_by_name(self, image_name):
    #     for row in self.image_data:
    #         if row[IMAGE_NAME] == image_name:
    #             print(row)
    #             break
    #     else:
    #         print("Image not found.")
