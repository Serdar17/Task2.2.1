from _datetime import datetime
import pandas as pd


class Chunk:
    """
    Класс для разбиение csv файла на чанки по годам
    Attributes:
        file_name (str): Название вакансии
    """
    def __init__(self, file_name):
        """Конструктор для инициализации объекта Chunk
        :param file_name: Название файла
        """
        self.file_name = file_name

    def create_chunks(self):
        """
        Читает и разделяет данные по годам в отдельные csv файлы
        :return: None
        """
        pd.set_option("expand_frame_repr", False)
        df = pd.read_csv(self.file_name)
        df["years"] = df["published_at"].apply(lambda x: datetime(int(x[:4]), int(x[5:7]), int(x[8:10])).year)
        years = df["years"].unique()
        for year in years:
            data = df[df["years"] == year]
            data.iloc[:, :6].to_csv(rf"vacancies/vacancies_by_{year}_year.csv", index=False)


name = input("Введите название файла для создания чанков: ")
chunk = Chunk(name)
chunk.create_chunks()