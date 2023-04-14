import pandas as pd

from check.Parsing.parsing import ActivationFunctions, LossesFunctions, Optimizers


class CheckParams:
    """
    Класс для отлови неправильных переданных значений. Так же он нужен для тестов.
    """

    def __init__(self):
        """
        Конструктор.

        Здесь инициализируются классы парсингов.
        """
        self.losses = LossesFunctions()
        self.activations = ActivationFunctions()
        self.optimizers = Optimizers()

    @staticmethod
    def csv(*, filename: str):
        """
        Метод проверяет, есть ли в {filename} расширение, и есть ли {filename} в проекте.

        :param filename: str: имя файла.
        :return: None
        """
        if not (filename[-4:] == '.csv'):
            raise RuntimeError('The file must have the extension ".csv"')

        try:
            pd.read_csv(filename)
        except FileNotFoundError:
            raise FileNotFoundError(f'There should be a "{filename}" file in project')

    @staticmethod
    def filling(*, filling):
        """
        Метод проверяет, является ли {filling} словарем.

        :param filling: any: начинка для DataFrame.
        :return: None
        """
        if type(filling) != dict:
            raise ValueError('The "filling" variable type must be a dict')

    @staticmethod
    def int_param(value, max_value: int = 1):
        """
        Метод проверяет, является ли {value} целым числом, и входит ли число в диапазон от 0 до {max_value}.

        :param value: int: проверяемое число.
        :param max_value: int | float: Максимальное значение диапазона.
        :return:
        """
        try:
            int(value)
        except ValueError:
            raise ValueError(f'The passed {value=} must be int')

        if not (0 <= int(value) <= max_value):
            raise RuntimeError(f'{value} not included in the range from 0 to {max_value} not inclusive')

    @staticmethod
    def param(data, value_error, array, url):
        """
        Метод проверяет, является ли {data} строкой или объектом класса и есть ли {data} в списке доступных "значений".

        :param data: str | object: Переданное значение на проверку.
        :param value_error: str: ошибка типа {data}.
        :param array: list: список "доступных" значений.
        :param url: str: ссылка на документацию по конкретной проблеме.
        :return: None
        """
        runtime_error = f'Check your the {value_error} in {url}'
        value_error = f'The {value_error} must be a str or class'
        if (type(data) != str) and ('object' not in str(data)):
            raise ValueError(value_error)
        for item in array:
            if item in str(data):
                break
        else:
            raise RuntimeError(runtime_error)

    def uvf(self, data, _object):  # Universal verification function
        """
        Универсальная форма заполнения каждого объекта для проверки.

        :param data: str | object: Переданное значение на проверку.
        :param _object: LossesFunctions | ActivationFunctions | Optimizers: Объект, с которым будут сравнивать {data}.
        :return: None
        """
        value_error = _object.value_error
        array = _object.array
        url = _object.url
        self.param(data, value_error, array, url)

    def check_data(self, data, max_value):
        """
        Метод проверяет, является ли data кортеджом (tuple), и проверяет по отдельности каждое значение внутри себя.

        :param data: Переданный кортедж на проверку.
        :param max_value: максимальное значение числа для {data[0]}
        :return: None
        """
        if not (type(data) == tuple):
            raise ValueError('The passed value must be tuple. Example: (int, str)')

        self.int_param(data[0], max_value)
        self.uvf(data[1], self.activations)

    def model_generator(self, *args):
        """
        Метод проверяет, все ли переданные параметры введены верно.

        :param args: list: список определённых параметров для проверки
        :return: None
        """
        check_methods = [self.int_param, self.check_data]
        max_values = [float('inf'), float('inf'), 1]
        for index, arg in enumerate(args):
            check_methods[index % 2](arg, max_values[index])

    def learn(self, optimizer, learning_rate, epochs, loss):
        """
        Метод проверяет, все ли переданные параметры введены верно.

        :param optimizer: str: Оптимизатор.
        :param learning_rate: float: Коэффициент скорости обучения.
        :param epochs: int: Кол-во эпох.
        :param loss: str: Имя функции ошибки.
        :return: None
        """
        self.uvf(optimizer, self.optimizers)
        self.int_param(learning_rate, max_value=1)
        self.int_param(epochs, max_value=float('inf'))
        self.uvf(loss, self.losses)

    @staticmethod
    def init(df):
        """
        Метод проверяет, является ли {df} таблицой pd.DataFrame и есть ли в этой таблицы все нужные столбцы.

        :param df: pd.DataFrame: Таблица DataFrame
        :return: None
        """
        if not (type(df) == pd.DataFrame):
            raise ValueError('The passed Dataframe must be pd.DataFrame')

        for column in ['loss', 'val_loss', 'epoch']:
            if column not in df.columns:
                raise RuntimeError(f'Column {column} not in DataFrame')
