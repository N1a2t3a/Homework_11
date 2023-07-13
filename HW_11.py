from collections import UserDict
from datetime import datetime

class Phone:
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, number):
        if not isinstance(number, str):
            raise ValueError("Phone number must be a string")

        # Перевірка на коректність введеного номера телефону
        if not number.isdigit():
            raise ValueError("Phone number can only contain digits")

        self._value = number

class Birthday:
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, date):
        if date is not None and not isinstance(date, datetime):
            raise ValueError("Birthday must be a datetime object")

        # Перевірка на коректність введеного дня народження
        if date is not None and date > datetime.now():
            raise ValueError("Birthday cannot be in the future")

        self._value = date

    def days_to_birthday(self):
        if self.value is None:
            return None

        today = datetime.now()
        next_birthday = datetime(today.year, self.value.month, self.value.day)

        if today > next_birthday:
            next_birthday = datetime(today.year + 1, self.value.month, self.value.day)

        days_left = (next_birthday - today).days
        return days_left

class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = name
        self.fields = []
        if phone is not None:
            self.add_field(phone)
        if birthday is not None:
            self.add_field(birthday)

    def add_field(self, field):
        self.fields.append(field)

    def remove_field(self, field):
        self.fields.remove(field)

    def edit_field(self, field, new_value):
        field.value = new_value

    def matches_criteria(self, criteria):
        for field in self.fields:
            if field.matches_criteria(criteria):
                return True
        return False

class Field:
    def __init__(self, value):
        self.value = value

    def matches_criteria(self, criteria):
        return str(self.value).lower() == str(criteria).lower()

class Name(Field):
    pass

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def search(self, criteria):
        results = []
        for record in self.data.values():
            if record.matches_criteria(criteria):
                results.append(record)
        return results

    def iterator(self, n):
        if n <= 0:
            raise ValueError("Invalid iterator step size")

        start = 0
        while start < len(self.data):
            yield list(self.data.values())[start:start+n]
            start += n

def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except KeyError:
            return "Contact not found."
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Invalid input. Please enter name and phone number separated by a space."

    return inner

address_book = AddressBook()

@input_error
def add_contact(contact_info):
    name, phone = contact_info.split(' ')
    name_field = Name(name)
    phone_field = Phone(phone)
    record = Record(name_field, phone_field)
    address_book.add_record(record)
    return "Contact added successfully."

@input_error
def change_phone(contact_info):
    name, phone = contact_info.split(' ')
    record = address_book.data.get(name)
    if record:
        phone_field = record.fields[0]
        phone_field.value = phone
        return "Phone number updated successfully."
    else:
        raise KeyError

@input_error
def show_phone(name):
    record = address_book.data.get(name)
    if record:
        phone_field = record.fields[0]
        return phone_field.value
    else:
        raise KeyError

def show_all_contacts():
    if len(address_book.data) == 0:
        return "No contacts found."
    else:
        return "\n".join([f"{name}: {record.fields[0].value}" for name, record in address_book.data.items()])

def command_parser(command):
    command = command.strip()

    if command == "hello":
        return "How can I help you?"
    elif command.startswith("add"):
        contact_info = command[4:]
        return add_contact(contact_info)
    elif command.startswith("change"):
        contact_info = command[7:]
        return change_phone(contact_info)
    elif command.startswith("phone"):
        name = command[6:]
        return show_phone(name)
    elif command == "show all":
        return show_all_contacts()
    else:
        return "Invalid command. Please try again."

def process_command(command):
    if command in ["good bye", "close", "exit"]:
        print("Good bye!")
        return False

    result = command_parser(command)
    print(result)
    return True

def main():
    print("How can I help you?")
    while True:
        command = input("> ")
        if not process_command(command):
            break

if __name__ == "__main__":
    main()