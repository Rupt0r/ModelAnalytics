import matplotlib.pyplot as plt
import numpy as np

from check.checkparams import CheckParams
from logs.logger import logger


class Chart:
    """
    Класс, для визуализации обучения модели
    """

    def __init__(self, *, history):
        """
        Конструктор.

        :param history: pd.DataFrame: Таблица с данными по обучению модели
        """
        CheckParams().init(history)
        self.history = history

    def show(self):
        """
        Данный метод визуализирует данные ввиде графика.

        :return: None
        """
        logger.info('Create graph.')
        plt.plot(self.history['loss'], label='loss')
        plt.plot(self.history['val_loss'], label='val_loss')
        plt.xticks(np.array(self.history['epoch'])[::10])
        plt.xlabel('Epoch')
        plt.ylabel('Error')
        plt.legend()
        plt.grid(True)
        plt.show()

    def get_accuracy(self) -> tuple:
        """
        Этот метод находит итоговые {loss} и {val_loss} значениея.

        :return: tuple
        """
        loss = list(self.history[-1:].loss ** 0.5)[0]
        val_loss = list(self.history[-1:].val_loss ** 0.5)[0]
        return loss, val_loss

    def show_accuracy(self):
        """
        Метод демонстрирует значения {loss} и {val_loss} на экране.

        :return: None
        """
        loss, val_loss = self.get_accuracy()
        print(f'{loss=}\n{val_loss=}')
