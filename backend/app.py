import argparse

from flask import Flask

from config import config
from src.adapters import BootstapAdapters, P2PAdapters
from src.routes import BootstrapRouteHandler, P2PRouteHandler


def main():
    app = Flask(__name__)

    if config.IS_BOOTSRAP:
        adapter_services = BootstapAdapters()
        BootstrapRouteHandler(app, adapter_services)
    else:
        adapter_services = P2PAdapters()
        P2PRouteHandler(app, adapter_services)

    app.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Start NoobCash backend')
    parser.add_argument('-b',
                        '--bootstrap',
                        action='store_true',
                        help='Start the NoobCash backend as a bootstrap node.')

    parser.add_argument('-n',
                        '--nodes',
                        type=int,
                        default=5,
                        help='The number of nodes in the NoobCash system.')

    parser.add_argument('-p',
                        '--port',
                        type=int,
                        default=5000,
                        help='The port in which the app will listen')

    args = parser.parse_args()
    config.IS_BOOTSRAP = config.IS_BOOTSRAP if config.IS_BOOTSRAP else args.bootstrap
    config.MAX_USER_COUNT = config.MAX_USER_COUNT if config.MAX_USER_COUNT else args.nodes
    config.PORT = str(config.PORT if config.PORT else args.port)

    main()
