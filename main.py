from Task2_1_1 import main_excel
from Task2_1_3 import main_pdf

data = input("Введите 'Вакансии' для формирование табличнх вакансии или 'Статистика' для формирования отчета: ")
if data == "Вакансии":
    main_excel()
elif data == "Статистика":
    main_pdf()

