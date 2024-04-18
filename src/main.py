from alive_progress import alive_bar

from config import ConfigController
from paint import PaintManager, IMAGE_NAME, TASK_ID, UPLOAD_DATE, MAYBE_RELATE_TO_TASK, MAYBE_DUPLICAT
from similarity import SimilarityModel
from task import TaskManager, TASK_NAME
from unique_search import UniqueSearchModel
from user import UserManager, ROLE, ID, FULL_NAME

import warnings
warnings.filterwarnings("ignore")

config_controller: ConfigController
user_manager: UserManager
paint_manager: PaintManager
task_manager: TaskManager
similarity: SimilarityModel
unique_search: UniqueSearchModel

current_user: list


def load_modules():
    print("Загружаем модули для работы программы:")
    with alive_bar(6) as bar:
        config_controller = ConfigController()
        bar()
        user_manager = UserManager()
        bar()
        paint_manager = PaintManager()
        bar()
        task_manager = TaskManager()
        bar()
        similarity = SimilarityModel()
        bar()
        unique_search = UniqueSearchModel()
        bar()
    print("Модули загружены!")
    return config_controller, user_manager, paint_manager, task_manager, similarity, unique_search


def user_choose_commands():
    global current_user
    while True:
        choice = input("\nВыбрать пользователя или создать нового (1 или 2): ")
        if choice == '1':
            current_user = user_manager.choose_user_dialog()
            break
        elif choice == '2':
            user_manager.create_user_dialog()
            continue
        else:
            print("Неправильная команда.")
            continue


def show_other_students_works():
    students = user_manager.get_students()
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
            paint_manager.show_images_dialog(student[ID], unique_search, task_manager, student[FULL_NAME])
        elif choice == "quit" or choice == "q":
            break
        else:
            print("Некорректный номер. Введите правильный")
            continue


def check_student_work():
    works = paint_manager.get_not_checked_works()
    if len(works) < 1:
        print("\nНет работ для проверки.")
        input("Продолжить (нажмите enter)...")
        return
    else:
        print("\nВыберите номер рисунка, который Вы хотели бы проверить.")

    for i in range(len(works)):
        work = works[i]
        task = task_manager.find_task(work[TASK_ID])
        comparable_with_task = "совпадает с заданием" if work[
            MAYBE_RELATE_TO_TASK] == 'True' else "возможно расхождение с заданием"
        plagiat = "возможно работа является плагиатом" if work[MAYBE_DUPLICAT] == 'True' else "плагиат не обнаружен"
        print(f"{i}. Рисунок {work[IMAGE_NAME]}, задание `{task[TASK_NAME]}`"
              f" - {comparable_with_task}, {plagiat}, загружен {work[UPLOAD_DATE]}. ")

    checked_ids = []

    while True:
        choice = input("\nНомер работы или quit для выхода: ")
        if choice in checked_ids:
            print(f"Работа {choice} уже была проверена Вами, выберите другую.")
        elif choice.isdigit() and -1 < int(choice) < len(works):
            work = works[int(choice)]
            image = paint_manager.get_image(work[ID])
            while True:
                print("\nМеню:")
                print("1 - Открыть изображение")
                print("2 - Показать подробное описание задания")
                print("3 - Показать плагиаты (если есть)")
                print("4 - Подтвердить или отклонить рисунок")
                print("quit - выход")
                choice2 = input("Выберите действие: ")
                if choice2 == "1":
                    paint_manager.open_image_window(work[ID])
                    print("Открываем...")
                elif choice2 == "2":
                    task = task_manager.find_task(work[TASK_ID])
                    task_manager.show_description(task)
                    input("Продолжить (нажмите enter)...")
                elif choice2 == "3":
                    ids = unique_search.find_duplicates(image)
                    try:
                        ids.remove(work[ID])
                    except ValueError:
                        pass
                    paint_manager.show_images_by_ids(ids, "Список возможных дубликатов:")
                elif choice2 == "4":
                    if paint_manager.check_work_dialog(work):
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


def main_commands():
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
                task = task_manager.choose_task_dialog()
                if task is None:
                    continue
                paint_manager.create_paint_dialog(current_user[ID], task, similarity, unique_search)
            elif choice == '2':
                paint_manager.show_images_dialog(current_user[ID], unique_search, task_manager)
            elif choice == '3':
                show_other_students_works()
            elif choice == '4':
                paint_manager.checked_works_dialog(current_user[ID], task_manager, similarity, unique_search)
            elif choice == 'user' or choice == 'u':
                user_choose_commands()
                main_commands()
                break
            elif choice == 'quit' or choice == 'q':
                print("Выход.")
                break
            else:
                print("Неверный выбор. Пожалуйста, выберите снова.")
        elif current_user[ROLE] == 'teacher':
            if choice == '1':
                task_manager.create_task_dialog()
            elif choice == '2':
                check_student_work()
            elif choice == 'user' or choice == 'u':
                user_choose_commands()
                main_commands()
                break
            elif choice == 'quit' or choice == 'q':
                print("Выход.")
                break
            else:
                print("Неверный выбор. Пожалуйста, выберите снова.")


def main():
    print("Draw learning helper запущен...")

    global config_controller, user_manager, paint_manager, task_manager, similarity, unique_search
    config_controller, user_manager, paint_manager, task_manager, similarity, unique_search = load_modules()

    config_controller.initialize([user_manager, paint_manager, task_manager])
    unique_search.initialize(
        [[paint_manager.get_image(row[ID]), row[ID]] for row in paint_manager.image_data]
    )

    if len(user_manager.users) < 1:
        print("\nНеобходимо создать пользователя.")
        user_manager.create_user_dialog()

    user_choose_commands()
    main_commands()

    config_controller.save_on_close()


if __name__ == "__main__":
    main()