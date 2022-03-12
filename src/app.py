import argparse
from flask import Flask
from src.adapters.adapters import Adapters
from src.routes import RouteHandler
from src import config


def main(is_bootstrap, max_user_count):
    app = Flask(__name__)

    adapterServices = Adapters(is_bootstrap, max_user_count)
    RouteHandler(app, adapterServices)

    app.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Start NoobCash backend')
    parser.add_argument('-b',
                        '--bootstrap',
                        action='store_true',
                        help='Start the NoobCash backend as a bootstrap node.')

    parser.add_argument('-n',
                        '--nodes',
                        nargs='?',
                        type=int,
                        default=5,
                        help='The number of nodes in the NoobCash system.')

    parser.add_argument('-p',
                        '--port',
                        type=int,
                        default=5,
                        help='The port in which the app will listen')

    args = parser.parse_args()
    config.IS_BOOTSRAP = config.IS_BOOTSRAP if config.IS_BOOTSRAP else args.bootstrap
    config.MAX_USER_COUNT = config.MAX_USER_COUNT if config.MAX_USER_COUNT else args.nodes

    main(config.IS_BOOTSRAP, config.MAX_USER_COUNT)