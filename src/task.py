import csv
import os

import utils
from utils import Manager

ID = 0
TASK_NAME = 1
DESCRIPTION = 2


class TaskManager(Manager):
    def __init__(self):
        super().__init__()
        self.main_folder_path = None
        self.tasks_filepath = ''
        self.tasks = []

    def load_folder_configs(self, main_folder_path):
        self.main_folder_path = main_folder_path
        self.tasks_filepath = os.path.join(main_folder_path, 'tasks.csv')
        if os.path.exists(self.tasks_filepath):
            with open(self.tasks_filepath, 'r', newline='') as file:
                reader = csv.reader(file)
                header = next(reader, None)
                for item in reader:
                    self.tasks.append(item)

    def save_folder_configs(self):
        with open(self.tasks_filepath, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Id', 'Task Name', 'Description'])
            writer.writerows(self.tasks)
        pass

    def choose_task_dialog(self):
        if len(self.tasks) < 1:
            print("\nПростите, пока нет заданий. Попросите преподавателя создать новое.")
            input("Продолжить (нажмите enter)...")
            return

        print("\nСписок заданий:")
        for i in range(len(self.tasks)):
            task = self.tasks[i]
            print(f"{i}. {task[TASK_NAME]}")
        while True:
            choice = input("\nВыберите номер задания или введите quit для выхода: ")
            if choice.isdigit() and -1 < int(choice) < len(self.tasks):
                task = self.tasks[int(choice)]
                print(f"Задание {task[TASK_NAME]} выбрано")
                return task
            elif choice == 'quit' or choice == 'q':
                break
            else:
                print("Некорректный номер. Введите правильный")
                continue

    def create_task_dialog(self):
        task_name = input("Введите имя задания: ")
        description = input("Опишите подробнее какой рисунок требуется нарисовать: ")

        id = utils.get_next_id(self.tasks, ID)
        new_task = [id, task_name, description]
        self.tasks.append(new_task)

        self.save_folder_configs()
        print(f"Задание с именем `{task_name}` и описанием `{description}` успешно создано.")

    def find_task(self, task_id):
        for i in range(len(self.tasks)):
            task = self.tasks[i]
            if task[ID] == task_id:
                return task
        return None

    @staticmethod
    def show_description(task):
        print(f"{task[ID]}. Задание {task[TASK_NAME]}. Описание: {task[DESCRIPTION]}")
