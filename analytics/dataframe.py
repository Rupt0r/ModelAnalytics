import pandas as pd

from check.checkparams import CheckParams
from logs.logger import logger


class DF:
    """
    Класс для взаимосвязи с pd.DataFrame.
    """

    def __init__(self):
        """
        Конструктор.
        """
        CheckParams().csv(filename='flats.csv')
        self.df = pd.read_csv('flats.csv')
        self.X = None
        self.y = None
        self.upgrade_data()
        self.set_Xy_dataset()

    def upgrade_data(self):
        """
        Данный метод обрабатывает DataFrame таким образом, чтобы мы могли с ним без конфликтно работать.

        :return: None
        """
        logger.info('Upgrade data in DataFrame')
        self.df = self.df.dropna()
        for column in ['dist', 'kitsp']:
            self.df[column] = self.df[column].apply(lambda x: float(str(x).replace(',', '.')))

    def set_Xy_dataset(self):
        """
        Метод, который из данных DataFrame делает нам список 'X' и 'y'.

        :return: None
        """
        self.X = self.df.loc[:, 'totsp':'code']
        self.y = self.df['price']

    def show(self):
        """
        Метод, который показывает в Консоли весь DataFrame.

        :return: None
        """
        print(self.df)

    @staticmethod
    def new_df(filling=None) -> pd.DataFrame:
        """
        Получив начинку (данные) для новой базы, метод создает новый DataFrame по этими данными.

        :return: pd.DataFrame
        """
        logger.info('Create a new DataFrame.')
        if filling is None:
            filling = {}
        CheckParams().filling(filling=filling)
        return pd.DataFrame(filling)
