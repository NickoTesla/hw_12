import json

from datetime import date
from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def validate(self, value):
        if not value:
            return False
        return True


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError('Invalid phone number')
        self.__value = value


phone = Phone('0998765656')
print(phone.value)
try:
    phone.value = "dfsgsg"
except ValueError as e:
    print(e)

print(phone.value)


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate(value)

    def validate(self, value):
        super().validate(value)
        try:
            date.fromisoformat(value)
        except ValueError:
            raise ValueError('Invalid date format')

    def __set__(self, instance, value):
        try:
            self.validate(value)
            self._

    def __get__(self, instance, owner):
        return self._value


@property
def value(self):
        return self._value


@value.setter
def value(self, value):
        self.validate(value)
        self._value = value


class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = name
        self.birthday = birthday
        self.phones = []
        if phone:
            self.add_phone(phone)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if str(p) != phone]

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                break

    def days_to_birthday(self):
       if self.birthday is None:
            return None
        today = date.today()
        birthday = self.birthday.replace(year=today.year)
        if birthday < today:
            birthday = birthday.replace(year=today.year + 1)
        delta = birthday - today
        return delta.days

class AddressBook:
    def __init__(self):
        self.contacts = {}

    def add_contact(self, contact):
        self.contacts[contact.name.lower()] = contact

    def remove_contact(self, name):
        del self.contacts[name.lower()]

    def edit_contact(self, name, contact):
        self.contacts[name.lower()] = contact

    def save_to_file(self, file_path):
        with open(file_path, 'w') as f:
            json.dump(self.contacts, f)

    def load_from_file(self, file_path):
        with open(file_path, 'r') as f:
            self.contacts = {c['name'].lower(): Contact(**c) for c in json.load(f)}

    def search_contacts(self, query):
        results = []
        for contact in self.contacts.values():
            if query.lower() in contact.name.lower() or query in contact.phone:
                results.append(contact)
        return results

contacts = AddressBook()


def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except KeyError:
            return "Contact not found"
        except ValueError:
            return "Enter name and phone number separated by a space"
        except IndexError:
            return "Enter a contact name"
    return wrapper


@input_error
def add_contact(command):
    name, phone = command.split()
    contacts.add_record(Record(name, phone))
    return f"Contact {name} added"


@input_error
def change_contact(command):
    name, phone = command.split()
    record = contacts.data[name.lower()]
    record.edit_phone(phone)
    contacts.edit_record(name, record)
    return f"Phone number for {name} changed"


@input_error
def get_phone(command):
    name = command.lower()
    record = contacts.data[name]
    phones = ", ".join(str(phone) for phone in record.phones)
    return f"Phone number(s) for {name}: {phones}"


def show_all():
    if not contacts:
        return "No contacts found"
    result = "Contacts:\n"
    for record in contacts.values():
        phones = ", ".join(str(phone) for phone in record.phones)
        result += f"{record.name}: {phones}\n"
    return result


def main():
    while True:
        command = input("Enter command: ")
        command = command.lower()
        if command == "hello":
            print("How can I help you?")
        elif command.startswith("add"):
            print(add_contact(command[4:].strip()))
        elif command.startswith("change"):
            print(change_contact(command[7:].strip()))
        elif command.startswith("phone"):
            print(get_phone(command[6:].strip()))
        elif command == "show all":
            print(show_all())
        elif command in ["good bye", "close", "exit"]:
            print("Good bye!")
            break
        else:
            print("Unknown command")


if __name__ == "__main__":
    main()