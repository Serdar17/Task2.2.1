import sqlite3
import pandas as pd


def print_statistics_by_query_from_db(connect, sql_query):
    """
    Функция для печати в консоль датафрейма из БД по sql запросу
    :param sql_query: Sql запрос
    :param connect: Объект для покдлючения к БД
    :return: None
    """
    df = pd.read_sql(sql_query, connect)
    print(df)

def create_table():
    """
    Скрипт для создания БД и записи из файла dataframe.csv со всеми курсами валют с 2003-2022 год
    :return: None
    """
    try:
        prof_name = input("Введите название профессии: ")
        sqlite_connection = sqlite3.connect('test.db')
        cursor = sqlite_connection.cursor()

        # Sql запрос для подсчета динамики уровня зарплаты по годам
        salary_by_year_query = (f"""SELECT SUBSTRING(published_at, 1, 4) AS 'Год', ROUND(AVG(salary), 2) AS 'Средняя з/п' 
        FROM converted_vacancy
        GROUP BY SUBSTRING(published_at, 1, 4)
        """)

        # Sql запрос для подсчета количества вакансии по годам
        salary_count_query = (f"""SELECT SUBSTRING(published_at, 1, 4) AS 'Год', COUNT(salary) AS 'Количество вакансий' 
        FROM converted_vacancy
        GROUP BY SUBSTRING(published_at, 1, 4)
        """)

        # Sql запрос для подсчета динамики уровня зарплат по выбранной профессии
        salary_by_name_query = (f"""SELECT SUBSTRING(published_at, 1, 4) AS 'Год', ROUND(AVG(salary), 2) 
        AS 'Средняя з/п - {prof_name}'
        FROM converted_vacancy
        WHERE name LIKE '%{prof_name}%'
        GROUP BY SUBSTRING(published_at, 1, 4)
        """)

        # Sql запрос для подсчета количества вакансии по выбранной профессии
        salary_count_by_name_query = (f"""SELECT SUBSTRING(published_at, 1, 4) AS 'Год', COUNT(salary) 
        AS 'Количетсво вакансий - {prof_name}'
        FROM converted_vacancy
        WHERE name LIKE '%{prof_name}%'
        GROUP BY SUBSTRING(published_at, 1, 4)
        """)

        # Sql запрос для подсчета уровня зарплат по городам
        salary_by_city_query = (f"""SELECT area_name AS 'Город', ROUND(AVG(salary), 2) AS 'Уровень зарплат по городам'
        FROM converted_vacancy
        GROUP BY area_name
        HAVING COUNT(*) >= (SELECT COUNT(*) FROM converted_vacancy) / 100
        ORDER BY ROUND(AVG(salary), 2) DESC 
        LIMIT 10
        """)

        # Sql запрос для подсчета доли вакансии по городам
        vacancy_count_by_city_query = (f"""SELECT area_name AS 'Город', 
        100 * COUNT(*) / (select COUNT(*) from converted_vacancy) AS 'Доля вакансий' FROM converted_vacancy
        GROUP BY area_name
        HAVING COUNT(*) >= (SELECT COUNT(*) FROM converted_vacancy) / 100
        ORDER BY COUNT(*) DESC 
        LIMIT 10
        """)

        print_statistics_by_query_from_db(sqlite_connection, salary_by_year_query)
        print_statistics_by_query_from_db(sqlite_connection, salary_count_query)
        print_statistics_by_query_from_db(sqlite_connection, salary_by_name_query)
        print_statistics_by_query_from_db(sqlite_connection, salary_count_by_name_query)
        print_statistics_by_query_from_db(sqlite_connection, salary_by_city_query)
        print_statistics_by_query_from_db(sqlite_connection, vacancy_count_by_city_query)

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)

    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


if __name__ == '__main__':
    create_table()