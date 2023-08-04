#Додаємо новий клас для адрес
class Address:
    def __init__(self):
        self.city = None
        self.street = None
        self.house = None
        self.apartment = None

    def input_address(self):
        self.city = input("Enter city: ")
        self.street = input("Enter street: ")
        self.house = input("Enter house number: ")
        self.apartment = input("Enter apartment number: ")

    def __str__(self):
        address_parts = []
        if self.city:
            address_parts.append(self.city)
        if self.street:
            address_parts.append(self.street)
        if self.house:
            address_parts.append(self.house)
        if self.apartment:
            address_parts.append(self.apartment)
        return ', '.join(address_parts)

#Модифікації класу Record, щоб він також додавав і зберігав адреси
class Record:
    def __init__(self, person_name, phone_num=None, email=None, birthday=None, ab=None):
        self.ab = ab
        self.name = person_name
        self.address = None  # Поле для адреси

        if phone_num:
            self.phones = []
            self.phones.append(phone_num)

        if email:
            self.emails = []
            self.emails.append(email)

        if birthday:
            self.birthday = birthday

    #Adress operations
        def add_address(self):
        if not self.address:
            self.address = Address()
        self.address.input_address()
        print("Address added successfully!")

    def change_address(self):
        if self.address:
            self.address.input_address()
            print("Address modified successfully!")
        else:
            print("No address available.")

    def delete_address(self):
        self.address = None
        print("Address deleted.")

#Додати до функції main основну логіку
    commands = ["add_adress", "change_address", "delete_address"]
    if command == 'add address':
        record.add_address()
    elif command == 'change_address':
        record.modify_address()
    elif command == 'delete_address':
        record.delete_address()
    elif command == 'exit':
        break
    else:
        print(f"\nUnknown command ({command})\nInput 'commands' to see all the commands avalible!\nFor more information go to README.md\n")