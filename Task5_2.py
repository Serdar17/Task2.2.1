import csv
from _datetime import datetime
import re
import prettytable
from prettytable import PrettyTable

"""Словарь для перевода названий колонок в csv файле"""
dic_naming = {"name": "Название", "description": "Описание", "key_skills": "Навыки", "experience_id": "Опыт работы",
              "premium": "Премиум-вакансия", "employer_name": "Компания", "salary_to": "Оклад",
              "area_name": "Название региона",
              "published_at": "Дата публикации вакансии", "True": "Да", "False": "Нет", "FALSE": "FALSE",
              "TRUE": "TRUE",
              "value": "Идентификатор валюты оклада"}

"""Словарь для перевода полей класса Vacancy с опытой работы"""
work_experience = {"noExperience": "Нет опыта", "between1And3": "От 1 года до 3 лет",
                   "between3And6": "От 3 до 6 лет", "moreThan6": "Более 6 лет"}

"""Словарь для лексикографической сортировки вакансий"""
work_experience_id = {"Нет опыта": 1, "От 1 года до 3 лет": 2, "От 3 до 6 лет": 3, "Более 6 лет": 4}

"""Словарь для перевода поля с валютой оклада"""
currencies = {"AZN": "Манаты", "BYR": "Белорусские рубли", "EUR": "Евро", "GEL": "Грузинский лари",
              "KGS": "Киргизский сом",
              "KZT": "Тенге", "RUR": "Рубли", "UAH": "Гривны", "USD": "Доллары", "UZS": "Узбекский сум"}

"""Словарь для перевода з/п в рубли"""
currency_to_rub = {
    "AZN": 35.68, "BYR": 23.91, "EUR": 59.90, "GEL": 21.74, "KGS": 0.76,
    "KZT": 0.13, "RUR": 1, "UAH": 1.64, "USD": 60.66, "UZS": 0.0055}


class DataSet:
    """Класс для хранения списка вакансий.

    Attributes:
        file_name (str): Название файла
        vacancies_objects (list): Список вакансий
    """
    def __init__(self, file_name):
        """
        Конструктор для инициализация объекта DataSet, который создает поле для хранения списка вакансий

        Args:
             file_name (str): Название файла
        """
        self.file_name = file_name
        self.vacancies_objects = list()

    def get_dataset(self):
        """ Считывает и фильтрует csv файл и формирует из строк объекты типа Vacancy для хранения в списке

        :return:
            DataSet: Объект класса DataSet
        """
        data = self.csv_reader()
        dict_list = self.csv_filter(data[0], data[1])
        for item in dict_list:
            args = list()
            salary = None
            skills = list()
            for key, value in item.items():
                if key == "key_skills":
                    skills = value.split('; ')
                elif key == "salary_from":
                    salary = Salary(value)
                else:
                    args.append(value)
            vacancy = Vacancy(args)
            vacancy.key_skills = skills
            vacancy.salary = salary
            self.vacancies_objects.append(vacancy)
        return self

    def remove_tags_and_spaces(self, items):
        """ Очищает строки от тегов и пустых пробелов

        Args:
            items (list): Список строк

        :returns:
            list: Cписок очищенных строк
        """
        for i in range(len(items)):
            items[i] = " ".join(re.sub(r"\<[^>]*\>", "", items[i]).split())
        return items

    def csv_reader(self):
        """ Считывает csv файл

        :returns:
            str: Строка с заголовками csv файла
            list: Список строк
        """
        with open(self.file_name, "r", encoding="utf-8-sig", newline="") as file:
            data = [x for x in csv.reader(file)]
        if len(data) == 0:
            print("Пустой файл")
            exit(0)
        if len(data) == 1:
            print("Нет данных")
            exit(0)
        columns = data[0]
        rows = [x for x in data[1:] if len(x) == len(columns) and not x.__contains__("")]
        return columns, rows

    def csv_filter(self, columns, rows):
        """Фильтрует и формирует из строк csv файла список словарей

        :param columns: Строка с заголовками csv файла
        :param rows: Список строк csv файла
        :return:
            list: Список словарей где key - это название колонки, а value - значение в определенной строке
        """
        dic_list = list()
        for row in rows:
            dic_result = dict()
            for i in range(len(row)):
                items = self.remove_tags_and_spaces(row[i].split('\n'))
                dic_result[columns[i]] = items[0] if len(items) == 1 else "; ".join(items)
            dic_result["premium"] = dic_naming[dic_result["premium"]]
            dic_result["salary_from"] = [dic_result["salary_from"], dic_result.pop("salary_to"),
                                         dic_result.pop("salary_gross"), dic_result.pop("salary_currency")]
            dic_list.append(dic_result)
        return dic_list


class Vacancy:
    """
    Класс для предоставления вакансии.

    Attributes:
        name (str): Название вакансии
        description (str): Описание вакансии
        key_skills (list): Название вакансии
        experience_id (str): Опыт работы
        premium (str): Премиум вакансия
        employer_name (str): Название компании
        salary (Salary): Объект класса Salary
        area_name (str): Название региона
        published_at (str): Дата публикации вакансии
    """
    def __init__(self, args):
        """Конструктов для инициализации вакансии

        :param args: Список строк с данными о вакансии
        """
        self.name = args[0]
        self.description = args[1]
        self.key_skills = list()
        self.experience_id = args[2]
        self.premium = args[3]
        self.employer_name = args[4]
        self.salary = None
        self.area_name = args[5]
        self.published_at = args[6]


class Salary:
    """
    Класс для предоставления зарплаты.

    Attributes:
        salary_from (str): Нижняя граница вилки оклада
        salary_to (str): Верхняя граница вилки оклада
        salary_gross (str): Описание налога
        salary_currency (str): Валюта оклада
    """
    def __init__(self, args):
        """Конструктов для инициализации зарплаты

        :param args: Список строк с данными о зарплате
        """
        self.salary_from = args[0]
        self.salary_to = args[1]
        self.salary_gross = args[2]
        self.salary_currency = args[3]


class InputConnect:
    """Класс для ввода данных и формирования вакансии в табличках

    Args:
        params (tuple): Кортеж с названием файла, профессии, параметрами сортировки, залоговками и количеством
        выводимых вакансии в табличке
    """
    def __init__(self):
        """Конструктор для инициализации объекта InputConnect"""
        self.params = InputConnect.get_params()

    @staticmethod
    def get_params():
        """Статический метод для ввода данные о вакансии

        :return: Кортеж с названием файла, профессии, параметрами сортировки, залоговками и количеством
        выводимых вакансии в табличке
        """
        file_name = input("Введите название файла: ")
        filter_params = input("Введите параметр фильтрации: ")
        sort_param = input("Введите параметр сортировки: ")
        sort_order = input("Обратный порядок сортировки (Да / Нет): ")
        numbers = input("Введите диапазон вывода: ").split()
        headings = input("Введите требуемые столбцы: ").split(', ')
        InputConnect.check_params(filter_params, sort_param, sort_order)
        return file_name, filter_params, sort_param, sort_order, numbers, headings

    @staticmethod
    def check_params(params, sort_param, sort_order):
        """Валидация параметров вводимых пользователем, если один из параметров не валидный, то завершается
        выполнение программы
        :param params: Строка с параметрами фильтрации
        :param sort_param: Строка с параметрами сортировки
        :param sort_order: Строка с правилами сортировки
        :return: None
        """
        if not params.__contains__(':') and len(params) > 1:
            print("Формат ввода некорректен")
            exit(0)
        params = params.replace(',', '').split(': ')
        if not params[0] in dic_naming.values() and len(params) >= 2:
            print("Параметр поиска некорректен")
            exit(0)
        if len(sort_param) != 0 and not sort_param in dic_naming.values():
            print("Параметр сортировки некорректен")
            exit(0)
        if not sort_order in ["Нет", "Да", '']:
            print("Порядок сортировки задан некорректно")
            exit(0)

    @staticmethod
    def universal_parser_csv(self, data: DataSet):
        """Статический Метод, который сортирует и фильтрует список вакансий
        :param self: Объект класса InputConnect
        :param data: Объект класса DataSet
        :return: Форматировнный список вакансии
        """
        filter_params = self.params[1].replace(',', '').split(': ')
        sort_order = len(self.params[3]) != 0 and self.params[3] == "Да"
        data.vacancies_objects = InputConnect.filter_by_params(filter_params, data.vacancies_objects)
        data.vacancies_objects = InputConnect.sort_by_params(data.vacancies_objects, self.params[2], sort_order)
        return InputConnect.formatter(data.vacancies_objects)

    @staticmethod
    def filter_by_params(params, vacancies_objects):
        """Статический Метод для фильтрации списка вакансии по определенному параметру
        :param params: Параметр фильтрации
        :param vacancies_objects: Список вакансий
        :return: Отфильтраванный список вакансий
        """
        def get_field_by_name(name, vacancy):
            """Функция, которая возвращает поле класса Vacancy
            :param name: Названия поля
            :param vacancy: Объект класса Vacancy
            :return: Поле объекта класса Vacancy
            """
            if name == "Название":
                return vacancy.name
            if name == "Описание":
                return vacancy.description
            return vacancy.employer_name
        def get_field_by_param(param, vacancy):
            """Функция, которая возвращает поле класса Vacancy
            :param param: Названия поля
            :param vacancy: Объект класса Vacancy
            :return: Поле объекта класса Vacancy
            """
            if param == "Премиум-вакансия":
                return vacancy.premium
            if param == "Опыт работы":
                return work_experience[vacancy.experience_id]
            return vacancy.area_name
        def filter_by_skills(skills, vacancy):
            """Функция для сравнения требуемых и существующих скиллов
            :param skills: Список навыков, требуемые для фильтрации
            :param vacancy: Объект класса Vacancy
            :return: Возвращает True, если при объеденении требуемый скиллов с существующими
            длина списка осталась прежней, иначе False
            """
            skills_set = set(vacancy.key_skills)
            return len(skills_set.union(set(skills))) == len(skills_set)
        filtered_vacancies = []
        if len(params) == 1:
            return vacancies_objects
        if params[0] == "Оклад":
            filtered_vacancies = list(
                filter(lambda x: float(x.salary.salary_from) <= float(params[1]) <= float(x.salary.salary_to), vacancies_objects))
        elif params[0] == "Навыки":
            skills = params[1].split()
            filtered_vacancies = list(filter(lambda x: filter_by_skills(skills, x), vacancies_objects))
        elif params[0] == "Идентификатор валюты оклада":
            filtered_vacancies = list(filter(lambda x: currencies[x.salary.salary_currency] == (params[1]), vacancies_objects))
        elif params[0] in ["Название", "Описание", "Компания"]:
            filtered_vacancies = list(filter(lambda x: get_field_by_name(params[0], x) == params[1], vacancies_objects))
        elif params[0] == "Дата публикации вакансии":
            filtered_vacancies = list(filter(
                lambda x: datetime.strptime(x.published_at, "%Y-%m-%dT%H:%M:%S%z").strftime("%d.%m.%Y").__contains__(
                    params[1]), vacancies_objects))
        else:
            filtered_vacancies = list(
                filter(lambda x: get_field_by_param(params[0], x).__contains__(params[1]), vacancies_objects))
        if len(filtered_vacancies) == 0:
            print("Ничего не найдено")
            exit(0)
        else:
            return filtered_vacancies

    @staticmethod
    def sort_by_params(vacancies_objects, sort_param, sort_order):
        """Статический метод для сортировки вакансии по определенным критериям
        :param vacancies_objects: Список вакансии для сортировки
        :param sort_param: Строка с параметром сортировки
        :param sort_order: Критерий сортировки
        :return: Отсортированный список вакансий
        """
        def get_currency_to_rub(vacancy):
            """Вычисляет среднюю з/п вилки и переподит в рубли, при помощи словаря - currency_to_rub
            :param vacancy: Объект класса Vacancy
            :return: Средняя з/п вилки
            """
            course = currency_to_rub[vacancy.salary.salary_currency]
            return int((float(vacancy.salary.salary_from) * course + float(vacancy.salary.salary_to) * course) / 2)
        def get_field_by_name(name, vacancy):
            """Функция, которая возвращает поле класса Vacancy
            :param name: Названия поля
            :param vacancy: Объект класса Vacancy
            :return: Поле объекта класса Vacancy
            """
            if name == "Название":
                return vacancy.name
            if name == "Описание":
                return vacancy.description
            if name == "Компания":
                return vacancy.employer_name
            if name == "Премиум-вакансия":
                return vacancy.premium
            if name == "Идентификатор валюты оклада":
                return vacancy.salary.salary_currency
            return vacancy.area_name
        if len(sort_param) == 0:
            return vacancies_objects
        if sort_param == "Оклад":
            return sorted(vacancies_objects, key=lambda x: get_currency_to_rub(x), reverse=sort_order)
        elif sort_param == "Навыки":
            return sorted(vacancies_objects, key=lambda x: len(x.key_skills), reverse=sort_order)
        elif sort_param == "Дата публикации вакансии":
            return sorted(vacancies_objects, key=lambda x: datetime.strptime(x.published_at, "%Y-%m-%dT%H:%M:%S%z"),
                          reverse=sort_order)
        elif sort_param == "Опыт работы":
            return sorted(vacancies_objects, key=lambda x: work_experience_id[work_experience[x.experience_id]],
                          reverse=sort_order)
        else:
            return sorted(vacancies_objects, key=lambda x: get_field_by_name(sort_param, x), reverse=sort_order)

    @staticmethod
    def formatter(vacancies_objects):
        """Статический метод для форматирование списка вакансий
        :param vacancies_objects: Список вакансий
        :return: Отформатированный список вакансий
        """
        def get_message(item):
            """Функция, которая возвращает сообщение об вычете налогов
            :param item: Строка с параметром налога
            :return: Возвращает строку с сообщением об вычете налогов
            """
            if item.lower() == "true" or item.lower() == "да":
                return "Без вычета налогов"
            return "С вычетом налогов"
        def get_salary(row):
            """Функция для формирования строки с данными об з/п
            :param row: Объект класса Vacancy
            :return: Сообщение с данными об з/п
            """
            message = get_message(row.salary.salary_gross)
            sum_min = InputConnect.get_valid_numbers(row.salary.salary_from)
            sum_max = InputConnect.get_valid_numbers(row.salary.salary_to)
            return f"{sum_min[0]}{sum_min[1]} - " \
                    f"{sum_max[0]}{sum_max[1]} " \
                    f"({currencies[row.salary.salary_currency]}) ({message})"

        for vacancy in vacancies_objects:
            vacancy.experience_id = work_experience[vacancy.experience_id]
            vacancy.salary.salary_info = get_salary(vacancy)
            vacancy.published_at = datetime.strptime(vacancy.published_at, "%Y-%m-%dT%H:%M:%S%z").strftime("%d.%m.%Y")
        return vacancies_objects

    @staticmethod
    def get_valid_numbers(str_num):
        """Возвращает корректную строку с з/п
        :param str_num: Строка с з/п
        :return: Возвращает строку в корректном виде
        """
        num = int(str_num.partition('.')[0])
        first_num = str(num // 1000)
        if first_num != '0':
            first_num = first_num + " "
        else:
            first_num = ''
        second_num = str(num % 1000)
        if len(second_num) == 1:
            second_num = second_num * 3
        elif len(second_num) == 2:
            second_num = '0' + second_num
        return first_num, second_num

    @staticmethod
    def print_table(self, dataset: DataSet):
        """Метод для печати таблицы в консоль при помощи модуля prettytable

        :param self: Объект класса InputConnect
        :param dataset: Объект класса Dataset
        :return: None
        """
        def get_table(vacancies):
            """Функция, которя создает таблицу при помощи класса PrettyTable и устанавливает
            значения в строки таблицы
            :param vacancies: Список вакансий
            :return: Возвращает объект класса PrettyTable
            """
            table = PrettyTable(hrules=prettytable.ALL, align='l')
            table.field_names = ["Название", "Описание", "Навыки", "Опыт работы", "Премиум-вакансия",
                                 "Компания", "Оклад", "Название региона", "Дата публикации вакансии"]
            for vacancy in vacancies:
                row = get_correct_row(vacancy)
                table.add_row(row)
            table.add_autoindex("№")
            table.max_width = 20
            return table

        def get_correct_row(vacancy):
            """Функция для формирования строки таблицы из объекта класса Vacancy

            :param vacancy: Объект класса Vacancy
            :return: Возвращает отформатированную строку таблицы
            """
            def trim_line(line):
                """Срезает строку, если её длина больше или равно 100

                :param line: Строка для среза
                :return: Возвращает срезанную строку с символами '...' среза в конце, если её длина больше или равно 100
                """
                if len(line) >= 100:
                    return line[:100] + "..."
                return line

            result = [trim_line(vacancy.name), trim_line(vacancy.description), trim_line("\n".join(vacancy.key_skills)),
                      vacancy.experience_id, vacancy.premium, vacancy.employer_name, vacancy.salary.salary_info,
                      vacancy.area_name, vacancy.published_at]
            return result

        def get_correct_headings(headings, table):
            """Функция, которая возвращает заголовки таблицы

            :param headings: Список строк с заголовками
            :param table: Объект класса PrettyTable
            :return: Возвращает список заголовков
            """
            if len(headings) == 1:
                return table.field_names
            headings.append('№')
            return headings

        vacancies_objects = InputConnect.universal_parser_csv(self, dataset)
        table = get_table(vacancies_objects)
        headings = get_correct_headings(self.params[5], table)
        if len(self.params[4]) == 2:
            print(table.get_string(start=int(self.params[4][0]) - 1, end=int(self.params[4][1]) - 1, fields=headings))
        elif len(self.params[4]) == 1:
            print(table.get_string(start=int(self.params[4][0]) - 1, fields=headings))
        else:
            print(table.get_string(fields=headings))


def print_vacancies():
    """Метод для формирования таблиц с вакансиями
    :return:None
    """
    inputParam = InputConnect()
    dataSet = DataSet(inputParam.params[0]).get_dataset()
    InputConnect.print_table(inputParam, dataSet)
