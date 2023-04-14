import sys

from analytics.application import Application
from tests import test
from logs.logger import logger


def main():
    logger.info('Start program!')
    if 'test' in sys.argv:
        test.run()
    else:
        settings = {}
        app = Application(settings)
        app.run()
    logger.info('Finish program!')


if __name__ == '__main__':
    main()
