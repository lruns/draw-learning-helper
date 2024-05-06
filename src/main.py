from alive_progress import alive_bar

from config import ConfigController
from paint import PaintManager, IMAGE_NAME, TASK_ID, UPLOAD_DATE, MAYBE_RELATE_TO_TASK, MAYBE_DUPLICATE
from similarity import SimilarityModel
from task import TaskManager, TASK_NAME
from unique_search import UniqueSearchModel
from user import UserManager, ROLE, ID, FULL_NAME

import warnings
warnings.filterwarnings("ignore")

class Main:
    def __init__(self):
        print("Загружаем модули для работы программы:")
        with alive_bar(6) as bar:
            self.config_controller = ConfigController()
            bar()
            self.user_manager = UserManager()
            bar()
            self.paint_manager = PaintManager()
            bar()
            self.task_manager = TaskManager()
            bar()
            self.similarity = SimilarityModel()
            bar()
            self.unique_search = UniqueSearchModel()
            bar()
        print("Модули загружены!")

        self.current_user = []

        self.config_controller.initialize([self.user_manager, self.paint_manager, self.task_manager])
        self.unique_search.initialize(
            [[self.paint_manager.get_image(row[ID]), row[ID]] for row in self.paint_manager.image_data]
        )

    def user_choose_commands(self):
        global current_user
        while True:
            choice = input("\nВыбрать пользователя или создать нового (1 или 2): ")
            if choice == '1':
                current_user = self.user_manager.choose_user_dialog()
                break
            elif choice == '2':
                self.user_manager.create_user_dialog()
                continue
            else:
                print("Неправильная команда.")
                continue


    def show_other_students_works(self):
        students = self.user_manager.get_students()
        if len(students) < 2:
            print("\nПростите, пока нет других студентов кроме Вас.")
            input("Продолжить (нажмите enter)...")
            return
        for i in range(len(students)):
            student = students[i]
            if student[ID] == current_user[ID]:
                continue
            print(f"{i}. {student[FULL_NAME]}")
        while True:
            choice = input("\nВыберите студента или наберите quit для выхода: ")
            if choice.isdigit() and -1 < int(choice) < len(students):
                student = students[int(choice)]
                self.paint_manager.show_images_dialog(student[ID], self.unique_search, self.task_manager, student[FULL_NAME])
            elif choice == "quit" or choice == "q":
                break
            else:
                print("Некорректный номер. Введите правильный")
                continue


    def check_student_work(self):
        works = self.paint_manager.get_not_checked_works()
        if len(works) < 1:
            print("\nНет работ для проверки.")
            input("Продолжить (нажмите enter)...")
            return
        else:
            print("\nВыберите номер рисунка, который Вы хотели бы проверить.")

        for i in range(len(works)):
            work = works[i]
            task = self.task_manager.find_task(work[TASK_ID])
            comparable_with_task = "совпадает с заданием" if work[
                MAYBE_RELATE_TO_TASK] == 'True' else "возможно расхождение с заданием"
            plagiat = "возможно работа является плагиатом" if work[MAYBE_DUPLICATE] == 'True' else "плагиат не обнаружен"
            print(f"{i}. Рисунок {work[IMAGE_NAME]}, задание `{task[TASK_NAME]}`"
                  f" - {comparable_with_task}, {plagiat}, загружен {work[UPLOAD_DATE]}. ")

        checked_ids = []

        while True:
            choice = input("\nНомер работы или quit для выхода: ")
            if choice in checked_ids:
                print(f"Работа {choice} уже была проверена Вами, выберите другую.")
            elif choice.isdigit() and -1 < int(choice) < len(works):
                work = works[int(choice)]
                image = self.paint_manager.get_image(work[ID])
                while True:
                    print("\nМеню:")
                    print("1 - Открыть изображение")
                    print("2 - Показать подробное описание задания")
                    print("3 - Показать плагиаты (если есть)")
                    print("4 - Подтвердить или отклонить рисунок")
                    print("quit - выход")
                    choice2 = input("Выберите действие: ")
                    if choice2 == "1":
                        self.paint_manager.open_image_window(work[ID])
                        print("Открываем...")
                    elif choice2 == "2":
                        task = self.task_manager.find_task(work[TASK_ID])
                        self.task_manager.show_description(task)
                        input("Продолжить (нажмите enter)...")
                    elif choice2 == "3":
                        ids = self.unique_search.find_duplicates(image)
                        try:
                            ids.remove(work[ID])
                        except ValueError:
                            pass
                        self.paint_manager.show_images_by_ids(ids, "Список возможных дубликатов:")
                    elif choice2 == "4":
                        if self.paint_manager.check_work_dialog(work):
                            checked_ids.append(choice)
                        break
                    elif choice2 == 'quit' or choice2 == 'q':
                        break
                    else:
                        print("Неверный выбор. Пожалуйста, выберите снова.")
                        continue
                break
            elif choice == 'quit' or choice == 'q':
                break
            else:
                print("Неправильный номер.")
                continue


    def main_commands(self):
        while True:
            print("\nМеню:")

            if current_user[ROLE] == 'student':
                print("1 - Загрузить изображение для задания")
                print("2 - Просмотреть свои работы")
                print("3 - Просмотреть работы других студентов")
                print("4 - Просмотреть проверки от преподавателя")
                print("user - Поменять или создать пользователя")
                print("quit - Выход")
            elif current_user[ROLE] == 'teacher':
                print("1 - Создать новое задание")
                print("2 - Просмотреть требующие проверку работы студентов")
                print("user - Поменять или создать пользователя")
                print("quit - Выход")

            choice = input("Выберите действие: ")

            if current_user[ROLE] == 'student':
                if choice == '1':
                    task = self.task_manager.choose_task_dialog()
                    if task is None:
                        continue
                    self.paint_manager.create_paint_dialog(current_user[ID], task, self.similarity, self.unique_search)
                elif choice == '2':
                    self.paint_manager.show_images_dialog(current_user[ID], self.unique_search, self.task_manager)
                elif choice == '3':
                    self.show_other_students_works()
                elif choice == '4':
                    self.paint_manager.checked_works_dialog(current_user[ID], self.task_manager, self.similarity, self.unique_search)
                elif choice == 'user' or choice == 'u':
                    self.user_choose_commands()
                    self.main_commands()
                    break
                elif choice == 'quit' or choice == 'q':
                    print("Выход.")
                    break
                else:
                    print("Неверный выбор. Пожалуйста, выберите снова.")
            elif current_user[ROLE] == 'teacher':
                if choice == '1':
                    self.task_manager.create_task_dialog()
                elif choice == '2':
                    self.check_student_work()
                elif choice == 'user' or choice == 'u':
                    self.user_choose_commands()
                    self.main_commands()
                    break
                elif choice == 'quit' or choice == 'q':
                    print("Выход.")
                    break
                else:
                    print("Неверный выбор. Пожалуйста, выберите снова.")


    def run(self):
        print("Draw learning helper запущен...")

        if len(self.user_manager.users) < 1:
            print("\nНеобходимо создать пользователя.")
            self.user_manager.create_user_dialog()

        self.user_choose_commands()
        self.main_commands()

        self.config_controller.save_on_close()


if __name__ == "__main__":
    main = Main()
    main.run()
