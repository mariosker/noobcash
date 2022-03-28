<img src="/documentation/logo.png" width="200" height="200"/>

# Noobcash

Just another simple blockchain implementation.




## Demo

<img src="/documentation/demo.gif"/>

## API Reference

#### Get balance of your wallet

```http
  GET /balance
```

#### View transactions of the last block in the blockchain

```http
  GET /transactions
```

#### Create a transaction
```http
  POST /transactions
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `node_id`      | `int` | **Required**. Id of the receiver node |
| `amount`      | `int` | **Required**. Amount of BTC to send |

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file or change the `config.py` file.

`ENV`

`HOST`

`PORT`

`IS_BOOTSTRAP`

`BOOTSTRAP_HOST`

`BOOTSTRAP_PORT`

`MAX_USER_COUNT`

`BLOCK_CAPACITY`

`MINING_DIFFICULTY`

## Run Locally

Clone the project

```bash
  git clone https://github.com/mariosker/noobcash
```

or 

```bash
  gh repo clone mariosker/noobcash
```

Go to the project directory

```bash
  cd noobcash
```

Install dependencies

```bash
  pip install -r backend/requirements.txt
  pip install -r cli/requirements.txt
```

Change the env/ config file and start the server

```bash
  python backend/app.py
```

You can also install it via docker:
```bash
cd infra
docker compose up
```

## License

[MIT](https://choosealicense.com/licenses/mit/)

