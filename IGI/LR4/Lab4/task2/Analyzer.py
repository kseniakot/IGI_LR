import re


class Analyzer:
    """A class that analyzes the given data"""
    def __init__(self, data):
        """Initializes the Analyzer object with the given data"""
        self._data = data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    def count_sentences(self):
        """Counts the number of sentences in the data"""
        return len(re.findall(r'[.!?](\s|$)', self.data))

    def count_narrative_sentences(self):
        """Counts the number of narrative sentences in the data"""
        return len(re.findall(r'[.](\s|$)', self.data))

    def count_questions(self):
        """Counts the number of questions in the data"""
        return len(re.findall(r'[?](\s|$)', self.data))

    def count_persuasive_sentences(self):
        """Counts the number of persuasive sentences in the data"""
        return len(re.findall(r'!(?!\?)(\s|$)', self.data))

    def count_average_sentence_length(self):
        """Counts the average sentence length in the data"""
        sentences = re.findall(r'[.!?](\s|$)', self.data)
        words = re.findall(r'\w+', self.data)
        words_characters = sum(len(word) for word in words)
        return words_characters / len(sentences) if len(sentences) > 0 else 0

    def count_average_word_length(self):
        """Counts the average word length in the data"""
        words = re.findall(r'\w+', self.data)
        words_characters = sum(len(word) for word in words)
        return words_characters / len(words) if len(words) > 0 else 0

    def count_emojy(self):
        """Counts the number of emojies in the data"""
        return len(re.findall(r'[:;]-*[\[\]()]+', self.data))

    def list_binary_numbers(self):
        """Returns the list of binary numbers in the data"""
        return re.findall(r'\b[01]+\b', self.data)

    def list_vowel_consonant_words(self):
        """Returns the list of words with first vowel letter and second consonant letter"""
        return re.findall(r'\b[aeiou][b-df-hj-np-tv-z]\w*\b', self.data, re.I)

    def list_vowel_start_vowel_end_words(self):
        """Returns the list of words with first or last letters being vowels"""
        return re.findall(r'\b[aeiou]\w*[aeiou]\b', self.data, re.I)

    def count_character_occurrences(self):
        """Counts the occurrences of each character in the data"""
        data_without_spaces = re.sub(r'\s', '', self.data.lower())
        character_counts = {}
        for character in data_without_spaces.lower():
            if character not in character_counts:
                character_counts[character] = 1
            else:
                character_counts[character] += 1
        return character_counts

    def list_words_after_comma(self):
        """Returns the list of words after a comma in alphabetical order"""
        words = re.findall(r',\s*(\w+)', self.data)
        return sorted(words)


