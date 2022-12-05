from _datetime import datetime
import pandas as pd
import os
from multiprocessing import Manager, Pool
import concurrent.futures as pool
import multiprocessing


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
        self.salary_by_year = dict()
        self.vacancies_count_by_year = dict()
        self.salary_by_profession_name = dict()
        self.vacancies_count_by_profession_name = dict()


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
        file_name = "vacancies" #input("Введите название директории с чанками: ")
        vacancy_name = "Программист" #input("Введите название профессии: ")
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
        with pool.ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executer:
            wait_complete = []
            for path in os.listdir(self.file_name):
                future = executer.submit(self.read_csv_by_path, f"{self.file_name}/{path}")
                wait_complete.append(future)

        for res in pool.as_completed(wait_complete):
            result = res.result()
            data.salary_by_year[result[0][0]] = result[0][1]
            data.vacancies_count_by_year[result[1][0]] = result[1][1]
            data.salary_by_profession_name[result[2][0]] = result[2][1]
            data.vacancies_count_by_profession_name[result[3][0]] = result[3][1]

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
