from unittest import TestCase, main
from Task2_1_3 import InputConnect, DataSet, Vacancy


class InputConnectTest(TestCase):
    def test_get_vacancies_count_by_name_with_correct_name(self):
        dataset = DataSet("../vacancies.csv").get_dataset()
        vacancies_count = InputConnect.get_vacancies_count_by_name(dataset, "Программист")
        self.assertEqual(len(vacancies_count), 1)
        self.assertEqual(vacancies_count[2022], 6)

    def test_get_vacancies_count_by_name_without_correct_name(self):
        dataset = DataSet("../vacancies.csv").get_dataset()
        vacancies_count = InputConnect.get_vacancies_count_by_name(dataset, "None")
        self.assertEqual(len(vacancies_count), 1)
        self.assertEqual(vacancies_count[2022], 91)

    def test_get_vacancies_count_by_name_with_no_existent_name(self):
        dataset = DataSet("../vacancies.csv").get_dataset()
        vacancies_count = InputConnect.get_vacancies_count_by_name(dataset, "123")
        self.assertEqual(len(vacancies_count), 1)
        self.assertEqual(vacancies_count[2022], 0)

    def test_get_salary_by_name_with_correct_name(self):
        dataset = DataSet("../vacancies.csv").get_dataset()
        dataset.vacancies_count_by_profession_name = InputConnect.get_vacancies_count_by_name(dataset, "Программист")
        salary_by_name = InputConnect.get_salary_by_name(dataset, "Программист")
        self.assertEqual(len(salary_by_name), 1)
        self.assertEqual(salary_by_name[2022], 101666)

    def test_get_salary_by_name_without_correct_name(self):
        dataset = DataSet("../vacancies.csv").get_dataset()
        dataset.vacancies_count_by_year = InputConnect.get_vacancies_count_by_name(dataset, "None")
        salary_by_name = InputConnect.get_salary_by_name(dataset, "None")
        self.assertEqual(len(salary_by_name), 1)
        self.assertEqual(salary_by_name[2022], 94892)

    def test_get_salary_by_name_with_with_no_existent_name(self):
        dataset = DataSet("../vacancies.csv").get_dataset()
        dataset.vacancies_count_by_year = InputConnect.get_vacancies_count_by_name(dataset, "123")
        with self.assertRaises(ZeroDivisionError) as e:
            salary_by_name = InputConnect.get_salary_by_name(dataset, "None")
        self.assertEqual("Словарь 'vacancies_count_by_year' или 'vacancies_count_by_profession_name'содержит"
                         " в качестве значение 0", e.exception.args[0])

    def test_get_vacancy_rate_by_city(self):
        dataset = DataSet("../vacancies.csv").get_dataset()
        vacancy_rate = InputConnect.get_vacancy_rate_by_city(dataset)
        self.assertEqual(len(vacancy_rate), 36)
        self.assertEqual(vacancy_rate["Москва"], 24)
        self.assertEqual(vacancy_rate["Санкт-Петербург"], 12)
        self.assertEqual(vacancy_rate["Сочи"], 1)
        self.assertEqual(vacancy_rate["Свердловский"], 1)

    def test_get_salary_by_city(self):
        dataset = DataSet("../vacancies.csv").get_dataset()
        dataset.vacancy_rate_by_city = InputConnect.get_vacancy_rate_by_city(dataset)
        salary_by_city = InputConnect.get_salary_by_city(dataset)
        self.assertEqual(len(salary_by_city), 36)
        self.assertEqual(salary_by_city["Москва"], 157438)
        self.assertEqual(salary_by_city["Екатеринбург"], 103333)
        self.assertEqual(salary_by_city["Санкт-Петербург"], 116875)
        self.assertEqual(salary_by_city["Хабаровск"], 100000)

    def test_get_salary_by_city_sorted(self):
        dataset = DataSet("../vacancies.csv").get_dataset()
        dataset.vacancy_rate_by_city = InputConnect.get_vacancy_rate_by_city(dataset)
        salary_by_city = InputConnect.get_salary_by_city(dataset)
        self.assertEqual(dict(sorted(salary_by_city.items(), key=lambda item: item[1], reverse=True)), salary_by_city)

    def test_set_value_by_name_empty_dict(self):
        test_dict = dict()
        InputConnect.set_value_by_name(test_dict, "test_name")
        self.assertEqual(test_dict["test_name"], 1)
        self.assertEqual(len(test_dict), 1)

    def test_set_value_by_name_dict_with_one_key(self):
        test_dict = {"test_name": 41}
        InputConnect.set_value_by_name(test_dict, "test_name")
        self.assertEqual(test_dict["test_name"], 42)

    def test_set_value_by_name_dict_with_key(self):
        test_dict = {"test_name": 42}
        InputConnect.set_value_by_name(test_dict, "test_name2")
        self.assertEqual(test_dict["test_name"], 42)
        self.assertEqual(test_dict["test_name2"], 1)
        self.assertEqual(len(test_dict), 2)

    def test_get_currency_to_rub_from_EUR(self):
        vacancy = Vacancy(args=["Senior Python Developer", "4500", "5500", "EUR", "Санкт-Петербург", "2022"])
        result = InputConnect.get_currency_to_rub(vacancy)
        self.assertEqual(result, 299500)

    def test_get_currency_to_rub_from_RUR(self):
        vacancy = Vacancy(args=["Junior Python Developer", "45000", "55000", "RUR", "Санкт-Петербург", "2022"])
        result = InputConnect.get_currency_to_rub(vacancy)
        self.assertEqual(result, 50000)

    def test_get_currency_to_rub_from_USD(self):
        vacancy = Vacancy(args=["Middle Python Developer", "1000", "2500", "USD", "Санкт-Петербург", "2022"])
        result = InputConnect.get_currency_to_rub(vacancy)
        self.assertEqual(result, 106155)



if __name__ == '__main__':
    main()