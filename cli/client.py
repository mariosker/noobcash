import cmd

import pyfiglet

from requests import RestAPI


class Noobcash(cmd.Cmd):
    intro = 'Welcome to the Noobcash client.   Type help or ? to list commands.\n'
    prompt = '(NC) '
    file = None

    def preloop(self) -> None:
        # host = input('Enter the host of your wallet: ')
        # port = input('Enter the port of your wallet: ')
        host = port = 1000
        self.api = RestAPI(host, port)

    def do_t(self, args):
        'Make a transaction given the address of the receiver and the amount of the transaction'
        args = args.split(" ")
        print('receiver', args[0], 'amount', args[1])

    def do_get_balance(self):
        'Get balance of your wallet'
        balance = self.api.get_balance() | 0
        print(f"You have {balance} NBC in your account")

    def do_get_transactions(self):
        'Get the transactions of the last block'
        transactions = self.api.view_last_transactions()
        print(transactions)
        return

    def exit(self):
        self.close()


def main():
    result = pyfiglet.figlet_format("NOOBCASH")
    Noobcash().cmdloop(intro=result)


if __name__ == "__main__":
    main()
