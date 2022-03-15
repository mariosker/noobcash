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

    app.run(host=config.HOST, port=config.PORT)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Start NoobCash backend')
    parser.add_argument('-b',
                        '--bootstrap',
                        default=None,
                        action='store_true',
                        help='Start the NoobCash backend as a bootstrap node.')

    parser.add_argument('-p',
                        '--port',
                        type=int,
                        default=None,
                        help='The port in which the app will listen')

    parser.add_argument('-n',
                        '--nodes',
                        type=int,
                        default=None,
                        help='The number of nodes in the NoobCash system.')

    args = parser.parse_args()

    config.IS_BOOTSRAP = args.bootstrap if args.bootstrap else config.IS_BOOTSRAP
    config.MAX_USER_COUNT = args.nodes if args.nodes else config.MAX_USER_COUNT
    config.PORT = args.port if args.port else config.PORT
    print(f'\nHost\'s IP: {config.HOST}, Host\'s Port: {config.PORT}')
    print(f'Boostrap\'s IP: {config.BOOTSTRAP_HOST}, Boostrap\'s Port: {config.BOOTSTRAP_PORT}')
    print(f'Nodes in the network: {config.MAX_USER_COUNT}, Block\'s Capacity: {config.BLOCK_CAPACITY}, Mining Difficulty: {config.MINING_DIFFICULTY}\n')

    main()
