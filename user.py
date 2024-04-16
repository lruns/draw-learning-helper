import csv
import os

import utils
from utils import Manager

ID = 0
FULL_NAME = 1
ROLE = 2


class UserManager(Manager):
    def __init__(self):
        super().__init__()
        self.main_folder_path = None
        self.users_filepath = ''
        self.users = []

    def load_folder_configs(self, main_folder_path):
        self.main_folder_path = main_folder_path
        self.users_filepath = os.path.join(main_folder_path, 'users.csv')
        if os.path.exists(self.users_filepath):
            with open(self.users_filepath, 'r', newline='') as file:
                reader = csv.reader(file)
                header = next(reader, None)
                for item in reader:
                    self.users.append(item)

    def save_folder_configs(self):
        with open(self.users_filepath, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Id', 'Full Name', 'Role'])
            writer.writerows(self.users)
        pass

    def choose_user_dialog(self):
        print("Список пользователей:")
        for i in range(len(self.users)):
            user = self.users[i]
            print(f"{i}. {user[FULL_NAME]} ({user[ROLE]})")
        choice = input("Выберите номер пользователя: ")
        while True:
            if choice.isdigit() and -1 < int(choice) < len(self.users):
                user = self.users[int(choice)]
                print(f"Пользователь {user[FULL_NAME]} выбран")
                return user
            else:
                print("Некорректный номер. Введите правильный")
                continue

    def create_user_dialog(self):
        fullname = input("Введите имя пользователя: ")
        role = input("Выберите тип пользователя (student или teacher): ").lower()
        while True:
            if role == 'student' or role == 'teacher':
                break
            else:
                print("Некорректный тип пользователя. Введите правильный")
                continue

        id = utils.get_next_id(self.users, ID)
        self.users.append([id, fullname, role])
        print(f"Пользователь {role} с именем {fullname} успешно создан.")
