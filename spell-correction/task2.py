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
        :return: ((sum of(ascii value * index of char)*10))+len(word))%size
        """
        if size is None:
            size = self.size
        index = 0
        for pos in range(len(word)):
            index += (ord(word[pos]) - 96)
        index *= 10
        index += len(word)
        return index % size

    def rehash(self, index, step=4):
        # return (index + (step ** 2)) % self.size
        return (index + step) % self.size

    def put(self, word):
        index = self.hash(word)
        if self.words is None:
            self.words[index] = word
            self.no_of_words += 1
        else:
            step = 1
            while self.words[index] is not None:
                index = self.rehash(index, step)
                step += 1
            self.words[index] = word
            self.no_of_words += 1

        if self.no_of_words/self.size > self.load_factor:
            temp = self.words
            self.no_of_words = 0
            self.size *= 2
            self.words = [None]*self.size
            for word in temp:
                if self.words is None:
                    self.words[index] = word
                    self.no_of_words += 1
                else:
                    step = 1
                    while self.words[index] is not None:
                        index = self.rehash(index, step)
                        step += 1
                    self.words[index] = word
                    self.no_of_words += 1

    def contains_words(self, word):
        index = self.hash(word)
        start_pos = index
        if self.words[index] == word:
            return True
        else:
            stop = False
            while self.words[index] != word or not stop:
                index = self.rehash(index)
                if index == start_pos:
                    stop = True
            if not stop:
                return True
            else:
                return False

    def __contains__(self, word):
        return self.contains_words(word)


def create_hashed_dictionary(words_set=None):
    file_name = "preprocessing/big.txt"
    if words_set is None:
        import re
        file_name = "preprocessing/big.txt"
        file = open(file_name, mode="r")
        file_content = file.read()
        file.close()
        words_set = set(re.sub('\W+', ' ', file_content).lower().split())
    print(len(words_set), "unique words found in", file_name)
    print("Saving all the words in hashmap")
    dictionary = WordTable()
    for word in words_set:
        dictionary.put(word)
    return dictionary


def calculate_detection_accuracy(dictionary,sentences=None, test_data=None, verbose=False):
    from preprocessing import utilities
    if sentences is None:
        sentences = utilities.sanitize_sentences(utilities.get_all_sentences(
            file_name="preprocessing/holbrook-tagged.dat.txt"))
    detected = 0
    no_of_words_in_sentences = 0
    for sentence in sentences:
        words = sentence.split()
        no_of_words_in_sentences += len(words)
        for word in words:
            if word in dictionary:
                detected += 1
    if test_data is None:
        test_data = utilities.parse_sentences(utilities.get_random_300_sentences(
            file_name="preprocessing/holbrook-tagged.dat.txt"))
    for incorrect_word in test_data:
        if incorrect_word not in dictionary:
            detected += 1
        if test_data[incorrect_word] in dictionary:
            detected += 1
    return (detected / (no_of_words_in_sentences + 2 * len(test_data))) * 100


def get_top3_matches(incorrect_word, words_list):
    from MED import normal_MED
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
    from preprocessing import utilities
    corrected = 0
    if test_data is None:
        test_data = utilities.parse_sentences(utilities.get_random_300_sentences(
            file_name="preprocessing/holbrook-tagged.dat.txt"))
    if verbose:
        print(test_data)
    print("checking for every incorrect word")

    for incorrect_word in test_data:
        lengths = [len(incorrect_word), len(incorrect_word) + 1, len(incorrect_word) - 1]
        iteration = 0
        while iteration < 3:
            if lengths[iteration] in indexes:
                top3_matches = get_top3_matches(incorrect_word=incorrect_word,
                                                words_list=words_list[lengths[iteration]:lengths[iteration]+1])
            if test_data[incorrect_word] in top3_matches:
                corrected += 1
                break
            iteration += 1
    return (corrected / len(test_data)) * 100


def calculate_accuracies(test_data=None, runs=1, verbose=False):
    from preprocessing import utilities
    words_set = utilities.get_words_set(file_name="preprocessing/big.txt")
    words_list = utilities.get_sorted_linear_dictionary(words_set)
    indexes = utilities.get_indexes_list(words_list)
    hashed_dictionary = create_hashed_dictionary(words_set)
    detection_accuracy_percentage = 0
    correction_accuracy_percentage = 0
    for run in range(runs):
        if test_data is None:
            test_data = utilities.parse_sentences(utilities.get_random_300_sentences(
                file_name="preprocessing/holbrook-tagged.dat.txt"))
        print(len(test_data), "tagged erroneous words found in randomly selected 300 sentences")
        detection_accuracy_percentage += calculate_detection_accuracy(dictionary=hashed_dictionary, test_data=test_data,
                                                                      verbose=verbose)
        correction_accuracy_percentage += calculate_correction_accuracy(words_list=words_list, test_data=test_data,
                                                                        indexes=indexes, verbose=verbose)
    return {'detection_accuracy_percentage': detection_accuracy_percentage/runs,
            'correction_accuracy_percentage': correction_accuracy_percentage/runs}

print(calculate_accuracies())