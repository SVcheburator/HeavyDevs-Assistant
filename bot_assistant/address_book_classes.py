import pickle
import re
from collections import UserDict
from datetime import datetime


TEXT_COLOR = {
    "red": "\033[31m",
    "green": "\033[32m",
    "reset": "\033[0m"
}


# Custom errors
class BirthdayError(Exception):
    pass


class PhoneError(Exception):
    pass


class EmailError(Exception):
    pass


# Decorator
def error_keeper(function):
    def inner(*args):
        try:
            function(*args)
        except BirthdayError:
            print(TEXT_COLOR['red'] + 'That is incorrect birthday!' + TEXT_COLOR['reset'])
        except PhoneError as pe:
            if pe.args:
                print(TEXT_COLOR['red'] + f'This phone number is too {pe.args[0]}!' + TEXT_COLOR['reset'])
            else:
                print(TEXT_COLOR['red'] + 'That is incorrect phone number!' + TEXT_COLOR['reset'])
        except EmailError:
            print(TEXT_COLOR['red'] + 'That is incorrect email!' + TEXT_COLOR['reset'])
        except ValueError:
            print(TEXT_COLOR['red'] + 'Something is wrong!\nGo to README.md to check the correctness\n' + TEXT_COLOR['reset'])
        except AttributeError:
            print(TEXT_COLOR['red'] + 'Something is wrong!\nGo to README.md to check the correctness\n' + TEXT_COLOR['reset'])
        except KeyError:
            print(TEXT_COLOR['red'] + 'Name is incorrect!\n' + TEXT_COLOR['reset'])

    return inner


# Classes
class Field:
    def __init__(self, name=None, phone=None, email=None, birthday=None, address=None):
        if name:
            self.value = name
        if phone:
            self.__value = None
            self.value = phone
        if email:
            self.__value = None
            self.value = email
        if birthday:
            self.__value = None
            self.value = birthday
        if address:
            self.__value = None
            self.value = address


class Birthday(Field):
    @property
    def value(self):
        if self.__value:
            return self.__value

    
    @value.setter
    @error_keeper
    def value(self, value):
        try:
            self.__value = datetime.strptime(value, "%d %m %Y")
        except ValueError:
            self.__value = None
            raise BirthdayError
        except IndexError:
            self.__value = None
            raise BirthdayError


class Phone(Field):
    @property
    def value(self):
        if self.__value:
            return self.__value

    @value.setter
    @error_keeper
    def value(self, value):
        try:
            if int(value.strip()) or (value.startswith('+') and int(value[1:])):
                self.__value = value
                if 10 > len(value):
                    self.__value = None
                    raise PhoneError('short')
                if 13 < len(value):
                    self.__value = None
                    raise PhoneError('long')
            else:
                self.__value = None
        except ValueError:
            self.__value = None
            raise PhoneError


class Email(Field):
    @property
    def value(self):
        if self.__value:
            return self.__value

    @value.setter
    @error_keeper
    def value(self, value):
        pattern = r"[A-Za-z]{1}[A-Za-z0-9._]{1,}@[A-Za-z]+\.[A-Za-z]{2,}"
        if re.match(pattern, value):
            self.__value = value
        else:
            self.__value = None
            raise EmailError


class Name(Field):
    pass


class Address(Field):
    @property
    def value(self):
        if self.__value:
            return self.__value

    @value.setter
    def value(self, value):
        address_split_lst = value.split(' ')
        if 'street' in address_split_lst:
            street = ' '.join(address_split_lst[address_split_lst.index('street')+1:])
            if 'building' in address_split_lst:
                street = ' '.join(address_split_lst[address_split_lst.index('street')+1:address_split_lst.index('building')])
                building = ' '.join(address_split_lst[address_split_lst.index('building')+1:])
                if 'apartment' in address_split_lst:
                    building = ' '.join(address_split_lst[address_split_lst.index('building')+1:address_split_lst.index('apartment')])
                    apartment = ' '.join(address_split_lst[address_split_lst.index('apartment')+1:])
        
        try:
            self.__value = ''
            self.__value += 'Street: ' + street
            try:
                self.__value += '\nBuilding: ' + building
                try:
                    self.__value += '\nApartment: ' + apartment
                except UnboundLocalError:
                    pass
            except UnboundLocalError:
                pass
        except UnboundLocalError:
            pass


class Record:
    def __init__(self, person_name, phone_num=None, email=None, birthday=None, address=None, ab=None):
        self.ab = ab
        self.name = person_name
        
        if phone_num:
            self.phones = []
            self.phones.append(phone_num)

        if email:
            self.emails = []
            self.emails.append(email)
        
        if birthday:
            self.birthday = birthday
        
        if address:
            self.address = address
    
    # Phone operations
    def add_phone(self, extra_phone, flag=True):
        try:
            try:
                self.phones.append(extra_phone)
                for x in self.phones:
                    x.value
            except AttributeError:
                self.phones = []
                self.phones.append(extra_phone)

            if flag == True and extra_phone.value != None:
                print(TEXT_COLOR['green'] + f'Phone number {extra_phone.value} has been successfully added!\n' + TEXT_COLOR['reset'])
        except AttributeError:
            pass

    def change_phone(self, some_phone, different_phone):
        try:
            flag = False
            if different_phone.value != None:
                for ph in self.phones:
                    if ph.value == some_phone.value:
                        self.phones.append(different_phone)
                        self.phones.remove(ph)
                        print(TEXT_COLOR['green'] + f'Phone number {some_phone.value} has been successfully changed to {different_phone.value}\n' + TEXT_COLOR['reset'])
                        flag = True
            else:
                flag = True
        except AttributeError:
            flag == False
        if flag == False:
            print(TEXT_COLOR['red'] + f'There is no such phone!' + TEXT_COLOR['reset'])

    def delete_phone(self, some_phone):
        try:
            if some_phone.value != None:
                flag = False
                for ph in self.phones:
                    if ph.value == some_phone.value:
                        self.phones.remove(ph)
                        flag = True
                        print(TEXT_COLOR['green'] + f'Phone number {some_phone.value} has been successfully deleted\n' + TEXT_COLOR['reset'])
        except AttributeError:
            flag = False
            
        if flag == False:
            print(TEXT_COLOR['red'] + f'There is no such phone as {some_phone.value}\n' + TEXT_COLOR['reset'])

    # Email operations
    def add_email(self, extra_email):
        if extra_email.value != None:
            try:
                self.emails.append(extra_email)
                for x in self.emails:
                    x.value
            except AttributeError:
                self.emails = []
                self.emails.append(extra_email)

            print(TEXT_COLOR['green'] + f'Email {extra_email.value} has been successfully added!\n' + TEXT_COLOR['reset'])

    def change_email(self, some_email, different_email):
        try:
            flag = False
            if different_email.value != None:
                for em in self.emails:
                    if em.value == some_email.value:
                        self.emails.remove(em)
                        self.emails.append(different_email)
                        print(TEXT_COLOR['green'] + f'Email {some_email.value} has been successfully changed to {different_email.value}\n' + TEXT_COLOR['reset'])
                        flag = True
            else:
                flag = True
        except AttributeError:
            flag == False

        if flag == False:
                print(TEXT_COLOR['red'] + f'There is no such email as {some_email.value}\n' + TEXT_COLOR['reset'])

    def delete_email(self, some_email):
        flag = False
        try:
            for em in self.emails:
                if em.value == some_email.value:
                    self.emails.remove(em)
                    flag = True
                    print(TEXT_COLOR['green'] + f'Email {some_email.value} has been successfully deleted\n' + TEXT_COLOR['reset'])
        except AttributeError:
            flag == False

        if flag == False:
                print(TEXT_COLOR['red'] + f'There is no such email as {some_email.value}\n' + TEXT_COLOR['reset'])

    # Birthday operations
    def days_to_birthday(self):
        try:
            self.birthday.value
            bd = datetime(year=datetime.now().year, month=self.birthday.value.month, day=self.birthday.value.day)
            delta = bd - datetime.now()
            if delta.days < 0:
                delta = datetime(year=datetime.now().year+1, month=self.birthday.value.month, day=self.birthday.value.day) - datetime.now()
            return delta.days+1
        except AttributeError:
            pass
    
    def add_birthday(self, extra_birthday):
        self.birthday = extra_birthday
        print(TEXT_COLOR['green'] + f'Birthday {extra_birthday.value.date()} has been successfully added!\n' + TEXT_COLOR['reset'])

    def change_birthday(self, some_bd, different_bd):
        flag = False
        try:
            if self.birthday.value == some_bd.value:
                self.birthday = different_bd
                print(TEXT_COLOR['green'] + f'Birthday {some_bd.value.date()} has been successfully changed to {different_bd.value.date()}\n' + TEXT_COLOR['reset'])
                flag = True
        except AttributeError:
            flag == False

        if flag == False:
                print(TEXT_COLOR['red'] + f'There is no such birthday as {some_bd.value.date()}\n' + TEXT_COLOR['reset'])
    
    def delete_birthday(self, some_bd):
        flag = False
        try:
            if self.birthday.value == some_bd.value:
                self.birthday = None
                flag = True
                print(TEXT_COLOR['green'] + f'Birthday {some_bd.value.date()} has been successfully deleted\n' + TEXT_COLOR['reset'])
        except AttributeError:
            flag == False
        
        if flag == False:
            print(TEXT_COLOR['red'] + f'There is no such birthday as {some_bd.value.date()}\n' + TEXT_COLOR['reset'])
    
    #Address operations
    def add_address(self, new_address):
        self.address = new_address
        print(TEXT_COLOR['green'] + f'Address \n{new_address.value} \nhas been successfully added!\n' + TEXT_COLOR['reset'])

   
    def change_address(self, old_adr, new_adr):
        flag = False
        try:
            if self.address.value == old_adr.value:
                self.address = new_adr
                print(TEXT_COLOR['green'] + f'Address \n{old_adr.value} \nhas been successfully changed to \n{new_adr.value}\n' + TEXT_COLOR['reset'])
                flag = True
        except AttributeError:
            flag == False
        
        if flag == False:
            print(TEXT_COLOR['red'] + f'There is no such address as \n{old_adr.value}\n' + TEXT_COLOR['reset'])

    def delete_address(self, some_adr):
        flag = False
        try:
            if self.address.value == some_adr.value:
                self.address = None
                flag = True
                print(TEXT_COLOR['green'] + f'Address \n{some_adr.value} \nhas been successfully deleted\n' + TEXT_COLOR['reset'])
        except AttributeError:
            flag == False
        
        if flag == False:
            print(TEXT_COLOR['red'] + f'There is no such address as \n{some_adr.value}\n' + TEXT_COLOR['reset'])

    def __str__(self):
        result = f'\nName: {self.name.value}\n'
        try:
            p = list(x.value for x in self.phones if x.value != None)
            if len(p) > 0:
                result += f'Phones: {p}\n'
        except AttributeError:
            pass

        try:
            e = list(x.value for x in self.emails)
            if len(e) > 0:
                result += f'Emails: {e}\n'
        except AttributeError:
            pass

        try:
            result += f'Birthday: {self.birthday.value.date()}'
            result += f'\nDays to next birthday: {str(self.ab[self.name.value].days_to_birthday())}\n'
        except AttributeError:
            pass

        try:
            if self.address.value != None:
                result += f'{self.address.value}\n'
        except AttributeError:
            pass 

        return result


class AddressBook(UserDict):
    def add_record(self, record):
        try:
            self.data[record.name.value] = record
            print(TEXT_COLOR['green'] + f'One contact ({record.name.value}) has been successfully added!\n' + TEXT_COLOR['reset'])
        except AttributeError:
            print(TEXT_COLOR['red'] + 'The contact has to be named!\n' + TEXT_COLOR['reset'])

    def delete_record(self, name_to_delete):
        for username in self.data.keys():
            if username == name_to_delete:
                del self.data[username]
                print(TEXT_COLOR['green'] + f'Contact ({username}) has been deleted successfully!\n' + TEXT_COLOR['reset'])
                return None
            
        print(TEXT_COLOR['red'] + f'There is no such contact as {name_to_delete}\n' + TEXT_COLOR['reset'])
    
    def clear_data(self):
        self.data.clear()
        print(TEXT_COLOR['green'] + '\nYour addressbook was cleared successfully!\n' + TEXT_COLOR['reset'])

    def find_contact(self, inp):
        def inner_find(inp, rec):
            for attr in rec.__dict__.values():
                try:
                    if attr.value != None and inp in str(attr.value):
                        result = str(rec)
                        return result
                except AttributeError:
                    try:
                        for i in attr:
                            if i.value != None and inp in str(i.value):
                                result = str(rec)
                                return result
                    except AttributeError:
                        pass
                    except TypeError:
                        pass
            return ''

        result = ''

        for rec in self.data.values():
            result += inner_find(inp, rec)
            
        if len(result) > 0:
            print(result)
        else:
            print(TEXT_COLOR['red'] + f"Nothing was found by '{inp}'\n" + TEXT_COLOR['reset'])
    
    # Autosave functions
    def load_from_file(self, file):
        try:
            with open(file, "rb") as fh:
                self.data = pickle.load(fh)
        except:
            return "The file with saved addressbook not found, corrupted or empty."

    def save_to_file(self, file):
        with open(file, "wb") as fh:
            pickle.dump(self.data, fh)

    current_index = 0

    def __next__(self):
        records = self.data
        if self.current_index < len(records):
            self.current_index += 1
            result = list(enumerate(self))
            return self.data[result[self.current_index-1][1]]
        print(TEXT_COLOR['green'] + 'Here is the end of your address book!\n' + TEXT_COLOR['reset'])
        self.current_index = 0
        raise StopIteration

    def __str__(self):
        result = ''
        for rec in self.data.values():
            result += str(rec)
        return result