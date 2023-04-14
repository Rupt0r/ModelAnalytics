import pandas as pd
import tensorflow as tf
import numpy as np

from analytics.dataframe import DF
from keras.layers import Dense, Dropout
from keras.optimizers import SGD, Adam, RMSprop, Adadelta, Adagrad, Adamax, Nadam, Ftrl

from check.checkparams import CheckParams
from logs.logger import logger


class Model:
    """
    Класс, который позволяет создавать, обучать любую модель.
    """

    def __init__(self):
        """
        Конструктор.
        """
        self.df = DF()
        self.df.set_Xy_dataset()
        self.my_model = None
        self.history = None
        self.new_history = None
        self.normalizer = None
        self.optimizers = {'SGD': SGD, 'Adam': Adam, 'RMSprop': RMSprop, 'Adadelta': Adadelta,
                           'Adagrad': Adagrad, 'Adamax': Adamax, 'Nadam': Nadam, 'Ftrl': Ftrl}

    def model_generator(self, layers: int = 0, data_layers: tuple = (64, 'relu'), drop_kof: float = 0.0):
        """
        Метод, который создает модель по определённым параметрам.

        :param layers: int: Кол-во слоёв.
        :param data_layers: tuple(int, str): Кол-во нейронов и функция активации каждого слоя
        :param drop_kof: float: Коэффициент дропа нейронов на слое
        :return: None
        """
        logger.info('Model generation.')
        CheckParams().model_generator(layers, data_layers, drop_kof)
        self.normalizer = tf.keras.layers.experimental.preprocessing.Normalization()
        self.normalizer.adapt(np.array(self.df.X))
        model = tf.keras.Sequential()
        model.add(self.normalizer)
        for _ in range(layers):
            model.add(Dense(data_layers[0], activation=data_layers[1]))
            if 0 < drop_kof <= 1:
                model.add(Dropout(drop_kof))
        model.add(Dense(units=1))
        self.my_model = model

    def learn(self, optimizer: str, learning_rate: float, epochs: int, loss: str):
        """
        Метод, который обучает созданную модель также по определённым параметрам.

        :param optimizer: str: Оптимизатор.
        :param learning_rate: float: Коэффициент скорости обучения.
        :param epochs: int: Кол-во эпох.
        :param loss: str: Функция ошибки.
        :return: None
        """
        logger.info('Model Training.')
        CheckParams().learn(optimizer, learning_rate, epochs, loss)
        self.my_model.compile(optimizer=self.optimizers[optimizer](learning_rate=learning_rate), loss=loss)
        self.history = self.my_model.fit(self.df.X, self.df.y, epochs=epochs, verbose=0, validation_split=0.2)

    def get_history(self) -> pd.DataFrame:
        """
        Метод, который возвращает историю обучения.

        :return: pd.DataFrame
        """
        self.new_history = self.df.new_df(self.my_model.history.history)
        self.new_history['epoch'] = self.my_model.history.epoch
        return self.new_history

    def show(self):
        """
        Метод, который покажет архитектуру модели.

        :return:
        """
        self.my_model.summary()
