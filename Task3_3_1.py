import pandas as pd
from _datetime import datetime
from xml.etree import ElementTree
import numpy as np
import grequests
from Chunk import create_chunk


class CurrencyFrame:
    """
    Класс для создания DataFrame с курсами валют
    Attributes:
        file_name (str): Название файла с вакансиями
    """
    def __init__(self):
        """
        Конструктор для инициализации объекта CurrencyFrame
        """
        self.file_name = "vacancies_dif_currencies.csv"
        create_chunk(self.file_name)

    def filter_csv(self):
        """
        Метод для фильтрации DataFrame
        :return: Возвращает headers - список требуемых валют, data_dict - словарь для сбора данных из запросов,
         dates_lst - список с датами
        """
        df = pd.read_csv(self.file_name)
        print(df["salary_currency"].value_counts())
        df["count"] = df.groupby("salary_currency")["salary_currency"].transform("count")
        df = df[(df["count"] > 5000)]
        df["published_at"] = df["published_at"].apply(lambda x: datetime(int(x[:4]), int(x[5:7]), 1))
        headers = df["salary_currency"].unique()
        min_date = df["published_at"].min()
        max_date = df["published_at"].max()

        headers = np.delete(headers, 1)
        data_dict = {item: [] for item in np.insert(headers, 0, "date")}
        dates_lst = pd.date_range(min_date.strftime("%Y-%m"), max_date.strftime("%Y-%m"), freq="MS")
        return headers, data_dict, dates_lst

    def get_urls(self, dates_lst, data_dict):
        """
        Создает список url для GET запросов (http://www.cbr.ru/scripts/XML_daily.asp)
        :param dates_lst: Список с датами
        :param data_dict: Словать с данными о запросе
        :return: Список url
        """
        sites = []
        for date in dates_lst:
            t = pd.to_datetime(str(date))
            timestring = t.strftime('%d/%m/%Y')
            data_dict["date"].append(t.strftime('%Y-%m'))
            sites.append(rf"http://www.cbr.ru/scripts/XML_daily.asp?date_req={timestring}")
        return sites

    def create_frame(self):
        """
        Создает dataframe с расширением csv с информацией о валютах за определенный период
        :return: None
        """
        headers, data_dict, dates_lst = self.filter_csv()
        sites = self.get_urls(dates_lst, data_dict)
        response = (grequests.get(url) for url in sites)
        for res in grequests.map(response):
            data = {}
            root = ElementTree.fromstring(res.content)
            for element in root.iter('Valute'):
                args = []
                for child in element:
                    args.append(child.text)
                if headers.__contains__(args[1]):
                    data[args[1]] = round(float(args[4].replace(',', '.')) / int(args[2]), 6)
            for key in headers:
                if data.__contains__(key):
                    data_dict[key].append(data[key])
                else:
                    data_dict[key].append(None)

        df = pd.DataFrame(data_dict)
        df.to_csv("dataframe.csv", index=False)


if __name__ == '__main__':
    frame = CurrencyFrame()
    frame.create_frame()