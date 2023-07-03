#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

def read_user_data():
    
    # If no user.txt file, write one with a default account
    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as default_file:

            default_file.write("admin;password")

    # Read in user_data
    with open("user.txt", 'r') as user_file:

        user_data = user_file.read().split("\n")

    # Convert to a dictionary
    username_password = {}
    for user in user_data:

        username, password = user.split(';')
        username_password[username] = password

    return username_password

def save_user_data(username_password):

    with open("user.txt", "w") as out_file:

        user_data = []
        for k in username_password:
            user_data.append(f"{k};{username_password[k]}")
        out_file.write("\n".join(user_data))

def reg_user():

    # - Request input of a new username
    while True:
            new_username = input("New Username: ") # Asks user to enter new username.

            if new_username in username_password: # Checks o see if the new username is already in the user data dictionary.
                print("That username is already taken. Please choose another.\n") # Error message.
                continue

            else:
                break # Only breaks loop if new username doesn't already exist in dictionary.

    # - Request input of a new password
    new_password = input("New Password: ")

    # - Request input of password confirmation.
    confirm_password = input("Confirm Password: ")

    # - Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        # - If they are the same, perform save_user_data function,
        username_password[new_username] = new_password

        # - Saves user data to user.text file
        save_user_data(username_password)
        print("New user added")

    # - Otherwise you present a relevant message.
    else:
        print("Passwords do not match")

def read_tasks():

    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w") as default_file:
            pass

    with open("tasks.txt", 'r') as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]

    task_list = []

    for t_str in task_data:
        curr_t = {}

        # Split by semicolon and manually add each component
        task_components = t_str.split(";")
        curr_t['username'] = task_components[0]
        curr_t['title'] = task_components[1]
        curr_t['description'] = task_components[2]
        curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
        curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
        curr_t['completed'] = True if task_components[5] == "Yes" else False

        task_list.append(curr_t)

    return task_list

def save_tasks(task_list):

    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []

        for t in task_list:

            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))

def add_task(username_password):
    ''' Allow a user to add a new task to task.txt file
            Prompt a user for the following: 
             - A username of the person whom the task is assigned to,
             - A title of a task,
             - A description of the task and 
             - the due date of the task.'''
    task_username = input("Name of person assigned to task: ")

    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return

    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")

    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")

     # Then get the current date.
    curr_date = date.today()
    ''' Add the data to the file task.txt and
            Include 'No' to indicate if the task is complete.'''
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)

    # - Saves task to tasks.txt file
    save_tasks(task_list)
    print("Task successfully added.")

def view_all(task_list):
    ''' Reads the task from task.txt file and prints to the console in the 
        format of Output 2 presented in the task pdf (i.e. includes spacing
        and labelling) 
    '''
    for t in task_list:

        disp_str = f"Task: \t\t\t {t['title']}\n"
        disp_str += f"Assigned to: \t\t {t['username']}\n"
        disp_str += f"Date Assigned: \t\t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t\t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Completed?: \t {t['completed']}\n" # Added task completed status.
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)

def view_mine(task_list, curr_user):
    ''' Reads the task from task.txt file and prints to the console in the 
        format of Output 2 presented in the task pdf (i.e. includes spacing
        and labelling)
    '''
    for index, t in enumerate(task_list, start = 1): # Starts index at 1.

        if t['username'] == curr_user:
            disp_str = print("\n[{}]".format(index)) # Prints task number in front a user's tasks.
            disp_str = f"Task: \t\t\t {t['title']}\n"
            disp_str += f"Assigned to: \t\t {t['username']}\n"
            disp_str += f"Date Assigned: \t\t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t\t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Completed?: \t {t['completed']}\n" # Added task completed status.
            disp_str += f"Task Description: \n {t['description']}\n"
            print(disp_str)         
    
    for index, t in enumerate(task_list, start = 1):

        while True: # Loops until user inputs valid input
            try:
                edit_task = int(input("Enter index number of task you wish to select (or enter -1 to return to main menu): "))
                index = edit_task - 1 # Takes one from the number input by user to match position in the the list

                print("\nSelected task: {}\n".format(t['title'])) # Displays the title of selected task.

                if edit_task == -1: # Brings user back to the menu if they input -1
                    return
                
                if 0 <= index < len(task_list): # Makes sure that the number entered by the user is valid number within the task list.
                    updated_task = task_list[index] # Used to update current selected task.
                    break

                else:
                    print("Invalid index number. Please try again.\n") # Displays error if the number input by user is not in the task list. Loops back to edit_task input.
                
            except ValueError:
                print("Invalid input. Please try again\n") # Displays error if user doesn't input an integer. Loops back to edit_task input.

        # User selects which task they wish to perform.
        edit_menu = input('''Select one of the following Options below:
    ve - Edit selected task
    c - Mark selected task as complete
    e - Return to main menu
    : ''').lower()
        
        if edit_menu == 've':
                
            if updated_task['completed'] == False: # If the task is currently incomplete.

                updated_user = input("\nEnter user to be assigned to this task: ") # User enters updated user.
                updated_due_date = input("Enter updated due date (YYYY-MM-DD): ") # User enters updated due date.

                # Updates the task with the updated information
                updated_task['username'] = updated_user
                updated_task['due_date'] = datetime.strptime(updated_due_date, DATETIME_STRING_FORMAT)

                # Saves the updated task to tasks.txt file
                save_tasks(task_list)
                print("Your task has been updated.")
                return
            
            elif updated_task['completed'] == True: # If the task is already complete.
                print("\nThe selected task cannot be edited because it has already been marked as complete.") # Informs user that the selected task has already been marked as complete.
                return

        elif edit_menu == 'c':

            if updated_task['completed'] == False:  # If the task is currently incomplete.

                updated_task['completed'] = True # Update task to be complete.
                
                # # Saves the updated completion status to tasks.txt file
                save_tasks(task_list)
                print("\nYour task has been marked as complete.")
                return
            
            else:
                print("\nThe selected task has already been marked as complete.") # Informs user that the selected task has already been marked as complete.
                return
            
        elif edit_menu == 'e':

            return # Return to main menu
        
        else:
            print("\nInvalid Input. Please try again.\n") # Displays error message if menu option isn't valid.

def task_overview(task_list):

    # Task overview report

    total_tasks = len(task_list) # Calls the length of the task list to calculate total number of tasks.

    complete_tasks = sum(1 for t in task_list if t['completed']) # Adds 1 for every task marked as complete.

    incomplete_tasks = total_tasks - complete_tasks # Calculates the number of incomplete tasks.

    overdue_tasks = sum(1 for t in task_list if not t['completed'] and t['due_date'] < datetime.now()) # Adds 1 for every task that is not complete and with a due date before current date and time.

    percentage_incomplete = (incomplete_tasks / total_tasks) * 100 # Calculates the percentage of tasks incomplete.
    
    percentage_overdue = (overdue_tasks / total_tasks) * 100 # Calculates the percentage of tasks overdue.

    with open("task_overview.txt", "w") as report_file:

        # Writes to task overview file

        report_file.write("[Task Overview]\n")
        report_file.write("\n")
        report_file.write(f"Total tasks: \t\t\t\t {total_tasks}\n")
        report_file.write(f"Completed tasks: \t\t\t {complete_tasks}\n")
        report_file.write(f"Tasks incomplete: \t\t\t {incomplete_tasks}\n")
        report_file.write(f"Tasks overdue: \t\t\t\t {overdue_tasks}\n")
        report_file.write(f"Percentage incomplete: \t\t {percentage_incomplete}%\n")
        report_file.write(f"Percentage overdue: \t\t {percentage_overdue}%\n")

def user_overview(task_list, username_password):

     # User overview repot

    total_users = len(username_password.keys()) 

    total_tasks = len(task_list) # Calls the length of the task list to calculate total number of tasks.

    with open("user_overview.txt", "w") as report_file:

        # Writes to user overview file

        report_file.write("[User Overview]\n")
        report_file.write("\n")
        report_file.write(f"Total number of users: \t {total_users}\n")
        report_file.write(f"Total tasks: \t\t\t {total_tasks}\n")

        for username in username_password:

            assigned_tasks = sum(1 for t in task_list if t['username'] == username) # Calculates the number of assigned tasks assigned current user.

            percentage_assigned = (assigned_tasks / total_tasks) * 100 # Calculates percentage of tasks assigned to current user.

            percentage_completed = sum(1 for t in task_list if t['username'] == username and t['completed']) / assigned_tasks * 100 # Adds 1 for every complete task belonging to current user, then calculates percentage of assigned tasks completed.

            percentage_incomplete = sum(1 for t in task_list if t['username'] == username and not t['completed']) / assigned_tasks * 100 # Adds 1 for every incomplete task belonging to current user, then calculates percentage of assigned tasks incomplete.

            percentage_overdue = sum(1 for t in task_list if t['username'] == username and not t['completed'] and t['due_date'] < datetime.now()) / assigned_tasks * 100 # Adds 1 for every incomplete and overdues task belonging to current user, then calculates percentage of tasks overdue

            # Writes to user overview file

            report_file.write(f"\nUsername: \t\t\t\t\t\t\t\t {username}\n")
            report_file.write(f"Assigned tasks: \t\t\t\t\t\t {assigned_tasks}\n")
            report_file.write(f"Tasks assigned to user (percentage): \t {percentage_assigned}%\n")
            report_file.write(f"Tasks completed (percentage): \t\t\t {percentage_completed}%\n")
            report_file.write(f"Tasks in progress (percentage): \t\t {percentage_incomplete}%\n")
            report_file.write(f"Tasks overdue (percentage): \t\t\t {percentage_overdue}%\n")

def gen_rep(task_list, username_password):

    task_overview(task_list)
    
    user_overview(task_list, username_password)
    
    print("\nA task overview report has successful been exported.")
    print("A user overview report has successful been exported.")

def view_stats(username_password, task_list):
    ''' If the user is an admin they can display statistics about number of users
            and tasks.'''

    task_overview(task_list) # Generates task_overview.txt file if one doesn't exist / updates current task_overview.txt file. 
    
    user_overview(task_list, username_password) # Generates user_overview.txt file if one doesn't exist / updates current user_overview.txt file.

    with open("task_overview.txt", "r") as task_stats, open("user_overview.txt", "r") as user_stats:

        view_task_stats = task_stats.readlines() # Reads data from task_overview.txt file.
        view_user_stats = user_stats.readlines() # Reads data from user_overview.txt file.

        print()
        print("----------------------------------------------------------")
        print("                        Statistics                        ") # Title
        print("----------------------------------------------------------") # Lines to break up text.
        print()

        # Task statistics formatting

        for line in view_task_stats:
            formatted_line = line.replace("\t", "") # removes tab spacing 
            if formatted_line:
                print(formatted_line.strip()) # removes white space between lines and prints data

        print()
        print("----------------------------------------------------------") # Seperates boths data pools.
        print()

        # User statistics formatting

        for line in view_user_stats:
            formatted_line = line.replace("\t", "") # removes tab spacing
            if formatted_line:
                print(formatted_line.strip()) # removes white space between lines and prints data
        
        print()
        print("----------------------------------------------------------")



################################################################################################################################

username_password = read_user_data()
task_list = read_tasks()

logged_in = False

while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")

    if curr_user not in username_password.keys():
        print("User does not exist")
        continue

    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue

    else:
        print("Login Successful!")
        logged_in = True

while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()

    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - generate reports
ds - Display statistics
e - Exit
: ''').lower()

    if menu == 'r':

        reg_user()

    elif menu == 'a':

        add_task(username_password)

    elif menu == 'va':

        view_all(task_list)

    elif menu == 'vm':

        view_mine(task_list, curr_user)

    elif menu == 'gr':

        gen_rep(task_list, username_password)

    elif menu == 'ds' and curr_user == 'admin':

        view_stats(username_password, task_list)

    elif menu == 'e':

        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice. Please try again")