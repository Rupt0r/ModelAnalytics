import unittest

import pandas as pd

from check.checkparams import CheckParams


class Tests(unittest.TestCase):
    """
    Тут происходит проверка всевозможных кривых ввод данных.
    """

    def test_csv_file_extension(self):
        """
        Проверяет, имеет ли файл расширение.

        :return: None
        """
        self.assertRaises(RuntimeError, CheckParams().csv, filename='data')

    def test_csv_filename(self):
        """
        Проверяет, есть ли данный файл в проекте.

        :return: None
        """
        self.assertRaises(FileNotFoundError, CheckParams().csv, filename='0.csv')

    def test_filling(self):
        """
        Проверяет, что переданное значение является словарём (dict).

        :return: None
        """
        self.assertRaises(ValueError, CheckParams().filling, filling=[])

    def test_int_param_value(self):
        """
        Проверяет, является ли переданное значение целым числом.

        :return: None
        """
        self.assertRaises(ValueError, CheckParams().int_param, '1.2')

    def test_int_param_range(self):
        """
        Проверяет, попадает ли число в диапазон от 0 до {max_value}.

        :return: None
        """
        self.assertRaises(RuntimeError, CheckParams().int_param, 12, max_value=10.0)

    def test_uvf_type(self):
        """
        Проверяет, является ли {data} строкой или объектом класса.

        :return: None
        """
        self.assertRaises(ValueError, CheckParams().uvf, data=121, _object=CheckParams().optimizers)

    def test_uvf_not_in_list(self):
        """
        Проверяет, есть ли {data} в списке доступных "значений".

        :return:
        """
        self.assertRaises(RuntimeError, CheckParams().uvf, data='adam', _object=CheckParams().optimizers)

    def test_check_data(self):
        """
        Проверяет, является ли переданное значение кортеждом (tuple).

        :return: None
        """
        self.assertRaises(ValueError, CheckParams().check_data, [10, 10], 10)

    def test_check_init_df(self):
        """
        Проверяет, является ли переданное значение DataFrame'ом.

        :return: None
        """
        self.assertRaises(ValueError, CheckParams().init, {'': {"": {}}})

    def test_check_init_df_columns(self):
        """
        Проверяет, есть ли все нужные столбцы в DataFrame.

        :return: None
        """
        self.assertRaises(RuntimeError, CheckParams().init, pd.DataFrame(columns=['loss', 'val_loss']))


def run():
    unittest.main()
