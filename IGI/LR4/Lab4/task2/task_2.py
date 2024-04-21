from task2.Analyzer import Analyzer
from Services.file_service import FileService


def task_2():
    """Analyze the data from the txt file and print the results"""
    try:
        file_service = FileService('text.txt')
    except FileNotFoundError as e:
        print(e)
        return
    data = file_service.read_txt()
    analyzer = Analyzer(data)
    file_service.file_path = 'results.txt'
    file_service.clear_file()
    # Count the number of sentences in the data
    file_service.write_txt(f'Sentences: {analyzer.count_sentences()}\n')
    print(f'Sentences: {analyzer.count_sentences()}')

    # Count the number of narrative sentences in the data
    file_service.write_txt(f'Narrative sentences: {analyzer.count_narrative_sentences()}\n')
    print(f'Narrative sentences: {analyzer.count_narrative_sentences()}')

    # Count the number of questions in the data
    file_service.write_txt(f'Questions: {analyzer.count_questions()}\n')
    print(f'Questions: {analyzer.count_questions()}')

    # Count the number of persuasive sentences in the data
    file_service.write_txt(f'Persuasive sentences: {analyzer.count_persuasive_sentences()}\n')
    print(f'Persuasive sentences: {analyzer.count_persuasive_sentences()}')

    # Count the average sentence length in the data
    file_service.write_txt(f'Average sentence length: {analyzer.count_average_sentence_length()}\n')
    print(f'Average sentence length: {analyzer.count_average_sentence_length()}')

    # Count the average word length in the data
    file_service.write_txt(f'Average word length: {analyzer.count_average_word_length()}\n')
    print(f'Average word length: {analyzer.count_average_word_length()}')

    # Count the number of emojies in the data
    file_service.write_txt(f'Emojies: {analyzer.count_emojy()}\n')
    print(f'Emojies: {analyzer.count_emojy()}')

    # Returns the list of binary numbers in the data
    file_service.write_txt(f'Binary numbers: {analyzer.list_binary_numbers()}\n')
    print(f'Binary numbers: {analyzer.list_binary_numbers()}')

    # Returns the list of words with first vowel letter and second consonant letter
    file_service.write_txt(f'Words with first vowel letter and second consonant letter:'
                           f' {analyzer.list_vowel_consonant_words()}\n')
    print(f'Words with first vowel letter and second consonant letter: '
          f'{analyzer.list_vowel_consonant_words()}')

    # Returns the list of words with first or last letters being vowels
    file_service.write_txt(f'Vowel start vowel end words: {analyzer.list_vowel_start_vowel_end_words()}\n')
    print(f'Vowel start vowel end words: {analyzer.list_vowel_start_vowel_end_words()}')

    # Dublicates
    for character, count in analyzer.count_character_occurrences().items():
        file_service.write_txt(f'Character: {character} Count: {count}\n')
        print(f'Character: {character} Count: {count}')

    print('Results are saved to results.txt')

    FileService.make_zip('text.zip', file_service.file_path)

    # Get information about the zip file
    for item in FileService.get_zip_info('text.zip'):
        print(f"File Name: {item.filename} Date: {item.date_time} Size: {item.file_size}"
              f" Compressed Size: {item.compress_size}")


if __name__ == '__main__':
    task_2()
