import json
import os

FOLDER_PATH = 'folder_path'

class ConfigController:
    def __init__(self):
        self.managers = None
        self.config_file = os.path.join(os.path.expanduser('~'), '.draw_learning_helper_config.json')
        self.folder_path = ''

    def _create_config(self):
        folder_path = input("Введите путь к папке для хранения пользователей, фотографий и заданий (можете указать "
                            "ранее используемую папку чтобы восстановить настройки): ")
        self.folder_path = os.path.abspath(folder_path)
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)
        self._save_config()

    def _save_config(self):
        config = {FOLDER_PATH: self.folder_path}
        with open(self.config_file, 'w') as file:
            json.dump(config, file)

    def _load_config(self):
        with open(self.config_file, 'r') as file:
            config = json.load(file)
            self.folder_path = config[FOLDER_PATH]

    def _update_folder_path(self):
        folder_path = input("Введите новый путь к папке: ")
        self.folder_path = os.path.abspath(folder_path)
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)
        self._save_config()

    def _load_folder_configs(self):
        for manager in self.managers:
            manager.load_folder_configs(self.folder_path)

    def initialize(self, managers):
        self.managers = managers
        if not os.path.exists(self.config_file):
            "Добро пожаловать первый раз в программу!"
            self._create_config()
        else:
            self._load_config()
            if not os.path.exists(self.folder_path):
                print("Папка с настройками не найдена.")
                self._update_folder_path()
            else:
                print("Обнаружена папка с настройками `" + self.folder_path + "`.")

        self._load_folder_configs()

    def save_on_close(self):
        for manager in self.managers:
            manager.save_folder_configs()

    def get_main_folder(self):
        return self.folder_path
