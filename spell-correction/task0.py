assumptions = "Assumption(s):\n" \
              "\tFirst character is correct\n" \
              "Note(s):\n" \
              "\tEverything is converted to lowercase first" \
              "\tEverything is alphanumeric"


def calculate_accuracy(verbose=False):
    from preprocessing import utilities
    from MED import normal_MED
    from collections import defaultdict
    dictionary = utilities.get_dictionary(file_name="preprocessing/big.txt")

    if verbose:
        print(dictionary)
    words = utilities.parse_sentences(utilities.get_random_300_sentences(
        file_name="preprocessing/holbrook-tagged.dat.txt"))
    print(len(words), "erroneous words found in randomly selected 300 sentences")
    if verbose:
        print(words)
    results = defaultdict(lambda: {'correct_word': None,
                                   'top_matches': []})
    print("checking for every incorrect word")
    for incorrect_word in words:
        if verbose:
            print("checking for", incorrect_word)
        med_dict = defaultdict(int)
        for i in range(len(dictionary[incorrect_word[0]])):
            med_dict[i] = normal_MED.calculate(incorrect_word, dictionary[incorrect_word[0]][i])
        results[incorrect_word]['correct_word'] = words[incorrect_word]
        med_dict_sorted = sorted(med_dict, key=lambda x: med_dict[x])
        probable_correct_words = 0
        for correct_word_list_index in med_dict_sorted:
            results[incorrect_word]['top_matches'].append(dictionary[incorrect_word[0]][correct_word_list_index])
            probable_correct_words += 1
            if probable_correct_words == 3:
                break

    correctly_detected = 0
    for result in results:
        if results[result]['correct_word'] in results[result]['top_matches']:
            correctly_detected += 1

    detection_accuracy_percentage = float(correctly_detected / len(results)) * 100

    if verbose:
        print(results)

    print("Correctly detected", correctly_detected, "out of", len(results), "words")
    print("Accuracy", detection_accuracy_percentage, '%')

    return detection_accuracy_percentage


if __name__ == "__main__":
    calculate_accuracy()
