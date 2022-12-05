import multiprocessing
from _datetime import datetime
import pandas as pd
import os
from multiprocessing import Manager, Pool


class DataSet:
    """
    Класс для хранения списка вакансий.

    Attributes:
         salary_by_year (dict) : Словарь с статистикой зарплаты по годам
         vacancies_count_by_year (dict) : Словарь с общим количеством вакансии по годам
         salary_by_profession_name (dict) : Словарь с статистикой зарплаты по выбранной профессии
         vacancies_count_by_profession_name (dict) : Словарь с общим количеством вакансии по выбранной профессии
    """
    def __init__(self):
        """
        Конструктор для инициализация объекта DataSet, который создает поле для хранения списка вакансий

        Args:
             salary_by_year (dict) : Словарь с статистикой зарплаты по годам
             vacancies_count_by_year (dict) : Словарь с общим количеством вакансии по годам
             salary_by_profession_name (dict) : Словарь с статистикой зарплаты по выбранной профессии
             vacancies_count_by_profession_name (dict) : Словарь с общим количеством вакансии по выбранной профессии
        """
        self.salary_by_year = Manager().dict()
        self.vacancies_count_by_year = Manager().dict()
        self.salary_by_profession_name = Manager().dict()
        self.vacancies_count_by_profession_name = Manager().dict()


class InputConnect:
    """Класс для ввода данных и формирования отчетности о вакансиях

    Args:
        file_name (str): Название директории с чанками
        vacancy_name (str): Навзвание вакансии
    """
    def __init__(self):
        """Конструктор для инициализации объекта InputConnect"""
        self.file_name, self.vacancy_name = InputConnect.get_params()

    @staticmethod
    def get_params():
        """Статический метод для ввода данные о вакансии
        :return: Кортеж с названием файла и вакансии
        """
        file_name = input("Введите название директории с чанками: ")
        vacancy_name = input("Введите название профессии: ")
        return file_name, vacancy_name

    def read_csv_by_path(self, path: str):
        """Метод для многопоточной обработки csv файлов при помощи модуля pandas
        :param path: Путь до csv файла с вакансиями
        :param data: Объект класса DataSet
        """
        df = pd.read_csv(path)
        df["salary"] = df[["salary_from", "salary_to"]].mean(axis=1)
        df["published_at"] = df["published_at"].apply(lambda d: datetime(int(d[:4]), int(d[5:7]), int(d[8:10])).year)
        year = df["published_at"][0]
        df_vacancy = df["name"].str.contains(self.vacancy_name)

        filter_by_year = df["published_at"] == year
        salary_by_year = (year, int(df[filter_by_year]["salary"].mean()))
        vacancies_count_by_year = (year, len(df[filter_by_year]))
        salary_by_profession_name = (year, int(df[df_vacancy & filter_by_year]["salary"].mean()))
        vacancies_count_by_profession_name = (year, len(df[df_vacancy & filter_by_year]))
        return salary_by_year, vacancies_count_by_year, salary_by_profession_name, vacancies_count_by_profession_name

    def processesed(self, data: DataSet):
        """
        Метод, для создания потоков при помощи модуля multiprocessing и вывода на консоль статистики по годам
        :param data: Объект класса DataSet
        :return: None
        """
        process_args = []
        for file in os.listdir(self.file_name):
            process_args.append(f"{self.file_name}/{file}")

        pool = Pool(processes=multiprocessing.cpu_count())
        for item in pool.map(self.read_csv_by_path, process_args):
            data.salary_by_year[item[0][0]] = item[0][1]
            data.vacancies_count_by_year[item[1][0]] = item[1][1]
            data.salary_by_profession_name[item[2][0]] = item[2][1]
            data.vacancies_count_by_profession_name[item[3][0]] = item[3][1]

        pool.terminate()

        print(f"Динамика уровня зарплат по годам: {data.salary_by_year}")
        print(f"Динамика количества вакансий по годам: {data.vacancies_count_by_year}")
        print(f"Динамика уровня зарплат по годам для выбранной профессии: {data.salary_by_profession_name}")
        print(f"Динамика количества вакансий по годам для выбранной профессии: {data.vacancies_count_by_profession_name}")


if __name__ == '__main__':
    inputconnect = InputConnect()
    start_time = datetime.now()
    dataset = DataSet()
    inputconnect.processesed(dataset)
    print(f"Total time: {datetime.now() - start_time}")
