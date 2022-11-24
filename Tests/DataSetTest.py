from unittest import TestCase, main
from Task2_1_3 import DataSet


class DataSetTest(TestCase):
    def test_dataSet_type_and_fields(self):
        self.assertEqual(type(DataSet("vacancies.csv")).__name__, "DataSet")

    def test_dataSet_fields(self):
        self.assertEqual(DataSet("vacancies.csv").file_name, "vacancies.csv")
        self.assertEqual(len(DataSet("vacancies.csv").vacancies_objects), 0)

    def test_csv_reader(self):
        row, column = DataSet("../vacancies.csv").csv_reader()
        self.assertEqual(len(row), 12)
        self.assertEqual(len(column), 91)

    def test_csv_filter(self):
        dataset = DataSet("../vacancies.csv")
        row, column = dataset.csv_reader()
        dict_list = dataset.csv_filter(row, column)
        self.assertEqual(len(dict_list), 91)

    def text_csv_filter_second_item(self):
        dataset = DataSet("../vacancies.csv")
        row, column = dataset.csv_reader()
        dict_list = dataset.csv_filter(row, column)
        self.assertEqual(dict_list[1]["name"], "Senior Python Developer (Crypto)")
        self.assertEqual(dict_list[1]["salary_from"], "4500")
        self.assertEqual(dict_list[1]["salary_to"], "5500")
        self.assertEqual(dict_list[1]["salary_currency"], "EUR")

    def test_remove_tags_and_spaces(self):
        dataSet = DataSet("../vacancies.csv")
        text = "<p><strong>Группа компаний «МИАКОМ»</strong><p>     <p>   Основана    в Санкт-Петербурге<p>"
        lines = dataSet.remove_tags_and_spaces(text.split('\n'))
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0], "Группа компаний «МИАКОМ» Основана в Санкт-Петербурге")


if __name__ == '__main__':
    main()