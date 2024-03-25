# Laboratory work №3
# Data types, Collections, Functions, Modules

# Ksenia Kotova, 253503, 23.02.2024

from task_1 import task_1
from task_2 import task_2
from task_3 import task_3
from task_4 import task_4
from task_5 import task_5
from menu import print_menu, navigate_menu

if __name__ == '__main__':
    main_tasks = {
        "Task 1": task_1,
        "Task 2": task_2,
        "Task 3": task_3,
        "Task 4": task_4,
        "Task 5": task_5,
    }

    main_options = list(main_tasks.keys()) + ["Exit"]
    main_choice = 1
    main_prompt = '\t\t\t\tWhich task would you like to check?'

    print_menu(main_choice, main_options, main_prompt)
    navigate_menu(main_choice, main_options, main_prompt, main_tasks)
