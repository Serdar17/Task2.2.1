from unittest import TestCase, main
from Task2_1_3 import Vacancy


class VacancyTest(TestCase):

    def test_vacancy_type(self):
        self.assertEqual(type(
            Vacancy(args=["Senior Python Developer", "4500", "5500", "EUR", "Санкт-Петербург", "2022"])).__name__,
                         "Vacancy")

    def test_vacancy_name_field(self):
        self.assertEqual(Vacancy(args=["Senior Python", "4500", "5500", "EUR", "Санкт-Петербург", "2022"]).name,
                         "Senior Python")

    def test_vacancy_salary_from_field(self):
        self.assertEqual(Vacancy(args=["Senior Python", "4500", "5500", "EUR", "Санкт-Петербург", "2022"]).salary_from,
                         4500)

    def test_vacancy_salary_to_field(self):
        self.assertEqual(Vacancy(args=["Senior Python", "4500", "5500", "EUR", "Санкт-Петербург", "2022"]).salary_to,
                         5500)

    def test_vacancy_salary_currency_field(self):
        self.assertEqual(Vacancy(args=["Python", "4500", "5500", "EUR", "Санкт-Петербург", "2022"]).salary_currency,
                         "EUR")

    def test_vacancy_area_name_field(self):
        self.assertEqual(Vacancy(args=["Python", "4500", "5500", "EUR", "Санкт-Петербург", "2022"]).area_name,
                         "Санкт-Петербург")

    def test_vacancy_published_at_field(self):
        self.assertEqual(Vacancy(args=["Python", "4500", "5500", "EUR", "Санкт-Петербург", "2022"]).published_at,
                         "2022")


if __name__ == '__main__':
    main()