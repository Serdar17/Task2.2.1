from Task5_2 import print_vacancies
from Task2_1_3 import main_pdf

data = input("Введите 'Вакансии' для формирование табличнх вакансии или 'Статистика' для формирования отчета: ")
if data == "Вакансии":
    print_vacancies()
elif data == "Статистика":
    main_pdf()
