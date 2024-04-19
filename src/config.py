import json
import os

FOLDER_PATH = 'folder_path'

class ConfigController:
    def __init__(self):
        self.managers = None
        self.default_folder = os.path.join(os.path.expanduser('~'), 'Draw learning helper')
        self.folder_path = ''
        self.main_config_file = os.path.join(self.default_folder, 'draw_learning_helper_config.json')

    def _create_config_dialog(self):
        while True:
            choice = input("Нажмите enter если Вы хотите оставить все по умолчанию"
                           " или введите change для изменения папки: ")
            if choice is None or choice == '':
                self.folder_path = self.default_folder
                break
            elif choice == 'c' or choice == 'change':
                new_folder_path = input(
                    "Введите путь к папке для хранения пользователей, фотографий и заданий (можете указать "
                    "ранее используемую папку чтобы восстановить настройки): ")
                self.folder_path = os.path.abspath(new_folder_path)
                break
            else:
                print("Неправильный ввод, попробуйте ещё раз.")

        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)
        self._save_main_config()

    def _save_main_config(self):
        config = {FOLDER_PATH: self.folder_path}
        with open(self.main_config_file, 'w') as file:
            json.dump(config, file)

    def _load_main_config(self):
        with open(self.main_config_file, 'r') as file:
            config = json.load(file)
            self.folder_path = config[FOLDER_PATH]

    def _update_folder_path(self):
        folder_path = input("Введите новый путь к папке: ")
        self.folder_path = os.path.abspath(folder_path)
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)
        self._save_main_config()

    def _load_folder_configs(self):
        for manager in self.managers:
            manager.load_folder_configs(self.folder_path)

    def initialize(self, managers):
        print()
        self.managers = managers
        if not os.path.exists(self.main_config_file):
            print("Добро пожаловать первый раз в программу!")
            print(f"По умолчанию все настройки и работы студентов будут храниться в {self.default_folder} "
                  "\nНо может Вы хотите поменять путь?")
            self._create_config_dialog()
        else:
            self._load_main_config()
            if not os.path.exists(self.folder_path):
                print("Папка с настройками не найдена.")
                self._update_folder_path()
            else:
                print("Обнаружена папка с настройками `" + self.folder_path + "`.")
                print("Оставить ее или поменять?")
                self._create_config_dialog()

        self._load_folder_configs()

    def save_on_close(self):
        for manager in self.managers:
            manager.save_folder_configs()
