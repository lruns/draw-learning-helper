import datetime

from alive_progress import alive_bar

from config import ConfigController
from paint import PaintManager
from similarity import SimilarityModel
from task import TaskManager
from unique_search import UniqueSearchModel
from user import UserManager, ROLE

#import warnings
#warnings.filterwarnings("ignore")

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
        # similarity = SimilarityModel()
        bar()
        # unique_search = UniqueSearchModel()
        bar()
    print("Модули загружены!")
    # return config_controller, user_manager, paint_manager, task_manager, similarity, unique_search
    return config_controller, user_manager, paint_manager, task_manager, None, None


def main():
    print("Draw learning helper запущен...")

    config_controller, user_manager, paint_manager, task_manager, similarity, unique_search = load_modules()
    config_controller.initialize([user_manager, paint_manager, task_manager])

    current_user = None

    if len(user_manager.users) < 1:
        print("\nНеобходимо создать пользователя.")
        user_manager.create_user_dialog()

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

    while True:
        print("\nМеню:")

        if current_user[ROLE] == 'student':
            print("1. Загрузить изображение для задания")
            print("2. Просмотреть свои работы")
            print("3. Просмотреть работы других студентов")
            print("4. Просмотреть проверки от преподавателя")
            print("9. Поменять пользователя")
            print("10. Выход")
        elif current_user[ROLE] == 'teacher':
            print("1. Создать новое задание")
            print("2. Просмотреть требующие проверку работы студентов")
            print("9. Поменять пользователя")
            print("10. Выход")

        choice = input("Выберите действие: ")

        if current_user[ROLE] == 'student':
            if choice == '1':
                # нужно функционал который предупредит студента, что его рисунок заброкуют если не будет соотвествовать заданию
                image_name = input("Введите имя изображения: ")
                task_label = input("Введите метку задания: ")
                student_name = paint_manager.current_user.username
                upload_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                paint_manager.add_image(image_name, task_label, student_name, upload_date)
                print("Изображение добавлено.")
            elif choice == '2':
                print("Ваши работы:")
                # нужен функционал, чтобы можно было найти по своему рисунку похожие
                paint_manager.view_images(student=paint_manager.current_user.username)
            elif choice == '3':
                print("Работы других студентов:")
                paint_manager.view_images(student=None)
            elif choice == '4':
                print("Проверки от преподавателя:")
                # нужно чтобы видно было, принят ли рисунок или нет
            elif choice == '9':
                pass
                # goto change user
            elif choice == '10':
                print("Выход.")
                break
            else:
                print("Неверный выбор. Пожалуйста, выберите снова.")
        elif current_user[ROLE] == 'teacher':
            if choice == '1':
                pass
                # Добавьте функционал создания нового задания
            elif choice == '2':
                print("Работы студентов:")
                print("1. Проверить на плагиат")
                print("2. Просмотреть требующие проверку работы студентов")
                print("3. Назад")
                # тут пишется, какой студент, какое задание, есть ли подозрение на плагиат, есть ли подозрение что не соответствует заданию
                # и можно или принять рисунок или нет, с комментарием
            elif choice == '9':
                pass
                # goto change user
            elif choice == '10':
                print("Выход.")
                break
            else:
                print("Неверный выбор. Пожалуйста, выберите снова.")

    config_controller.save_on_close()


if __name__ == "__main__":
    main()
