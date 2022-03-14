import cmd

import pyfiglet


class Noobcash(cmd.Cmd):
    intro = 'Welcome to the noobcash client.   Type help or ? to list commands.\n'
    prompt = '(NC) '

    def do_t(self, args):
        'Make a transaction'
        print('receiver', args[0], 'amount', args[1])

def main():
    result = pyfiglet.figlet_format("NOOBCASH")
    print(result)
    Noobcash().cmdloop()


if __name__ == "__main__":
    main()

