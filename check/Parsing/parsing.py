import requests
from bs4 import BeautifulSoup

from logs.logger import logger


class Soup:
    """
    Класс по парсингу сайтов.
    """

    def __init__(self, url):
        """
        Конструктор.

        Для начала мы получаем сырой html-code, который передаем в класс BeautifulSoup,
        где уже можно будет быстро и просто находить нужну информацию.

        :param url: str: ссылка на web-сайт.
        """
        self._html_code = requests.get(url).text
        self._soup = BeautifulSoup(self._html_code, features="html.parser")

    def get(self):
        """
        Геттер класса, который вернёт "обработанный" html-code.

        :return: BeautifulSoup
        """
        return self._soup

    def show(self):
        """
        Вывод html-code на экран.

        Нужно для визуального поиска нужной информации.

        :return: None
        """
        print(self._soup)


class Base:
    """
    Это базовый класс для парсинга официальной документации Keras (https://keras.io).
    """

    def __init__(self, url):
        """
        Конструктор.

        :param url: str: ссылка на сайт.
        """
        self.array: list = []
        self.soup = Soup(url).get()
        self.parsing()
        self.update()

    def parsing(self):
        """
        Данный метод будет брать html-code,
        и находить по определенным тегам нужную информацию.

        :return: None
        """
        pass

    def update(self):
        """
        Данный метод будет обрабатывать список,
        и/или удалять/добавлять какую-либо информацию.

        :return: None
        """
        pass

    def get(self):
        """
        Данный метод будет возвращать список, который был собран во время парсинга.

        :return: list
        """
        return self.array


class LossesFunctions(Base):
    """
    Наследуемый класс, который ищет данные о функциях 'ошибок'.
    """

    def __init__(self):
        """
        Конструктор

        :param self.url: str: ссылка на информацию по 'ошибочным' функциям.
        :param self.value_error: str: именование ошибки, если такова будет.
        """
        self.url = 'https://keras.io/api/losses/regression_losses/'
        super().__init__(self.url)
        self.value_error = 'loss function or class'

    def parsing(self):
        """
        Пасрим сайт, получая названия функций.

        :return: None
        """
        logger.info('Parsing regression_losses')
        for under_soup in self.soup.select('pre'):
            name = under_soup.text.split('(')[0]
            if name.startswith('tf.'):
                self.array.append(name)

    def update(self):
        """
        Здесь мы обрабатываем имена, создавая ещё по 2 формы имени.

        Нужно, чтобы, не важно как ведет человек имя функции, программа поняла, что вели.

        :return: None
        """
        errors = self.array
        self.array += list(map(lambda line: line.split('.')[-1], errors))
        self.array += list(map(lambda line: '.'.join(line.split('.')[1:]), errors))
        self.array = self.array[:self.array.index('')]


class ActivationFunctions(Base):
    """
    Наследуемый класс, который ищет данные о функциях активации.
    """

    def __init__(self):
        """
        Конструктор

        :param self.url: str: ссылка на информацию по функциям активации.
        :param self.value_error: str: именование ошибки, если такова будет.
        """
        self.url = 'https://keras.io/api/layers/activations/'
        super().__init__(self.url)
        self.value_error = 'activation function'

    def parsing(self):
        """
        Пасрим сайт, получая названия функций.

        :return: None
        """
        logger.info('Parsing activations')
        for under_soup in self.soup.select('h3'):
            name = under_soup.select_one('code').text
            self.array.append(name)


class Optimizers(Base):
    """
    Наследуемый класс, который ищет данные по оптимизаторам.
    """

    def __init__(self):
        """
        Конструктор

        :param self.url: str: ссылка на информацию по оптимизаторам.
        :param self.value_error: str: именование ошибки, если такова будет.
        """
        self.url = 'https://keras.io/api/optimizers/'
        super().__init__(self.url)
        self.value_error = 'optimizer'

    def parsing(self):
        """
        Пасрим сайт, получая названия оптимизаторов.

        :return: None
        """
        logger.info('Parsing optimizers')
        for under_soup in self.soup.select('ul')[:1]:
            for block in under_soup.select('li'):
                self.array.append(block.text)
