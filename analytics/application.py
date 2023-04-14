from dataclasses import dataclass

from analytics.model import Model
from analytics.chart import Chart


@dataclass
class Settings:
    layers: int = 0
    data_layers: tuple[int, str] = (64, 'relu')
    drop_kof: int = 0
    optimizer: str = 'Adam'
    learning_rate: float = 0.1
    epochs: int = 100
    loss: str = 'mean_squared_error'


class Application:
    """
    Основной код, с которым обращается пользователь.
    """
    __IS_CREATED = None

    def __new__(cls, *args, **kwargs):
        """
        Метод проверяет, есть ли объект класса или нет.

        Если нет, то создаёт. Иначе говорит, что объект класса уже есть.

        :param args: list: =\\_(0_0)_//=
        :param kwargs: dict: =\\_(0_0)_//=
        """
        if cls.__IS_CREATED is None:
            cls.__IS_CREATED = True
            return super(Application, cls).__new__(cls)
        else:
            raise RuntimeError('Я уже есть. Просто обнови данные. <# app.initial(settings) #>')

    def __init__(self, settings: dict):
        """
        Конструктор.

        Здесь {settings} является настройками модели, так как в нем может храниться любая информация о модели.

        :param settings: dict: Кастомные параметры модели.
        """
        if type(settings) != dict:
            raise ValueError('Передаваемые настройки должны быть типа dict.')

        self.dc = Settings(**settings)  # dc = DataClass
        self.my_model = None
        self.chart = None

    def run(self):
        """
        Метод старта программы.

        Создание модели. Создание архитектуры модели. Обучение модели.
        Создание и вывод графика модели и некоторые параметры.

        :return: None
        """
        self.my_model = Model()
        self.my_model.model_generator(
            layers=self.dc.layers, data_layers=self.dc.data_layers, drop_kof=self.dc.drop_kof
            )
        self.my_model.learn(
            optimizer=self.dc.optimizer, learning_rate=self.dc.learning_rate, epochs=self.dc.epochs, loss=self.dc.loss
            )
        self.chart = Chart(history=self.my_model.get_history())
        self.chart.show_accuracy()
        self.chart.show()

    def initial(self, settings):
        """
        Метод для обновления данных.

        :param: dict: Новые настройки модели.
        :return: None
        """
        self.__init__(settings)
