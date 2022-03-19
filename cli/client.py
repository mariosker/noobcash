import cmd

import pyfiglet

from rest import RestAPI


class Noobcash(cmd.Cmd):
    intro = 'Welcome to the Noobcash client.   Type help or ? to list commands.\n'
    prompt = '(NC) '
    file = None

    def preloop(self) -> None:
        print(pyfiglet.figlet_format("NOOBCASH"))
        port = input('Enter the port of your wallet: ')
        host = 'localhost'
        self.api = RestAPI(host, port)

    def do_t(self, args):
        't <recipient_id> <amount>\nMake a transaction of NBC coins given the id of the receiver and the specified amount'

        args = args.split(" ")

        if len(args) != 2:
            print(
                f"You need to provide <recipient_address> and <amount> to make the transaction"
            )
            return

        try:
            self.api.create_transaction(args[0], args[1])
        except Exception as err:
            print(err)

    def do_balance(self, _):
        'Check the balance of your wallet'
        try:
            balance = self.api.get_balance()
            print(f"You have {balance} NBC coins in your wallet")
        except Exception as err:
            print(err)

    def do_view(self, _):
        'View the transactions of the last block of the blockchain'
        try:
            transactions = self.api.view_last_transactions()
            print(transactions)
        except Exception as err:
            print(err)

    def do_exit(self, _):
        'Exit the Noobcash CLI'
        return True


def main():
    Noobcash().cmdloop()


if __name__ == "__main__":
    main()
