#!/usr/bin/env python3
task = 'implement and analyze searching scheme with hashed dictionary / bitmap approach'


class WordTable:
    def __init__(self, size=40001, load_factor=0.9):
        self.load_factor = load_factor
        self.size = size
        self.no_of_words = 0
        self.words = [None] * size

    def hash(self, word, size=None):
        """
        :param word:
        :param size:
        :return: ((sum of(ascii value - 96 * index of char)*10))+len(word))%size
        """
        if size is None:
            size = self.size
        index = 0
        for pos in range(len(word)):
            index += (ord(word[pos]) - 96) * (pos + 1)
        index *= 10
        index += len(word)
        return index % size

    def rehash(self, index, step=13):
        # return (index + (step ** 2)) % self.size
        return (index + step) % self.size

    def put(self, word):
        index = self.hash(word)

        if self.words[index] is None:
            self.words[index] = word
            self.no_of_words += 1
        else:
            while self.words[index] is not None:
                index = self.rehash(index)
            self.words[index] = word
            self.no_of_words += 1

        if self.no_of_words/self.size > self.load_factor:
            print('load_factor', self.no_of_words/self.size, "creating bigger list")
            temp = self.words
            self.no_of_words = 0
            self.size *= 2
            self.words = [None]*self.size

            for word in temp:
                if word is not None:
                    index = self.hash(word)
                    if self.words[index] is None:
                        self.words[index] = word
                        self.no_of_words += 1
                    else:
                        while self.words[index] is not None:
                            index = self.rehash(index)
                        self.words[index] = word
                        self.no_of_words += 1

    def contains_words(self, word):
        # print('searching for', word)
        index = self.hash(word)

        if self.words[index] == word:
            return True
        else:
            while self.words[index] != word and self.words[index] is not None:
                index = self.rehash(index)
                # print(index, self.words[index])

            if self.words[index] == word:
                return True
            else:
                return False

    def __contains__(self, word):
        return self.contains_words(word)


def create_hashed_dictionary(words_set):
    print(len(words_set), "unique words found")

    print("Saving all the words in hashmap")

    dictionary = WordTable()

    for word in words_set:
        dictionary.put(word)
    return dictionary


def calculate_detection_accuracy(dictionary, sentences=None, test_data=None):
    from .preprocessing import utilities

    if sentences is None:
        sentences = utilities.sanitize_sentences(utilities.get_all_sentences())

    detected = 0
    no_of_words_in_sentences = 0

    for sentence in sentences:
        words = sentence.split()
        no_of_words_in_sentences += len(words)
        for word in words:
            if word in dictionary:
                detected += 1

    if test_data is None:
        test_data = utilities.parse_sentences(utilities.get_random_300_sentences())

    for incorrect_word in test_data:
        if incorrect_word not in dictionary:
            detected += 1
        if test_data[incorrect_word] in dictionary:
            detected += 1

    return (detected / (no_of_words_in_sentences + 2 * len(test_data))) * 100


def get_top3_matches(incorrect_word, words_list):
    from .MED import normal_MED
    top3_matches = []
    med_dict = dict()
    for word in words_list:
        med_dict[word] = normal_MED.calculate(incorrect_word, word)
    med_dict_sorted_by_MED = sorted(med_dict, key=lambda x: med_dict[x])
    probable_correct_words = 0
    for word in med_dict_sorted_by_MED:
        top3_matches.append(word)
        probable_correct_words += 1
        if probable_correct_words == 3:
            break
    return top3_matches


def calculate_correction_accuracy(words_list, indexes, test_data=None, verbose=False):
    from .preprocessing import utilities

    corrected = 0

    if test_data is None:
        test_data = utilities.parse_sentences(utilities.get_random_300_sentences())
    if verbose:
        print(test_data)

    print("checking for every incorrect word")
    for incorrect_word in test_data:
        if verbose:
            print('checking for', incorrect_word)
        lengths = [len(incorrect_word), len(incorrect_word) + 1, len(incorrect_word) - 1]
        iteration = 0
        while iteration < 3:
            if lengths[iteration] in indexes:
                start = indexes[lengths[iteration]]
                stop = len(words_list)
                if lengths[iteration] + 1 in indexes:
                    stop = indexes[lengths[iteration] + 1]
                else:  # look for next closest length
                    count = 0
                    length = lengths[iteration] + 2
                    while count != len(indexes):
                        if length in indexes:
                            stop = indexes[length]
                            length += 1
                            count += 1

                top3_matches = get_top3_matches(incorrect_word=incorrect_word,
                                                words_list=words_list[start:stop])

            if test_data[incorrect_word] in top3_matches:
                corrected += 1
                break

            iteration += 1

    return (corrected / len(test_data)) * 100


def calculate_accuracies(test_data=None, runs=1, verbose=False):
    from .preprocessing import utilities

    words_set = utilities.get_words_set()
    words_list = utilities.get_sorted_linear_dictionary(words_set)
    indexes = utilities.get_indexes_list(words_list)
    hashed_dictionary = create_hashed_dictionary(words_set=words_set)

    detection_accuracy_percentage = 0
    correction_accuracy_percentage = 0

    for run in range(runs):
        if test_data is None:
            test_data = utilities.parse_sentences(utilities.get_random_300_sentences())
        print(len(test_data), "tagged erroneous words found in randomly selected 300 sentences")

        detection_accuracy_percentage += calculate_detection_accuracy(dictionary=hashed_dictionary, test_data=test_data)
        correction_accuracy_percentage += calculate_correction_accuracy(words_list=words_list, test_data=test_data,
                                                                        indexes=indexes, verbose=verbose)

    return {'detection_accuracy_percentage': detection_accuracy_percentage/runs,
            'correction_accuracy_percentage': correction_accuracy_percentage/runs}

if __name__ == '__main__':
    print(calculate_accuracies())
