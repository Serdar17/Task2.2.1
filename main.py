from Task5_2 import print_vacancies
from Task2_1_3 import main_pdf

data = input("Выберите способ формирования таблиц: ")
if data == "Вакансии":
    print_vacancies()
elif data == "Статистика":
    main_pdf()
