import pickle
from collections import UserDict
from datetime import datetime


# Custom errors
class BirthdayError(Exception):
    pass


class PhoneError(Exception):
    pass


# Decorator
def error_keeper(function):
    def inner(*args):
        try:
            function(*args)
        except BirthdayError:
            print('That is incorrect birthday!')
        except PhoneError as pe:
            if pe.args:
                print(f'This phone number is too {pe.args[0]}!')
            else:
                print('That is incorrect phone number!')
        except ValueError:
            print('Something is wrong!\nGo to README.md to check the correctness\n')
        except AttributeError:
            print('Something is wrong!\nGo to README.md to check the correctness\n')
        except KeyError:
            print('Name is incorrect!\n')

    return inner


# Classes
class Field:
    def __init__(self, name=None, phone=None, email=None, birthday=None):
        if name:
            self.value = name
        if phone:
            self.__value = None
            self.value = phone
        if email:
            self.value = email
        if birthday:
            self.__value = None
            self.value = birthday


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
    pass


class Name(Field):
    pass


class Record:
    def __init__(self, person_name, phone_num=None, email=None, birthday=None, ab=None):
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
                print(f'Phone number {extra_phone.value} has been successfully added!\n')
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
                        print(f'Phone number {some_phone.value} has been successfully changed to {different_phone.value}\n')
                        flag = True
        except AttributeError:
            flag == False
        if flag == False:
            print(f'There is no such phone!')

    def delete_phone(self, some_phone):
        try:
            if some_phone.value != None:
                flag = False
                for ph in self.phones:
                    if ph.value == some_phone.value:
                        self.phones.remove(ph)
                        flag = True
                        print(f'Phone number {some_phone.value} has been successfully deleted\n')
        except AttributeError:
            flag = False
            
        if flag == False:
            print(f'There is no such phone as {some_phone.value}\n')

    # Email operations
    def add_email(self, extra_email):
        try:
            self.emails.append(extra_email)
            for x in self.emails:
                x.value
        except AttributeError:
            self.emails = []
            self.emails.append(extra_email)

        print(f'Email {extra_email.value} has been successfully added!\n')

    def change_email(self, some_email, different_email):
        flag = False
        try:
            for em in self.emails:
                if em.value == some_email.value:
                    self.emails.remove(em)
                    self.emails.append(different_email)
                    print(f'Email {some_email.value} has been successfully changed to {different_email.value}\n')
                    flag = True
        except AttributeError:
            flag == False

        if flag == False:
                print(f'There is no such email as {some_email.value}\n')

    def delete_email(self, some_email):
        flag = False
        try:
            for em in self.emails:
                if em.value == some_email.value:
                    self.emails.remove(em)
                    flag = True
                    print(f'Email {some_email.value} has been successfully deleted\n')
        except AttributeError:
            flag == False

        if flag == False:
                print(f'There is no such email as {some_email.value}\n')

    # Birthday operations
    def days_to_birthday(self):
        self.birthday.value
        bd = datetime(year=datetime.now().year, month=self.birthday.value.month, day=self.birthday.value.day)
        delta = bd - datetime.now()
        if delta.days < 0:
            delta = datetime(year=datetime.now().year+1, month=self.birthday.value.month, day=self.birthday.value.day) - datetime.now()
        return delta.days+1
    
    def add_birthday(self, extra_birthday):
        self.birthday = extra_birthday
        print(f'Birthday {extra_birthday.value.date()} has been successfully added!\n')

    def change_birthday(self, some_bd, different_bd):
        flag = False
        try:
            if self.birthday.value == some_bd.value:
                self.birthday = different_bd
                print(f'Birthday {some_bd.value.date()} has been successfully changed to {different_bd.value.date()}\n')
                flag = True
        except AttributeError:
            flag == False

        if flag == False:
                print(f'There is no such birthday as {some_bd.value.date()}\n')
    
    def delete_birthday(self, some_bd):
        flag = False
        try:
            if self.birthday.value == some_bd.value:
                self.birthday = None
                flag = True
                print(f'Birthday {some_bd.value.date()} has been successfully deleted\n')
        except AttributeError:
            flag == False
        
        if flag == False:
            print(f'There is no such birthday as {some_bd.value.date()}\n')

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

        return result


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
        print(f'One contact ({record.name.value}) has been successfully added!\n')

    def delete_record(self, name_to_delete):
        for username in self.data.keys():
            if username == name_to_delete:
                del self.data[username]
                print(f'Contact ({username}) has been deleted successfully!\n')
                return None
            
        print(f'There is no such contact as {name_to_delete}\n')

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
            print(f"Nothing was found by '{inp}'\n")
    
    # Autosave functions
    def save_data(self):
        with open('ab_save.bin', 'wb') as f:
            pickle.dump(self.data, f)

    def load_data(self):
        try:
            with open('ab_save.bin', 'rb') as f:
                try:
                    self.data = pickle.load(f)
                except EOFError:
                    try:
                        self.data = pickle.loads(f)
                    except TypeError:
                        self.data = AddressBook()
                except TypeError:
                    self.data = AddressBook()

        except FileNotFoundError:
            with open('ab_save.bin', 'x'):
                pass
            self.load_data()

    current_index = 0

    def __next__(self):
        records = self.data
        if self.current_index < len(records):
            self.current_index += 1
            result = list(enumerate(self))
            return self.data[result[self.current_index-1][1]]
        print('Here is the end of your address book!\n')
        self.current_index = 0
        raise StopIteration

    def __str__(self):
        result = ''
        for rec in self.data.values():
            result += str(rec)
        return result