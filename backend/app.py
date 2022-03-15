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
    print(f'\nHost\'s IP: {config.HOST}, Host\'s Port: {config.PORT}')
    print(f'Boostrap\'s IP: {config.BOOTSTRAP_HOST}, Boostrap\'s Port: {config.BOOTSTRAP_PORT}')
    print(f'Nodes in the network: {config.MAX_USER_COUNT}, Block\'s Capacity: {config.BLOCK_CAPACITY}, Mining Difficulty: {config.MINING_DIFFICULTY}\n')

    main()
