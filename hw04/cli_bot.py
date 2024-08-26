import functools
from typing import Callable, List

CONTACT_NOT_FOUND = "Contact not found."
THERE_ARE_NO_CONTACTS = "There are no contacts."


def handle_general_errors(
    func: Callable[[str], List[str]]
) -> Callable[[str], List[str]]:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    return wrapper


def input_error(func: Callable[[str], List[str]]) -> Callable[[str], List[str]]:
    @functools.wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            print(
                f"Enter the argument for the command, please. Invalid value error: {e}"
            )
        except IndexError as e:
            print(
                f"Enter the argument for the command, please. Invalid index error: {e}"
            )
        except KeyError as e:
            print(f"Invalid input: {e}")

    return inner


@handle_general_errors
@input_error
def find_phone(name: str, contacts: dict[str, str]) -> str:
    phone = contacts.get(name)
    if not phone:
        return None
    return phone


@handle_general_errors
@input_error
def parse_input(user_input: str) -> tuple[str, list[str]]:
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@handle_general_errors
@input_error
def add_contact(args: tuple[str, str], contacts: dict[str, str]) -> str:
    name, phone = args
    contacts[name] = phone
    return "Contact added."


@handle_general_errors
@input_error
def change_contact(args: list[str], contacts: dict[str, str]) -> str:
    name, phone = args
    old_phone = find_phone(name, contacts)
    if not old_phone:
        return CONTACT_NOT_FOUND
    contacts[name] = phone
    return "Contact updated." or f"Contact {name} not found."


@handle_general_errors
@input_error
def show_phone(args: list[str], contacts: dict[str, str]) -> str:
    name = args[0]
    phone = find_phone(name, contacts)
    if not phone:
        return CONTACT_NOT_FOUND
    return phone


@handle_general_errors
@input_error
def show_all(contacts: dict[str, str]) -> None:
    if not contacts:
        print(THERE_ARE_NO_CONTACTS)
        return
    for name, phone_number in contacts.items():
        print(f"{name}\t{phone_number}")


def main():
    contacts = {}
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "show":
            show_all(contacts)
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()


# test_data = [
#     # Basic commands
#     ("hello", "How can I help you?"),
#     ("show", "There are no contacts in the dictionary."),  # Empty contacts
#     ("exit", "Good bye!"),

#     # Add contact
#     ("add Alice 1234567890", "Contact added."),
#     ("add Bob 9876543210", "Contact added."),

#     # Change contact
#     ("change Alice 9999999999", "Contact changed."),  # Successful change
#     ("change Charlie 1234567890", "Contact not found."),  # Non-existent contact

#     # Phone contact
#     ("phone Alice", "1234567890"),
#     ("phone Charlie", "Contact not found."),

#     # Show contacts
#     ("show", "Alice\t1234567890\nBob\t9999999999"),

#     # Invalid commands
#     ("invalid_command", "Invalid command."),
#     ("add Alice", "Invalid input: not enough arguments"),
#     ("change", "Invalid input: not enough arguments"),
#     ("phone", "Invalid input: not enough arguments"),
# ]
