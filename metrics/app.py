from threading import Lock
from flask import Flask, request

app = Flask(__name__)
times = {}
mining = {}
transactions = {}
time_lock = Lock()
trans_lock = Lock()
mine_lock = Lock()
valid_transactions_lock = Lock()
start = None
end = None
valid_transactions = 0


@app.post("/log/add_valid_transaction")
def start_transactions():
    global valid_transactions
    valid_transactions_lock.acquire()
    valid_transactions += 1
    valid_transactions_lock.release()


@app.post("/log/start_transactions/<time>")
def start_transactions(time):
    global start
    start = time


@app.post("/log/end_transactions/<time>")
def end_transactions(time):
    global end
    end = time


@app.post("/log/add_block/<int:id>/<time>")
def add_block_time(id, time):
    time_lock.acquire()
    if id in times:
        times[id].append(time)
    else:
        times[id] = [time]
    time_lock.release()
    return ""


@app.post("/log/add_transaction/<int:id>/<time>")
def add_transaction_time(id, time):
    trans_lock.acquire()
    if id in transactions:
        transactions[id].append(time)
    else:
        transactions[id] = [time]
    trans_lock.release()
    return ""


@app.post("/log/add_mine/<int:id>/<time>")
def add_mine_time(id, time):
    mine_lock.acquire()
    if id in mining:
        mining[id].append(time)
    else:
        mining[id] = [time]
    mine_lock.release()
    return ""


@app.post('/shutdown')
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')

    calculate_statistics()

    func()
    return "Shutting down..."


def calculate_statistics():
    print('WHAT AM I DOING')


app.run(port=7000)
