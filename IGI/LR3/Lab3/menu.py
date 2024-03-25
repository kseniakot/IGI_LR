import readchar
import os


def loop_function(function_to_loop):
    def wrapper(selected, *args, **kwargs):
        while True:
            selected = function_to_loop(selected, *args, **kwargs)
            if not selected:
                break

    return wrapper


def print_menu(index, options, prompt):
    os.system('clear')
    print(prompt)
    for i, option in enumerate(options, 1):
        print("\t\t\t\t" + option) if i != index else print("\t\t\t\t" + option + " <--")


@loop_function
def navigate_menu(selected, options, prompt, tasks):
    print_menu(selected, options, prompt)
    key = readchar.readkey()

    if key == readchar.key.UP:
        selected -= 1
        if selected < 1:
            selected = len(options)
    elif key == readchar.key.DOWN:
        selected += 1
        if selected > len(options):
            selected = 1
    elif key == readchar.key.ENTER:
        if selected == len(options):
            os.system('clear')
            return None
        else:
            tasks[options[selected - 1]]()
            print_menu(selected, options, prompt)
    return selected


def wait_for_key_press():
    print('Press any key...')
    while True:
        stop_key = readchar.readkey()
        if stop_key:
            break
