# Laboratory work №4
# Working with files, classes, serializers, regular expressions, and standard libraries.

# Ksenia Kotova, 253503, 21.04.2024
# version: 1.0

from task1.task_1 import task_1
from task2.task_2 import task_2
from task3.task_3 import task_3
from task4.task_4 import task_4
from task5.task_5 import task_5
from menu.menu import print_menu, navigate_menu
from task6.task_6 import task_6

if __name__ == '__main__':
    main_tasks = {
        "Task 1": task_1,
        "Task 2": task_2,
        "Task 3": task_3,
        "Task 4": task_4,
        "Task 5": task_5,
        "Task 6": task_6
    }

    main_options = list(main_tasks.keys()) + ["Exit"]
    main_choice = 1
    main_prompt = '\t\t\t\tWhich task would you like to check?'

    print_menu(main_choice, main_options, main_prompt)
    navigate_menu(main_choice, main_options, main_prompt, main_tasks)