import sys

from analytics.application import Application
from logs.logger import logger
from tests import test


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
