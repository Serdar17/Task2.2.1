import csv


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

    def read_csv(self):
        """
        Метод для чтения csv файла
        :return:
            columns (list): Список заголовков csv файла
            rows (list): Список оставшихся строк
        """
        with open(self.file_name, "r", encoding="utf-8-sig", newline="") as file:
            data = [x for x in csv.reader(file)]
        columns = data[0]
        rows = [x for x in data[1:] if len(x) == len(columns) and not x.__contains__("")]
        return columns, rows

    def create_chunks(self):
        """
        Разделяет данные по годам в отдельные csv файлы
        :return: None
        """
        columns, rows = self.read_csv()
        years = self.get_years(rows)
        for year in years:
            with open(rf'vacancies/vacancies_by_{year}_year.csv', mode="w", encoding='utf-8') as f:
                file_writer = csv.writer(f, delimiter=",", lineterminator="\r")
                file_writer.writerow(columns)
                for row in rows:
                    if row[5][:4] == year:
                        file_writer.writerow(row)

    def get_years(self, rows):
        """
        Метод для формирования списока годов из всех записей csv файла
        :param rows: Список строк csv файла
        :return:
            list_years (list): Список годов csv файла
        """
        list_years = list()
        for row in rows:
            if not list_years.__contains__(row[5][:4]):
                list_years.append(row[5][:4])
        return list_years


name = "vacancies_by_year.csv"
chunk = Chunk(name)
chunk.create_chunks()


