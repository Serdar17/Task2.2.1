import sqlite3
import pandas as pd


def converter_from_db(x, cursor):
    """
    Метод для конвертации валюты, курс валюты берется из БД
    :param x: Строка для конвертации
    :param cursor: Объект класса Cursor
    :return: Сконвертированную валюту в рубли
    """
    if pd.isnull(x):
        return x
    values = x.split()
    if values[1] in ["RUR", "AZN", "UZS", "KGS", "GEL"]:
        return values[0]
    cursor.execute(f"""SELECT date, {values[1]} FROM exchange_rates
    WHERE date = '{values[2]}'
    """)
    course = cursor.fetchone()
    return course[1] is not None if round(float(values[0]) * course[1]) else values[0]


def convert_table():
    """
    Скрипт для создания БД и конвертации валют файла vacancies_dif_currencies_orig.csv
    :return: None
    """
    try:
        sqlite_connection = sqlite3.connect('test.db')
        cursor = sqlite_connection.cursor()

        df = pd.read_csv("vacancies_dif_currencies_orig.csv")
        df.insert(1, "salary", None)
        df["salary"] = df[["salary_from", "salary_to"]].mean(axis=1)
        df["published_at"] = df["published_at"].apply(lambda d: d[:7])
        df["salary"] = df["salary"].astype(str) + " " + + df["salary_currency"] + " " + df["published_at"]
        df["salary"] = df["salary"].apply(lambda x: converter_from_db(x, cursor))
        df = df.drop(columns=['salary_from', 'salary_to', 'salary_currency'])
        df.to_sql('converted_vacancy', sqlite_connection, if_exists='replace', index=False)
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)

    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


if __name__ == '__main__':
    convert_table()