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

    def add_task(self, task_name, description):
        id = utils.get_next_id(self.tasks, ID)
        new_task = [id, task_name, description]
        self.tasks.append(new_task)
