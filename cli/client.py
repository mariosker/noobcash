import cmd

import pyfiglet

from rest import RestAPI


class Noobcash(cmd.Cmd):
    intro = 'Welcome to the Noobcash client.   Type help or ? to list commands.\n'
    prompt = '(NC) '
    file = None

    def preloop(self) -> None:
        # host = input('Enter the host of your wallet: ')
        # port = input('Enter the port of your wallet: ')
        host = 'localhost'
        port = '5000'
        self.api = RestAPI(host, port)

    def do_t(self, args):
        'Make a transaction given the address of the receiver and the amount of the transaction'
        args = args.split(" ")
        print('receiver', args[0], 'amount', args[1])

    def do_get_balance(self, _):
        'Get balance of your wallet'
        try:
            balance = self.api.get_balance()
            print(f"You have {balance} NBC in your account")
        except Exception as err:
            print(err)

    def do_get_transactions(self, args):
        'Get the transactions of the last block'
        transactions = self.api.view_last_transactions()
        print(transactions)
        return

    def do_exit(self, _):
        'Exit the CLI'
        return True


def main():
    result = pyfiglet.figlet_format("NOOBCASH")
    Noobcash().cmdloop(intro=result)


if __name__ == "__main__":
    main()
