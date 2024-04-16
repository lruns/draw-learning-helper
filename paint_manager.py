import os
import csv
import json
import utils


class photoManager:
    def __init__(self):
        self.config_file = os.path.join(os.path.expanduser('~'), '.photo_manager_config.json')
        self.folder_path = ''
        self.image_data_file = ''
        self.task_data_file = ''
        self.image_data = []
        self.task_data = []

    def start(self):
        if not os.path.exists(self.config_file):
            "Добро пожаловать первый раз в программу!"
            self.create_config()
        else:
            self.load_config()
            if not os.path.exists(self.folder_path):
                print("Папка с фотографиями не найдена.")
                self.update_folder_path()
            else:
                print("Обнаружена сохраненная папка с фотографиями `" + self.folder_path + "`.")

        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)
        if not os.path.exists(self.image_data_file):
            with open(self.image_data_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Image Name', 'Task Label', 'Student Name', 'Upload Date'])
        if not os.path.exists(self.task_data_file):
            with open(self.task_data_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Task Label', 'Task Description'])

    def create_config(self):
        folder_path = input("Введите путь к папке для сохранения фотографий и файлов CSV: ")
        self.folder_path = os.path.abspath(folder_path)
        self.image_data_file = os.path.join(self.folder_path, 'image_data.csv')
        self.task_data_file = os.path.join(self.folder_path, 'task_data.csv')
        self.save_config()

    def load_config(self):
        with open(self.config_file, 'r') as file:
            config = json.load(file)
            self.folder_path = config['folder_path']
            self.image_data_file = os.path.join(self.folder_path, 'image_data.csv')
            self.task_data_file = os.path.join(self.folder_path, 'task_data.csv')

    def save_config(self):
        config = {'folder_path': self.folder_path}
        with open(self.config_file, 'w') as file:
            json.dump(config, file)

    def update_folder_path(self):
        folder_path = input("Введите новый путь к папке: ")
        self.folder_path = os.path.abspath(folder_path)
        self.image_data_file = os.path.join(self.folder_path, 'image_data.csv')
        self.task_data_file = os.path.join(self.folder_path, 'task_data.csv')
        self.save_config()

    def save_data(self):
        with open(self.image_data_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Image Name', 'Task Label', 'Student Name', 'Upload Date'])
            writer.writerows(self.image_data)
        with open(self.task_data_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Task Label', 'Task Description'])
            writer.writerows(self.task_data)

    def add_image(self, image_name, task_label, student_name, upload_date):
        self.image_data.append([image_name, task_label, student_name, upload_date])

    def delete_image(self, image_name):
        for row in self.image_data:
            if row[0] == image_name:
                self.image_data.remove(row)
                break

    def view_images(self):
        for row in self.image_data:
            utils.open_image(row[0])
            print(row)

    def search_image_by_name(self, image_name):
        for row in self.image_data:
            if row[0] == image_name:
                print(row)
                break
        else:
            print("Image not found.")
