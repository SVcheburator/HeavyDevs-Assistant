import os
import pathlib
from datetime import datetime
from platformdirs import user_data_dir
from rich import print as rprint
from .address_book_classes import Birthday, Phone, Email, Name, Record, Address, AddressBook, error_keeper


TEXT_COLOR = {
    "red": "\033[31m",
    "green": "\033[32m",
    "reset": "\033[0m"
}


ab = AddressBook()

# Iterator
class ABIterator:
    def __iter__(self):
        return ab

abi = ABIterator()


def iter():
    ab.current_index = 0
    counter = ab.current_index
    for rec in abi:
        counter += 1
        print(rec)

        if (counter % 2) == 0:
            rprint("type 'next' to see the next page or type enything else to stop")
            inp = str(input(">>> "))
            if inp == 'next':
                continue
            else:
                print('\n')
                break

# Adding contact function
def add_contact(inp_split_lst):
    if 'phone' not in inp_split_lst:
        input_phone = None
    else:
        input_phone = True
    if 'email' not in inp_split_lst:
        input_email = None
    else:
        input_email = True
    if 'birthday' not in inp_split_lst:
        input_birthday = None
    else:
        input_birthday= True
    if 'address' not in inp_split_lst:
        input_address = None
    else:
        input_address = True

    input_name = ' '.join(inp_split_lst[1:])

    if input_address:
        input_name = ' '.join(inp_split_lst[1:inp_split_lst.index('address')])
        input_address = ' '.join(inp_split_lst[inp_split_lst.index('address')+1:])

    if input_birthday:
        input_name = ' '.join(inp_split_lst[1:inp_split_lst.index('birthday')])
        input_birthday = ' '.join(inp_split_lst[inp_split_lst.index('birthday')+1:])
        try:
            input_birthday = ' '.join(inp_split_lst[inp_split_lst.index('birthday')+1:inp_split_lst.index('address')])
        except ValueError:
            pass
        try:
            input_phone = ' '.join(inp_split_lst[inp_split_lst.index('phone')+1:inp_split_lst.index('birthday')])
        except ValueError:
            pass
        try:
            input_email = ' '.join(inp_split_lst[inp_split_lst.index('email')+1:inp_split_lst.index('birthday')])
        except ValueError:
            pass

    if input_email:
        input_name = ' '.join(inp_split_lst[1:inp_split_lst.index('email')])
        input_email = ' '.join(inp_split_lst[inp_split_lst.index('email')+1:])
        try:
            input_email = ' '.join(inp_split_lst[inp_split_lst.index('email')+1:inp_split_lst.index('address')])
        except ValueError:
            pass
        try:
            input_email = ' '.join(inp_split_lst[inp_split_lst.index('email')+1:inp_split_lst.index('birthday')])
        except ValueError:
            pass

    if input_phone:
        input_name = ' '.join(inp_split_lst[1:inp_split_lst.index('phone')])
        input_phone = ' '.join(inp_split_lst[inp_split_lst.index('phone')+1:])
        try:
            input_phone = ' '.join(inp_split_lst[inp_split_lst.index('phone')+1:inp_split_lst.index('address')])
        except ValueError:
            pass
        try:
            input_phone = ' '.join(inp_split_lst[inp_split_lst.index('phone')+1:inp_split_lst.index('birthday')])
        except ValueError:
            pass
        try:
            input_phone = ' '.join(inp_split_lst[inp_split_lst.index('phone')+1:inp_split_lst.index('email')])
        except ValueError:
            pass
        
    ab.add_record(Record(Name(name=input_name), Phone(phone=input_phone), Email(email=input_email), Birthday(birthday=input_birthday), Address(address = input_address), ab=ab))

# Field operations
@error_keeper
def add_field(inp_split_lst, type):
    name = ' '.join(inp_split_lst[1:inp_split_lst.index(type)])
    add = ' '.join(inp_split_lst[inp_split_lst.index(type)+1:])

    if type == 'phone':
        ab[name].add_phone(Phone(phone=add))

    elif type == 'email':
        ab[name].add_email(Email(email=add))

    elif type == 'birthday':
        ab[name].add_birthday(Birthday(birthday=add))

    elif type == 'address':
        ab[name].add_address(Address(address=add))

@error_keeper
def change_field(inp_split_lst, type):
    name = ' '.join(inp_split_lst[1:inp_split_lst.index(type)])
    change_from = ' '.join(inp_split_lst[inp_split_lst.index(type)+1:inp_split_lst.index('to')])
    change_to = ' '.join(inp_split_lst[inp_split_lst.index('to')+1:])

    if type == 'phone':
        ab[name].change_phone(Phone(phone=change_from), Phone(phone=change_to))

    elif type == 'email':
        ab[name].change_email(Email(email=change_from), Email(email=change_to))

    elif type == 'birthday':
        ab[name].change_birthday(Birthday(birthday=change_from), Birthday(birthday=change_to))

    elif type == 'address':
        ab[name].change_address(Address(address=change_from), Address(address=change_to))


@error_keeper
def delete_field(inp_split_lst, type):
    name = ' '.join(inp_split_lst[1:inp_split_lst.index(type)])
    del_item = ' '.join(inp_split_lst[inp_split_lst.index(type)+1:])
    
    if type == 'phone':
        ab[name].delete_phone(Phone(phone=del_item))

    elif type == 'email':
        ab[name].delete_email(Email(email=del_item))

    elif type == 'birthday':
        ab[name].delete_birthday(Birthday(birthday=del_item))

    elif type == 'address':
        ab[name].delete_address(Address(address=del_item))


def birthday_within_time(inp_split_lst):
    type = inp_split_lst[-1]
    amount = int(inp_split_lst[1])
    
    if type == 'days':
        if 0 < amount < 365:
            days = amount
        else:
            print(TEXT_COLOR['red'] + 'Incorrect number of days!\n' + TEXT_COLOR['reset'])
            return None
    elif type == 'weeks':
        if 0 < amount <= 52:
            days = amount*7
        else:
            print(TEXT_COLOR['red'] + 'Incorrect number of weeks!\n' + TEXT_COLOR['reset'])
            return None
    elif type == 'months':
        if 0 < amount < 12:
            now = datetime.now()
            if now.month + amount <= 12:
                last_date = datetime(year=now.year, month=now.month + amount, day=now.day)
                days = (last_date - now).days + 1
            else:
                last_date = datetime(year=now.year+1, month=(now.month+amount-12), day=now.day)
                days = (last_date - now).days + 1
        else:
            print(TEXT_COLOR['red'] + 'Incorrect number of months\n' + TEXT_COLOR['reset'])
            return None
    else:
        print(TEXT_COLOR['red'] + 'Incorrect type of time interval!\n' + TEXT_COLOR['reset'])
        return None
    
    result = ''

    for rec in ab.data.values():
        if rec.birthday != None and rec.days_to_birthday() != None:
            if rec.days_to_birthday() <= days:
                result += str(rec)
    
    if len(result) > 0:
        print(result)
    else:
        print(TEXT_COLOR['red'] + 'No one found within this interval\n' + TEXT_COLOR['reset'])


def find_func(inp_split_lst):
    inp = ' '.join(inp_split_lst[1:]).strip()
    ab.find_contact(inp)

def get_file_path(file_name):
    path = pathlib.Path(user_data_dir("Personal assistant"))
    if os.name == "nt":
        path = path.parent
    if not path.is_dir():
        path.mkdir()
    file_path = path.joinpath(file_name)
    return file_path

# Main function with all input logic
def address_book_main_func():
    file_path = get_file_path("addressbook.bin")
    ab.load_from_file(file_path)
    rprint("\nInput 'commands' to see all the commands avalible!\n")

    while True:
        ab.save_to_file(file_path)

        ask = input('>>> ')
        inp_split_lst = ask.split(' ')
        commands = ['add_contact', 'delete_contact', 'clear_addressbook', 'add_phone', 'change_phone', 'delete_phone', 'add_email', 'change_email', 'delete_email', 'add_birthday', 'change_birthday', 'delete_birthday', 'birthday_within', "add_address", "change_address", "delete_address", 'find', 'show', 'show_all', 'close', 'exit']
        command = inp_split_lst[0].lower()
        
        if command == 'hello':
            print("How can I help you?\nInput 'commands' to see all the commands avalible!\nFor more information go to README.md\n")

        elif command == 'commands':
            print('\nCommands avalible:\n')
            for com in commands:
                rprint("-"+"'"+com+"'")
            rprint('For more information go to README.md\n')

        elif command == 'add_contact':
            add_contact(inp_split_lst)

        elif command == 'delete_contact':
            ab.delete_record(' '.join(inp_split_lst[1:]))

        elif command == 'clear_addressbook':
            confirm_input = input(TEXT_COLOR['red'] + 'Are you sure you want to delete all the data!? (y/n) >>> ' + TEXT_COLOR['reset'])
            if confirm_input.lower() == 'y':
                if len(ab.data) > 0:    
                    ab.clear_data()
                else:
                    print(TEXT_COLOR['red'] + '\nThere is nothing to delete!\n' + TEXT_COLOR['reset'])
            elif confirm_input.lower() == 'n':
                print('\nOk\n')
            else:
                print(TEXT_COLOR['red'] + '\nIncorrect input!\n' + TEXT_COLOR['reset'])

        elif command == 'add_phone':
            add_field(inp_split_lst, 'phone')

        elif command == 'change_phone':
            change_field(inp_split_lst, 'phone')

        elif command == 'delete_phone':
            delete_field(inp_split_lst, 'phone')
        
        elif command == 'add_email':
            add_field(inp_split_lst, 'email')

        elif command == 'change_email':
            change_field(inp_split_lst, 'email')

        elif command == 'delete_email':
            delete_field(inp_split_lst, 'email')

        elif command == 'add_birthday':
            add_field(inp_split_lst, 'birthday')

        elif command == 'change_birthday':
            change_field(inp_split_lst, 'birthday')

        elif command == 'delete_birthday':
            delete_field(inp_split_lst, 'birthday')
        
        elif command == 'birthday_within':
            birthday_within_time(inp_split_lst)

        elif command == 'add_address':
            add_field(inp_split_lst, 'address')
        
        elif command == 'change_address':
            change_field(inp_split_lst, 'address')

        elif command == 'delete_address':
            delete_field(inp_split_lst, 'address')

        elif command == 'find':
            find_func(inp_split_lst)

        elif command == 'show':
            iter()

        elif command == 'show_all':
            if len(ab) > 0:
                print(ab)
            else:
                print('\nYour address book is empty now!\n')

        elif command in commands[-2:]:
            print('\nGood bye!')
            break

        else:
            print(TEXT_COLOR['red'] + f"\nUnknown command ({command})\nInput 'commands' to see all the commands avalible!\nFor more information go to README.md\n" + TEXT_COLOR['reset'])