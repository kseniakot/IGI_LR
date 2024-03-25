# Task 4

import os
from menu import wait_for_key_press


def count_uppercase_letters(s):
    """Count the number of uppercase letters in the string"""
    return sum(1 for char in s if char.isupper())


def count_lowercase_letters(s):
    """Count the number of lowercase letters in the string"""
    return sum(1 for char in s if char.islower())


def search_word_with_z(s):
    """Find the first word which contains 'z' and determine its position"""
    words = s.split()
    for i, word in enumerate(words):
        if 'z' in word:
            return i, word
    return None


def remove_words_starting_with_a(s):
    """Remove words starting with 'a' from the string"""
    words = s.split()
    return ' '.join(word for word in words if not word.startswith('a'))


def task_4():
    """ a) Determine the amount of lowercase and uppercase letters in the string
        b) Find the first word which contains 'z' and determine its position
        c) print the string without the words starting with 'a' """

    os.system('clear')
    test_str = ("«So she was considering in her own mind, as well as she could,"
                " for the hot day made her feel very sleepy and stupid, whether "
                "the pleasure of making a daisy-chain would be worth the trouble of "
                "getting up and picking the daisies, when suddenly a White Rabbit with "
                "pink eyes ran close by her.» ")

    print(f"The number of uppercase letters: {count_uppercase_letters(test_str)}")
    print(f"The number of lowercase letters: {count_lowercase_letters(test_str)}")

    if (z_word := search_word_with_z(test_str)) is not None:  # walrus operator
        print(f"The first word with 'z' is '{z_word[1]}' at position {z_word[0]}")

    print("The string without the words starting with 'a':")
    print(remove_words_starting_with_a(test_str))

    wait_for_key_press()


