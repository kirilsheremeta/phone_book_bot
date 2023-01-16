PHONE_DICT = {}


HELP_DESK = """Main commands:              
                'add'/'create' to create new contact.
                After this command you need to input name
                of your new contact and his and phone number.

                Example: add Peter 0931234567
                         create Bob +38(097)123-45-67
                         add Bill (098)9876543
                
                'change'/'upgrade' to update a phone number.
                After this command you need to input name
                of contact, his old and new phone numbers.

                Example: change Peter 093-123-45-67 067-765-43-21

                'delete'/'remove' to delete contact

                Example: delete Peter
                
                'phone'/'show' to show information about contact.
                After this command you need to input name
                of your contact.
                
                Example: phone Peter
                
                'show all'/'all' to show all your contacts and their phone numbers.

                Example: show all
                
                'exit'/'quit'/'good bye'/'close' to turn me off.
                
                Example: good bye
                """


def beginning():
    print("Hi, I'm a Phone Bot. Enter 'hello' to start or 'help' to see all my commands")

beginning()


# Exception handling decorator


def error_exception(func):
    def wrapper(*args):
        try:
            return func(*args)
        except ValueError:
            return "Try again. Enter your contacts name"
        except KeyError:
            return "Try again. Enter correct name"
        except IndexError:
            return "Try again. Enter correct name and phone number"
        except TypeError:
            return "I don't have enough parameters to execute the command. Please try again"
    return wrapper


def main():
    while True:
        user_input = str(input(">>> "))
        result = start_bot(user_input)
        print(result)


# Phone number filter

def filter_number(phone):
    new_number = (
        phone.strip()
        .removeprefix("+")
        .replace(" ", "")
        .replace("-", "")
        .replace("(", "")
        .replace(")", "")
    )
    return new_number


def hello_user(*args):
    return "How can I help you?"


def bye_user(*args):
    while True:
        return "Good bye. See you next time"


def help_user(*args):
    return HELP_DESK


# Create new contact
@error_exception
def add_contact(*args):
    print(args)
    name = args[0]
    phone = args[1]
    if name not in PHONE_DICT:
        PHONE_DICT[name] = []
        PHONE_DICT[name].append(filter_number(phone))

    elif name in PHONE_DICT:
        PHONE_DICT[name].append(filter_number(phone))

    return f"Added new contact - {name} {filter_number(phone)}"


# Delete contact
@error_exception
def delete_contact(name):
    if name in PHONE_DICT:
        del PHONE_DICT[name]
        return f"{name} has successfully deleted"
    else:
        return f"{name} is not found. Please try again"


# Upgrading the old number to the new number
@error_exception
def upgrade_number(name: str, old_num: str, new_num):
    if name in PHONE_DICT:
        PHONE_DICT[name].remove(filter_number(old_num))
        PHONE_DICT[name].append(filter_number(new_num))
        return f"{name}'s number {filter_number(old_num)} upgrated to {filter_number(new_num)}"
    else:
        return f"{name} is not found. Please try again"


# Show information about contact
@error_exception
def show_number(name):
    if name in PHONE_DICT:
        return f"Name: {name} Phone: {PHONE_DICT.get(name)}"
    else:
        return f"{name} is not found. Please try again"


# Show all contacts
@error_exception
def show_all(*args):
    contact_info = ""
    for user_name, phone_list in PHONE_DICT.items():
        phone_numbers = ""
        for i in phone_list:
            phone_numbers += i + " "
        contact_info += ''.join(user_name +
                                ": " + phone_numbers + '\n')

    return contact_info


COMMANDS = {hello_user: ['hello', 'hi'],
            show_all: ['show all', 'all'],
            show_number: ['phone', 'show'],
            add_contact: ['add', 'create'],
            upgrade_number: ['change', 'upgrade'],
            delete_contact: ['delete', 'remove'],
            help_user: ['help'],
            bye_user: ['exit', 'quit', 'good bye', 'close', 'bye']
            }


def parse_command(text: str):
    for commands, key_words in COMMANDS.items():
        for key_word in key_words:
            if text.startswith(key_word):
                return commands, text.replace(key_word, '').strip().split(' ')
    return None, None


# Interaction with the user
def start_bot(user_input):
    command, data = parse_command(user_input)
    if not command:
        return "Incorrect input. Please try again"
    return (command(*data))


if __name__ == "__main__":
    main()
