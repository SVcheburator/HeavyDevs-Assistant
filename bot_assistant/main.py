from .address_book_main import address_book_main_func
from .notes_main import notes_main_func
from .sort_main import sort_main_func
from rich import print as rprint

TEXT_COLOR = {
    "red": "\033[31m",
    "green": "\033[32m",
    "reset": "\033[0m"
}

def main_func():
    print("\nHi, I'm your personal helper!")

    while True:
        rprint("\nYou can run: \n-'addressbook'\n-'notebook' \n-'sorting_files *path*'\n\nOr close your personal helper by 'close' or 'exit'")

        choose_program_inp = input('\nChoose the program >>> ')

        input_split_list = choose_program_inp.split(' ')

        if choose_program_inp == 'addressbook':
            address_book_main_func()
        
        elif choose_program_inp == 'notebook':
            notes_main_func()

        elif input_split_list[0] == 'sorting_files':
            try:
                arg = input_split_list[1]
                confirm_input = input(TEXT_COLOR['red'] + f"\nAre you sure you want to sort all the files in ({arg}) path !? \n(y/n) >>> " + TEXT_COLOR['reset'])
                if confirm_input.lower() == 'y':
                    sort_main_func(arg)
                elif confirm_input.lower() == 'n':
                    print('\nOk')
                else:
                    print(TEXT_COLOR['red'] + '\nIncorrect input!\n' + TEXT_COLOR['reset'])
            except IndexError:
                print(TEXT_COLOR['red'] + "\nTo sort files in folder you need to write 'sorting_files *path*'\n" + TEXT_COLOR["reset"])
        
        elif choose_program_inp in ['close', 'exit']:
            print('\nGood bye!')
            break
        
        else:
            print(TEXT_COLOR['red'] + 'Incorrect command!'+ TEXT_COLOR['reset'])

if __name__ == "__main__":
    main_func()