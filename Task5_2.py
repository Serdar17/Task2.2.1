import csv
from _datetime import datetime
import re
import prettytable
from prettytable import PrettyTable

dic_naming = {"name": "Название", "description": "Описание", "key_skills": "Навыки", "experience_id": "Опыт работы",
              "premium": "Премиум-вакансия", "employer_name": "Компания", "salary_to": "Оклад",
              "area_name": "Название региона",
              "published_at": "Дата публикации вакансии", "True": "Да", "False": "Нет", "FALSE": "FALSE",
              "TRUE": "TRUE",
              "value": "Идентификатор валюты оклада"}
work_experience = {"noExperience": "Нет опыта", "between1And3": "От 1 года до 3 лет",
                   "between3And6": "От 3 до 6 лет", "moreThan6": "Более 6 лет"}
work_experience_id = {"Нет опыта": 1, "От 1 года до 3 лет": 2, "От 3 до 6 лет": 3, "Более 6 лет": 4}
currencies = {"AZN": "Манаты", "BYR": "Белорусские рубли", "EUR": "Евро", "GEL": "Грузинский лари",
              "KGS": "Киргизский сом",
              "KZT": "Тенге", "RUR": "Рубли", "UAH": "Гривны", "USD": "Доллары", "UZS": "Узбекский сум"}

currency_to_rub = {
    "AZN": 35.68, "BYR": 23.91, "EUR": 59.90, "GEL": 21.74, "KGS": 0.76,
    "KZT": 0.13, "RUR": 1, "UAH": 1.64, "USD": 60.66, "UZS": 0.0055}


class DataSet:
    def __init__(self, file_name):
        self.file_name = file_name
        self.vacancies_objects = list()

    @staticmethod
    def get_dataset(file_name):
        data = DataSet.csv_reader(file_name)
        dict_list = DataSet.csv_filter(data[0], data[1])
        dataset = DataSet(file_name)
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
            dataset.vacancies_objects.append(vacancy)
        return dataset

    @staticmethod
    def remove_tags_and_spaces(items):
        for i in range(len(items)):
            items[i] = " ".join(re.sub(r"\<[^>]*\>", "", items[i]).split())
        return items

    @staticmethod
    def csv_reader(file_name):
        with open(file_name, "r", encoding="utf-8-sig", newline="") as file:
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

    @staticmethod
    def csv_filter(columns, rows):
        dic_list = list()
        for row in rows:
            dic_result = dict()
            for i in range(len(row)):
                items = DataSet.remove_tags_and_spaces(row[i].split('\n'))
                dic_result[columns[i]] = items[0] if len(items) == 1 else "; ".join(items)
            dic_result["premium"] = dic_naming[dic_result["premium"]]
            dic_result["salary_from"] = [dic_result["salary_from"], dic_result.pop("salary_to"),
                                         dic_result.pop("salary_gross"), dic_result.pop("salary_currency")]
            dic_list.append(dic_result)
        return dic_list


class Vacancy:
    def __init__(self, args):
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
    def __init__(self, args):
        self.salary_from = args[0]
        self.salary_to = args[1]
        self.salary_gross = args[2]
        self.salary_currency = args[3]


class InputConnect:
    def __init__(self):
        self.params = InputConnect.get_params()

    @staticmethod
    def get_params():
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
        filter_params = self.params[1].replace(',', '').split(': ')
        sort_order = len(self.params[3]) != 0 and self.params[3] == "Да"
        data.vacancies_objects = InputConnect.filter_by_params(filter_params, data.vacancies_objects)
        data.vacancies_objects = InputConnect.sort_by_params(data.vacancies_objects, self.params[2], sort_order)
        return InputConnect.formatter(data.vacancies_objects)

    @staticmethod
    def filter_by_params(params, vacancies_objects):
        def get_field_by_name(name, vacancy):
            if name == "Название":
                return vacancy.name
            if name == "Описание":
                return vacancy.description
            return vacancy.employer_name
        def get_field_by_param(param, vacancy):
            if param == "Премиум-вакансия":
                return vacancy.premium
            if param == "Опыт работы":
                return work_experience[vacancy.experience_id]
            return vacancy.area_name
        def filter_by_skills(skills, vacancy):
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
        def get_currency_to_rub(vacancy):
            course = currency_to_rub[vacancy.salary.salary_currency]
            return int((float(vacancy.salary.salary_from) * course + float(vacancy.salary.salary_to) * course) / 2)
        def get_field_by_name(name, vacancy):
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
        def get_message(item):
            if item.lower() == "true" or item.lower() == "да":
                return "Без вычета налогов"
            return "С вычетом налогов"
        def get_experience(row): return work_experience[row.experience_id]
        def get_date(row): return datetime.strptime(row.published_at, "%Y-%m-%dT%H:%M:%S%z").strftime("%d.%m.%Y")
        def get_salary(row):
            message = get_message(row.salary.salary_gross)
            sum_min = InputConnect.get_valid_numbers(row.salary.salary_from)
            sum_max = InputConnect.get_valid_numbers(row.salary.salary_to)
            return f"{sum_min[0]}{sum_min[1]} - " \
                    f"{sum_max[0]}{sum_max[1]} " \
                    f"({currencies[row.salary.salary_currency]}) ({message})"

        for vacancy in vacancies_objects:
            vacancy.experience_id = get_experience(vacancy)
            vacancy.salary.salary_info = get_salary(vacancy)
            vacancy.published_at = get_date(vacancy)
        return vacancies_objects

    @staticmethod
    def get_valid_numbers(str_num):
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
    def print_table(self, dataset):
        def get_table(vacancies):
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
            def trim_line(line):
                if len(line) >= 100:
                    return line[:100] + "..."
                return line

            result = [trim_line(vacancy.name), trim_line(vacancy.description), trim_line("\n".join(vacancy.key_skills)),
                      vacancy.experience_id, vacancy.premium, vacancy.employer_name, vacancy.salary.salary_info,
                      vacancy.area_name, vacancy.published_at]
            return result

        def get_correct_headings(headings, table):
            if len(headings) == 1:
                return table.field_names
            headings.append('№')
            return headings

        vacancies_objects = InputConnect.universal_parser_csv(self, dataset)
        table = get_table(vacancies_objects)
        headings = get_correct_headings(self.params[5], table)
        if len(self.params[4]) == 2:
            time = datetime.now()
            print(table.get_string(start=int(self.params[4][0]) - 1, end=int(self.params[4][1]) - 1, fields=headings))
        elif len(self.params[4]) == 1:
            print(table.get_string(start=int(self.params[4][0]) - 1, fields=headings))
        else:
            print(table.get_string(fields=headings))


def print_vacancies():
    inputParam = InputConnect()
    dataSet = DataSet.get_dataset(inputParam.params[0])
    InputConnect.print_table(inputParam, dataSet)
