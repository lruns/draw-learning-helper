import datetime
from alive_progress import alive_bar
from PIL import Image

from paint_manager import photoManager
from similarity_model import SimilarityModel
from unique_search_model import UniqueSearchModel


def load_modules():
    print("Загружаем модули для работы программы:")
    with alive_bar(2) as bar:
        photo_manager = photoManager()
        bar()
        # similarity = SimilarityModel()
        # bar()
        unique_search = UniqueSearchModel()
        # image = Image.open('demo.jpg')
        # unique_search.is_duplicate(image, image)
        bar()
    print("Модули загружены!")
    return photo_manager, None, unique_search


def main():
    print("Draw learning helper запущен...")

    photo_manager, similarity, unique_search = load_modules()
    photo_manager.start()

    while True:
        print("\nМеню:")
        print("1. Добавить изображение")
        print("2. Удалить изображение")
        print("3. Просмотреть изображения")
        print("4. Найти изображение по имени")
        print("5. Выход")

        choice = input("Выберите действие: ")

        if choice == '1':
            image_name = input("Введите имя изображения: ")
            task_label = input("Введите метку задания: ")
            student_name = input("Введите имя студента: ")
            upload_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            photo_manager.add_image(image_name, task_label, student_name, upload_date)
            print("Изображение добавлено.")
        elif choice == '2':
            image_name = input("Введите имя изображения для удаления: ")
            photo_manager.delete_image(image_name)
            print("Изображение удалено.")
        elif choice == '3':
            print("Изображения:")
            photo_manager.view_images()
        elif choice == '4':
            image_name = input("Введите имя изображения для поиска: ")
            photo_manager.search_image_by_name(image_name)
        elif choice == '5':
            print("Выход.")
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите снова.")

    photo_manager.save_data()


if __name__ == "__main__":
    main()
