from .address_book_main import address_book_main_func
from .notes_main import notes_main_func
from .sort_main import sort_main_func
from .user_interaction import ConsoleInteraction
import sys

TEXT_COLOR = {
    "red": "\033[31m",
    "green": "\033[32m",
    "reset": "\033[0m"
}

# Default print and input replacement
print = ConsoleInteraction.user_output
input = ConsoleInteraction.user_input

# Checking for docker mode
try:
    if sys.argv[1] == 'docker':
        docker_mode = True
        print(TEXT_COLOR['green'] + '\nPersonal helper has been started in a docker mode\n' + TEXT_COLOR["reset"])
    else:
        print(TEXT_COLOR['red'] + "\nIncorrect args!\nPersonal helper has been started in a standard mode!\nYou might have some unexpected errors!\nGo to README.md to check all the modes available!\n" + TEXT_COLOR["reset"])
        docker_mode = False
except IndexError:
    print(TEXT_COLOR['green'] + '\nPersonal helper has been started in a standard mode\n' + TEXT_COLOR["reset"])
    docker_mode = False

def main_func():
    print("\nHi, I'm your personal helper!")

    while True:
        print("\nYou can run: \n-'addressbook'\n-'notebook'", richprint=True)
        if docker_mode == False:
            print("-'sorting_files *path*'", richprint=True)
        print("\nOr close your personal helper by 'close' or 'exit'", richprint=True)

        choose_program_inp = input('\nChoose the program >>> ')

        input_split_list = choose_program_inp.split(' ')

        if choose_program_inp == 'addressbook':
            address_book_main_func()
        
        elif choose_program_inp == 'notebook':
            notes_main_func()

        elif input_split_list[0] == 'sorting_files' and docker_mode == False:
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