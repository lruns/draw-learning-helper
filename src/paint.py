import csv
import os
from datetime import datetime

from PIL import Image

import utils
from task import DESCRIPTION, TASK_NAME
from utils import Manager, open_image

ID = 0
IMAGE_NAME = 1
TASK_ID = 2
STUDENT_ID = 3
UPLOAD_DATE = 4
MAYBE_RELATE_TO_TASK = 5
MAYBE_DUPLICAT = 6
APPROVED = 7
COMMENT = 8
CHECK_DATE = 9
CORRECTED_IMAGE_ID = 10


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
            writer.writerow(
                ['Id', 'Image Name', 'Task Id', 'Student Id', 'Upload Date', 'Maybe relate to task',
                 'Maybe duplicat', 'Approved', 'Comment', 'Check Date', 'Corrected by student - next image id'])
            writer.writerows(self.image_data)
        pass

    # def delete_image(self, id):
    #     for row in self.image_data:
    #         if row[ID] == id:
    #             self.image_data.remove(row)
    #             break

    def _view_student_works(self, student_id):
        student_image_data = []
        for row in self.image_data:
            if row[STUDENT_ID] == student_id:
                student_image_data.append(row)
        return student_image_data

    def _view_task_works(self, task_id):
        task_image_data = []
        for row in self.image_data:
            if row[TASK_ID] == task_id:
                task_image_data.append(row)
        return task_image_data

    def open_image_window(self, image_id):
        open_image(os.path.join(self.main_folder_path, image_id + ".jpg"))

    def get_image(self, image_id):
        path = os.path.join(self.main_folder_path, image_id + ".jpg")
        return Image.open(path)

    # def search_image_by_name(self, image_name):
    #     for row in self.image_data:
    #         if row[IMAGE_NAME] == image_name:
    #             print(row)
    #             break
    #     else:
    #         print("Image not found.")

    def create_paint_dialog(self, student_id, task, similarity, unique_search):
        print("\nВнимание! Если рисунок не будет соответствовать выбранному заданию или если рисунок будет "
              "являться плагиатом, то проверяющий отклонит Ваш рисунок!")
        while True:
            image_filepath = input("Введите путь к изображению (должен быть формат jpg или png): ")
            if os.path.exists(image_filepath) and image_filepath.lower().endswith(
                    ('.png', '.jpg', '.jpeg')):
                break
            else:
                print("Некорректный путь. Введите правильный")
                continue

        image_name = input("Введите имя изображения: ")
        task_id = task[ID]
        upload_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        id = utils.get_next_id(self.image_data, ID)

        # Converting and copying the image to the destination folder
        raw_img = Image.open(image_filepath)
        img = raw_img.convert('RGB')
        destination_path = os.path.join(self.main_folder_path, id + '.jpg')
        img.save(destination_path, 'JPEG')

        relate_to_task = similarity.compare_paint_and_task(img, task[DESCRIPTION])
        duplicat = len(unique_search.find_duplicates(img)) > 0

        image_data = [id, image_name, task_id, student_id, upload_date, str(relate_to_task), str(duplicat), None, None,
                      None,
                      None]
        self.image_data.append(image_data)

        unique_search.add_image(img, id)

        self.save_folder_configs()
        print(f"Изображение `{image_name}` добавлено.")
        return id

    def show_images_dialog(self, student_id, unique_search, task_manager, other_student_name=None):
        paints = self._view_student_works(student_id)
        if len(paints) < 1:
            print("\nПока нет рисунков.")
            input("Продолжить (нажмите enter)...")
            return

        while True:
            print()
            if other_student_name is None:
                print("Ваши работы: ")
            else:
                print(f"Работы студента `{other_student_name}`: ")

            for i in range(len(paints)):
                paint = paints[i]
                task = task_manager.find_task(paint[TASK_ID])
                print(f"{i}. {paint[IMAGE_NAME]} - задание {task[TASK_NAME]}")

            choice = input("\nВыберите номер рисунка для просмотра или поиска похожих. Или наберите quit для выхода: ")
            if choice.isdigit() and -1 < int(choice) < len(paints):
                chosen_image_id = paints[int(choice)][ID]

                while True:
                    choice2 = input("Наберите open для просмотра или search для поиска похожих изображений."
                                    " Или наберите quit для выхода: ")
                    if choice2 == 'open' or choice2 == 'open':
                        self.open_image_window(chosen_image_id)
                        print("Открываем...")
                        break
                    elif choice2 == 'search' or choice2 == 's':
                        ids = unique_search.fetch_similar(self.get_image(chosen_image_id))
                        try:
                            ids.remove(chosen_image_id)
                        except ValueError:
                            pass
                        self.show_images_by_ids(ids, "Поиск выдал следующие похожие изображения:")
                        break
                    elif choice2 == 'quit' or choice2 == 'q':
                        break
                    else:
                        print("Некорректный ввод. Попробуйте ещё.")
                        continue

            elif choice == 'quit' or choice == 'q':
                break
            else:
                print("Некорректный номер. Введите правильный")
                continue

    def show_images_by_ids(self, image_ids, title):
        if len(image_ids) < 1:
            print("Нет рисунков по данному запросу.")
            input("Продолжить (нажмите enter)...")
            return
        else:
            print(title)

        paints = []
        for row in self.image_data:
            if row[ID] in image_ids:
                paints.append(row)

        for i in range(len(paints)):
            paint = paints[i]
            print(f"{i}. {paint[IMAGE_NAME]}")

        while True:
            choice = input("\nВыберите номер рисунка для просмотра или наберите quit для выхода: ")
            if choice.isdigit() and -1 < int(choice) < len(paints):
                self.open_image_window(paints[int(choice)][ID])
                print("Открываем...")
            elif choice == 'quit' or choice == 'q':
                break
            else:
                print("Некорректный номер. Введите правильный")
                continue

    def get_not_checked_works(self, student_id=None):
        not_checked_works = []
        for row in self.image_data:
            try:
                exist = row[APPROVED]
                if exist is None or not exist:
                    not_checked_works.append(row)
            except IndexError:
                pass
        return not_checked_works

    def check_work_dialog(self, image_data):
        approved = None
        while True:
            choice = input("\nНаберите accept или decline для подтверждения или отклонения работы соответственно. Или "
                           "наберите quit для выхода: ")
            if choice == 'accept' or choice == 'a':
                approved = True
                break
            elif choice == 'decline' or choice == 'd':
                approved = False
                break
            elif choice == 'quit' or choice == 'q':
                return False
            else:
                print("Некорректный номер. Введите правильный")
                continue

        comment = input("Пожалуйста, напишите комментарий к работе: ")
        image_data[APPROVED] = str(approved)
        image_data[COMMENT] = comment
        image_data[CHECK_DATE] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.save_folder_configs()
        return True

    def checked_works_dialog(self, student_id, task_manager, similarity, unique_search):

        approved_works = []
        declined_works = []

        for row in self.image_data:
            if row[STUDENT_ID] != student_id:
                continue
            try:
                correct_id = row[CORRECTED_IMAGE_ID]
                if not (correct_id is None or not correct_id):
                    continue
            except IndexError:
                continue
            try:
                approved = row[APPROVED]
                if approved == 'True':
                    approved_works.append(row)
                elif approved == 'False':
                    declined_works.append(row)
            except IndexError:
                pass

        if len(approved_works) + len(declined_works) == 0:
            print("Пока нет никаких проверок. Попросите преподавателя проверить, если ранее загрузили работу.")
            input("Продолжить (нажмите enter)...")
            return

        if len(approved_works) > 0:
            print("\nПринятые работы:")
            for i in range(len(approved_works)):
                paint = approved_works[i]
                print(f"{i}. {paint[IMAGE_NAME]} - комментарий: {paint[COMMENT]}")

        if len(declined_works) > 0:
            print("Отклоненные работы:")
            for i in range(len(declined_works)):
                paint = declined_works[i]
                print(f"{i}. {paint[IMAGE_NAME]} - комментарий: {paint[COMMENT]}")

        while True:
            if len(declined_works) > 0:
                choice = input("\nВыберите номер отклоненной работы для исправления или наберите quit для выхода: ")
            else:
                choice = input("\nОтклоненных работ нет, наберите quit для выхода: ")
            if choice.isdigit() and -1 < int(choice) < len(declined_works):
                work = declined_works[int(choice)]
                task = task_manager.find_task(work[TASK_ID])
                correct_id = self.create_paint_dialog(student_id, task, similarity, unique_search)
                work[CORRECTED_IMAGE_ID] = correct_id
                declined_works.remove(work)
            elif choice == 'quit' or choice == 'q':
                break
            else:
                print("Некорректный ввод. Введите правильный.")
                continue
