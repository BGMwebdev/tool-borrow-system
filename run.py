import gspread
from google.oauth2.service_account import Credentials
import time
import os


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('tool_data_list')

members = SHEET.worksheet('members')

DIVIDER = '-' * 50


def clear_console():
    """
    This will clear the console
    """
    os.system('clear')


def welcome():
    """
    Provides a welcome message when program starts running
    """
    print('')
    print(DIVIDER)
    print('')
    print(('Welcome to Tools for borrow').upper())
    print('')
    print(('The place for you to borrow tools from your neighbours').upper())
    print('')
    print(DIVIDER)
    print('')


def explanation():
    """
    Provides an explanation for how to use the application and what to expect
    """
    time.sleep(2)
    print("To use this application, you first need to register.")
    print("After registration you'll be asked to log in.")
    print("when you are already registered, just log in!")
    print('')
    print("After that you can choose to search a tool.")
    print("Or you can choose to add a tool.")
    print('')
    print("First things first...")
    print('')
    time.sleep(1)


def start_menu():
    """
    Presents two options, to register or to log in.
    Detects if one out of two options is given
    """
    time.sleep(1)
    print("Please select one of the options and press enter: ")
    menu_options = "1) Register\n2) Log in\n"
    menu_selected = input(menu_options)
    print('')

    # This will validate the answer and check if 1 or 2 is choosen
    while menu_selected not in ('1', '2'):
        print("Please choose option '1' or '2':")
        menu_selected = input(menu_options)
        print('')

    if menu_selected == "1":
        print("You choose to register.")
        print("Loading...")
        time.sleep(2)
        clear_console()
        registration()

    elif menu_selected == "2":
        print("You choose to log in.")
        print("Loading...")
        time.sleep(1)
        clear_console()
        log_in_main()


def registration():
    """
    Registers a resident by asking for data input
    like first name, last name and phone number.
    """
    while 'n':
        time.sleep(1)
        print("When entering your name, do not use digits or spaces")
        fname = input("Please enter your first name:\n")
        # This will make sure to have only letters in the name
        while fname.isalpha() is False:
            print("Do not use numbers or spaces!")
            print(f"Only letters are required, you provided: {fname}")
            print('')
            fname = input("Please enter your first name again:\n")

        upd_fname = name_correct(fname)
        print(f"Hi {upd_fname}!")
        print('')
        time.sleep(1)

        print("When entering your name, do not use digits or spaces")
        lname = input("What is your last name?\n")
        # This will make sure to have only letters in the name
        while lname.isalpha() is False:
            print("Only letters are required, do not use digits or spaces")
            print(f"you provided: {lname}")
            print('')
            lname = input("Please enter your last name again:\n")

        upd_lname = name_correct(lname)
        print("Registering...")
        print('')
        time.sleep(1)

        phone = str(input("Please enter you phone number:\n"))
        while phone.isdigit() is False:
            print("Only digits are required, no letters or spaces.")
            print(f"you provided: {phone}")
            print('')
            phone = input("Please enter your phone number again:\n")

        print("we now have you registered as:")
        print(f"{upd_fname} {upd_lname} {phone}")
        time.sleep(1)
        correct = input("Is that correct? 'y' for yes or 'n' for no:\n")

        # This will make sure one of the two options is chosen
        while correct not in ('n', 'y'):
            print('')
            print(f"'y' or 'n' is requirred, you provided {correct}.")
            time.sleep(1)
            correct = input("'y' for yes or 'n' for no:\n")

        if correct == 'n':
            print('')
            print("Let's try that again!")

        elif correct == 'y':
            print('')
            print("Great! We're almost there...\n")
            time.sleep(2)
            clear_console()
            password = create_psswd()
            break
    # This will create a list out of the input for the worksheet
    reg = f'{upd_fname} ' + f'{upd_lname} ' + f'{phone} ' + f'{password}'
    input_list = reg.split(" ")
    update_member_worksheet(input_list)


def name_correct(data):
    """
    Capitalize names before going into the spreadsheet
    """
    name_corr = (data).capitalize()
    return name_corr


def update_member_worksheet(data):
    """
    This will update the members worksheet
    in the google spreadsheet, and add a new row
    to the list
    """
    print("Updating members list...\n")
    members_worksheet = SHEET.worksheet("members")
    members_worksheet.append_row(data)
    time.sleep(1)
    print("Member registration completed!")
    print('')
    print("You are now ready to log in!")
    time.sleep(2)
    clear_console()
    log_in_main()


def create_psswd():
    """
    Print restrictions and present input for a unique password.
    """
    time.sleep(1)
    print("To be able to log in, you need to create a unique password.")
    print('')
    time.sleep(1)
    print("Your password should have at least 6 characters")
    print("At least 1 uppercase")
    print("At least 1 lowercase")
    print("At least 1 digit")
    print("And no spaces")
    print('')
    while True:
        time.sleep(2)
        password = input("please enter your unique password:\n")
        if password_check(password):
            print("Password is valid\n")
            time.sleep(2)
            return password
            break


def password_check(password):
    """
    Check if password is valid within the restrictions given
    using length, uppercase, lowercase and isdigit
    """
    val = True

    if len(password) < 6:
        print('length should be at least 6')
        val = False

    if not any(char.isupper() for char in password):
        print('Password should have at least one uppercase letter')
        val = False

    if not any(char.islower() for char in password):
        print('Password should have at least one lowercase letter')
        val = False

    if not any(char.isdigit() for char in password):
        print('Password should have at least one digit')
        val = False

    if val:
        return val


def name_row_number():
    """
    With a for loop through the list from the srpeadsheet
    the row number of the name input is returned
    """
    while True:
        user_lname = input('Enter your last name: \n').capitalize()
        login_names = members.col_values(2)
        lname_row_number = 1
        for x in login_names:
            if x == user_lname:
                print("Your name has been found.")
                return lname_row_number
                list_psswd_check(lname_row_number)
            lname_row_number += 1
        print("The name you gave is not found!")
        menu_options = "1) Try again\n2) Start menu\n"
        menu_selected = input(menu_options)
        print('')
        # This will validate the answer and check if 1 or 2 is choosen
        while menu_selected not in ('1', '2'):
            print("Please choose option '1' or '2':")
            menu_selected = input(menu_options)
            print('')

        if menu_selected == "1":
            print("You choose try again.")
            print("Loading...")
            time.sleep(1)
            continue

        elif menu_selected == "2":
            print("You choose start menu.")
            print("Start menu loading...")
            time.sleep(1)
            clear_console()
            start_menu()


def list_psswd_check(lname_row_number):
    """
    Returns list of values of specific row
    """
    login_list = members.row_values(lname_row_number)
    return login_list


def password_val(list_psswd):
    """
    Password check
    """
    while True:
        input_psswd = input("\nPlease enter your unique password: \n")
        if input_psswd == list_psswd[3]:
            time.sleep(1)
            print("\nYour password is correct.")
            time.sleep(1)
            clear_console()
            break
        else:
            time.sleep(1)
            print("\nYour password is incorrect.")


def log_in_main():
    """
    Main login function goes through the needed login functions
    """
    row_num = name_row_number()
    list_psswd = list_psswd_check(row_num)
    password_val(list_psswd)


def main_menu():
    """
    Presents three options
    to add a tool, to search for a tool or to exit
    makes sure one is chosen
    """
    clear_console()
    time.sleep(1)
    print("Welcome to the main menu!")
    print("Please select one of the options and press enter: ")
    menu_options = "1) Add a tool\n2) Search for a tool\n3) Exit\n"
    menu_selected = input(menu_options)
    print('')

    # This will validate the answer and check if 1 or 2 is choosen
    while menu_selected not in ('1', '2', '3'):
        print("Please choose option '1', '2' or '3':")
        menu_selected = input(menu_options)
        print('')

    if menu_selected == "1":
        print("You choose to add a tool.")
        print("Loading...")
        time.sleep(1)
        clear_console()
        add_tool()

    elif menu_selected == "2":
        print("You choose to search for a tool.")
        print("Loading...")
        time.sleep(1)
        clear_console()
        search_for_tool()

    elif menu_selected == "3":
        print("You choose to exit.")
        print("Thank you for visiting!!")
        time.sleep(1)
        clear_console()


def row_number():
    """
    With a for loop the row number is returned
    that corresponds to the name input given
    """
    while True:
        user_lname = input('Enter your last name again: \n').capitalize()
        member_names = members.col_values(2)
        lname_row_number = 1
        for x in member_names:
            if x == user_lname:
                print("Thank you")
                return lname_row_number
                list_psswd_check(lname_row_number)
            lname_row_number += 1
        print("The name you gave was not found!")
        menu_options = "1) Try again\n2) main menu\n"
        menu_selected = input(menu_options)
        print('')
        # This will validate the answer and check if 1 or 2 is choosen
        while menu_selected not in ('1', '2'):
            print("Please choose option '1' or '2':")
            menu_selected = input(menu_options)
            print('')

        if menu_selected == "1":
            print("You choose try again.")
            print("Loading...")
            time.sleep(1)
            continue

        elif menu_selected == "2":
            print("You choose main menu.")
            print("Main menu loading...")
            time.sleep(1)
            clear_console()
            main_menu()


def list_member_tools(lname_row_number):
    """
    With the row number as parameter the members information is returned
    as a list of strings
    """
    member_list = members.row_values(lname_row_number)
    return member_list


def add_tool_to_list(member_list):
    """
    Adds the given tool input to the list returned from list_member_tools
    """
    print("\nWhat tool would you like to add?")
    print("Please use the right name for the tool,")
    print("your neighbours will look for the tool by name.\n")
    tool_name = input("Enter tool name: \n")
    if len(member_list) <= 11:
        member_list.append(tool_name)
        return member_list
    else:
        print("Maximum number of tools in list reached!\n")
        print("You're being redirected to the main menu...")
        time.sleep(2)
        main_menu()


def update_member_row(lname_row_number, member_list):
    """
    Updates the specific row pertaining to the logged in member
    """
    members.update(f"A{lname_row_number}:z{lname_row_number}", [member_list])
    print("Adding tool to member list...\n")


def return_overview_tools(lname_row_number):
    """
    Print overview of tools present in specific list spreadsheet
    """
    tools_list = members.row_values(lname_row_number)
    print("Here is an overview of your tools:")
    for i in tools_list[4:]:
        print(i)
    time.sleep(2)
    print("\nWhen you're ready, please select one of the options: ")
    menu_options = "1) Back to main menu\n2) Exit\n"
    menu_selected = input(menu_options)
    print('')

    # This will validate the answer and check if 1 or 2 is choosen
    while menu_selected not in ('1', '2'):
        print("Please choose option '1' or '2':")
        menu_selected = input(menu_options)
        print('')

    if menu_selected == "1":
        print("You choose back to main menu.")
        print("Loading...")
        time.sleep(1)
        main_menu()

    elif menu_selected == "2":
        print("You choose to exit.")
        print("Thank you for visiting!!")
        time.sleep(1)
        clear_console()


def add_tool():
    """
    Main add tool function, will go through the different function
    to add a tool to the spreadsheet
    """
    right_row = row_number()
    list_tools = list_member_tools(right_row)
    member_list = add_tool_to_list(list_tools)
    update_member_row(right_row, member_list)
    return_overview_tools(right_row)


def search_for_tool():
    """
    Find corresponding tool in data, returns validation and 
    name and number of neighbour in possession
    """
    while True:
        search_input = input("What tool are you looking for?\n")
        if members.find(search_input):
            result_row = members.find(search_input).row
            match_list = members.row_values(result_row)
            print()
            print("You're in luck!!")
            print(f"We've found the {search_input} you're looking for!")
            print(f"Your neighbour is: {match_list[0]} {match_list[1]}")
            print(f"You can reach them on: {match_list[2]}")
            break
        else:
            print("\nNo match found!")
            print("Would you like to do another search?")
            menu_options = "1) yes\n2) no\n"
            menu_selected = input(menu_options)
            print('')

            # This will validate the answer and check if 1 or 2 is choosen
            while menu_selected not in ('1', '2'):
                print("Please choose option '1' or '2':")
                menu_selected = input(menu_options)
                print('')

            if menu_selected == "1":
                print("You choose to search for another tool.")
                print("Loading...")
                time.sleep(1)
                search_for_tool()

            elif menu_selected == "2":
                print("You choose no.")
                break

    time.sleep(2)
    print("\nWhen you're ready, please select one of the options: ")
    menu_options = "1) Search another tool\n2) Back to main menu\n3) Exit\n"
    menu_selected = input(menu_options)
    print('')

    # This will validate the answer and check if 1 or 2 is choosen
    while menu_selected not in ('1', '2', '3'):
        print("Please choose option '1', '2' or '3':")
        menu_selected = input(menu_options)
        print('')

    if menu_selected == "1":
        print("You choose to search for another tool.")
        print("Loading...")
        time.sleep(1)
        search_for_tool()

    elif menu_selected == "2":
        print("You choose to go back to main menu.")
        print("Loading...")
        time.sleep(1)
        main_menu()

    elif menu_selected == "3":
        print("You choose to exit.")
        print("Thank you for visiting!!")
        time.sleep(1)
        clear_console()


def main():
    """
    This is the main function, that will run the application
    """
    welcome()
    explanation()
    start_menu() 
    main_menu()


main()
