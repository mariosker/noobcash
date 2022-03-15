import cmd

import pyfiglet

from rest import RestAPI


class Noobcash(cmd.Cmd):
    intro = 'Welcome to the Noobcash client.   Type help or ? to list commands.\n'
    prompt = '(NC) '
    file = None

    def preloop(self) -> None:
        # host = input('Enter the host of your wallet: ')
        port = input('Enter the port of your wallet: ')
        host = 'localhost'
        # port = '5000'
        self.api = RestAPI(host, port)

    def do_t(self, args):
        'Make a transaction given the address of the receiver and the amount of the transaction'

        args = args.split(" ")

        if len(args) != 2:
            print(
                f"You need to provide <recipient_address> and <amount> to make the transaction"
            )
            return

        print('receiver', args[0], 'amount', args[1])
        try:
            self.api.create_transaction(args[0], args[1])
        except Exception as err:
            print(err)

    def do_balance(self, _):
        'Get balance of your wallet'
        try:
            balance = self.api.get_balance()
            print(f"You have {balance} NBC in your account")
        except Exception as err:
            print(err)

    def do_view(self, args):
        'Get the transactions of the last block'
        try:
            transactions = self.api.view_last_transactions()
            print(transactions)
        except Exception as err:
            print(err)

    def do_exit(self, _):
        'Exit the CLI'
        return True


def main():
    result = pyfiglet.figlet_format("NOOBCASH")
    Noobcash().cmdloop(intro=result)


if __name__ == "__main__":
    main()
