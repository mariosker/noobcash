from adapters import Adapters
from flask import Flask
from routes import RouteHandler

if __name__ == "__main__":
    app = Flask(__name__)

    my_adapter = Adapters()
    RouteHandler(app, my_adapter)

    app.run()
'''
env = BOOTSTRAP | n
if bootstap:
    BOOTSTRAP -> node(id = 0)
else:
    get (id) -> node(id)

cli(node)
'''
