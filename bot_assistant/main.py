from bot_assistant.address_book_main import address_book_main_func
from bot_assistant.notes_main import notes_main_func
from bot_assistant.sort_main import sort_main_func


def main_func():
    print("\nHi, I'm your personal helper!")

    while True:
        print("\nYou can run: \n-'addressbook'\n-'notebook' \n-'sorting_files *path*'\n\nOr close your personal helper by 'close' or 'exit'")

        choose_program_inp = input('\nChoose the program >>> ')

        input_split_list = choose_program_inp.split(' ')

        if choose_program_inp == 'addressbook':
            address_book_main_func()
        
        elif choose_program_inp == 'notebook':
            notes_main_func()

        elif input_split_list[0] == 'sorting_files':
            arg = input_split_list[1]
            sort_main_func(arg)
        
        elif choose_program_inp in ['close', 'exit']:
            print('\nGood bye!')
            break
        
        else:
            print('Incorrect command!')

if __name__ == "__main__":
    main_func()