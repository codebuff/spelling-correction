assumptions = "Assumption(s):\n" \
              "\tFirst character is correct\n" \
              "Note(s):\n" \
              "\tEverything is converted to lowercase first" \
              "\tEverything is alphanumeric"


def calculate_detection_accuracy(words_set, sentences=None, test_data=None, verbose=False):
    from preprocessing import utilities
    words_list = utilities.get_sorted_linear_dictionary(words_set)
    if sentences is None:
        sentences = utilities.sanitize_sentences(utilities.get_all_sentences(
            file_name="preprocessing/holbrook-tagged.dat.txt"))
    detected = 0
    no_of_words_in_sentences = 0
    for sentence in sentences:
        words = sentence.split()
        no_of_words_in_sentences += len(words)
        for word in words:
            if word in words_list:
                detected += 1
    if test_data is None:
        test_data = utilities.parse_sentences(utilities.get_random_300_sentences(
            file_name="preprocessing/holbrook-tagged.dat.txt"))
    for incorrect_word in test_data:
        if incorrect_word not in words_list:
            detected += 1
        if test_data[incorrect_word] in words_list:
            detected += 1
    return (detected / (no_of_words_in_sentences + 2 * len(test_data))) * 100


def calculate_correction_accuracy(dictionary, test_data=None, verbose=False):
    from preprocessing import utilities
    from MED import normal_MED
    from collections import defaultdict
    if test_data is None:
        test_data = utilities.parse_sentences(utilities.get_random_300_sentences(
                file_name="preprocessing/holbrook-tagged.dat.txt"))
    if verbose:
        print(test_data)
    results = defaultdict(lambda: {'correct_word': None,
                                   'top_matches': []})
    print("checking for every incorrect word")
    for incorrect_word in test_data:
        if verbose:
            print("checking for", incorrect_word)

        med_dict = dict()
        for i in range(len(dictionary[incorrect_word[0]])):
            med_dict[i] = normal_MED.calculate(incorrect_word, dictionary[incorrect_word[0]][i])
        med_dict_sorted_indexes = sorted(med_dict, key=lambda x: med_dict[x])
        results[incorrect_word]['correct_word'] = test_data[incorrect_word]
        probable_correct_words = 0
        for correct_word_list_index in med_dict_sorted_indexes:
            results[incorrect_word]['top_matches'].append(dictionary[incorrect_word[0]][correct_word_list_index])
            probable_correct_words += 1
            if probable_correct_words == 3:
                break

    corrected = 0
    for result in results:
        if results[result]['correct_word'] in results[result]['top_matches']:
            corrected += 1
    if verbose:
        print(results)
    return float(corrected / len(test_data)) * 100


def calculate_accuracies(test_data=None, runs=1, verbose=False):
    from preprocessing import utilities
    words_set = utilities.get_words_set(file_name="preprocessing/big.txt")
    dictionary = utilities.get_dictionary(words_set)
    detection_accuracy_percentage = 0
    correction_accuracy_percentage = 0

    for run in range(runs):
        print("Iteration:", run)
        test_data = utilities.parse_sentences(utilities.get_random_300_sentences(
            file_name="preprocessing/holbrook-tagged.dat.txt"))

        print(len(test_data), "tagged erroneous words found in randomly selected 300 sentences")
        detection_accuracy_percentage += calculate_detection_accuracy(words_set=words_set, test_data=test_data,
                                                                      verbose=verbose)
        correction_accuracy_percentage += calculate_correction_accuracy(dictionary=dictionary, test_data=test_data,
                                                                        verbose=verbose)

    # print("Correctly detected", correctly_detected, "out of", len(results), "words")
    # print("Accuracy", detection_accuracy_percentage, '%')

    return {'detection_accuracy_percentage': detection_accuracy_percentage/runs,
            'correction_accuracy_percentage': correction_accuracy_percentage/runs}


if __name__ == "__main__":
    print("Dictionary approach accuracy %ages", calculate_accuracies(runs=2))
