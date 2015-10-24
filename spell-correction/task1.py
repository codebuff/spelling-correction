from preprocessing import utilities


def process_trigrams():
    import math
    from collections import Counter
    trigrams = utilities.get_trigrams(utilities.get_dictionary(file_name="preprocessing/big.txt"))
    total_trigrams = len(trigrams)
    top_20_percent = trigrams.most_common(math.ceil(0.2 * total_trigrams))
    normalized_trigrams_ = Counter()
    for trigram in top_20_percent:
        normalized_trigrams_[trigram[0]] = trigram[1] / total_trigrams
    return normalized_trigrams_

normalized_trigrams = process_trigrams()


def calculate_score(word):
    index = 0
    score = 0
    while (index + 2) < len(word):
        score += normalized_trigrams[word[index:index + 3]]
        index += 1
    return score / len(word)


def get_scores():
    sentences = utilities.get_all_sentences(file_name="preprocessing/holbrook-tagged.dat.txt")

    incorrect_words = utilities.parse_sentences(sentences)

    sentences = utilities.sanitize_sentences(sentences)

    total_correct_words = 0
    total_incorrect_words = 0
    total_correct_words_score = 0
    total_incorrect_words_score = 0
    for sentence in sentences:
        words = sentence.split()
        for word in words:
            total_correct_words_score += calculate_score(word)
        total_correct_words += len(words)

    for incorrect_word in incorrect_words:
        # incorrect_words[incorrect_word] = corresponding correct word
        total_correct_words_score += calculate_score(incorrect_words[incorrect_word])
        total_incorrect_words_score += calculate_score(incorrect_word)
        if len(incorrect_words) > 2:
            total_correct_words += 1
        if len(incorrect_words[incorrect_word]) > 2:
            total_incorrect_words += 1
    average_correct_words_score = total_correct_words_score / total_correct_words
    average_incorrect_words_score = total_incorrect_words_score / total_incorrect_words
    # print(total_correct_words, total_correct_words_score, len(incorrect_words), total_incorrect_words_score)

    return [average_correct_words_score, average_incorrect_words_score]


def get_threshold(scores):
    return (scores[0] + scores[1]) / 2


def calculate_accuracy(words=None):
    threshold = get_threshold(get_scores())
    if words is None:
        words = utilities.parse_sentences(utilities.get_random_300_sentences(
            file_name="preprocessing/holbrook-tagged.dat.txt"))
    print(len(words), "erroneous words found in randomly selected 300 sentences")
    correctly_detected = 0
    for incorrect_word in words:
        if calculate_score(incorrect_word) < threshold:
            correctly_detected += 1
    accuracy = (correctly_detected/len(words)) * 100
    # print("Accuracy", accuracy, "%")
    return accuracy


def compare_trigram_with_dictionary():
    import task0
    words = utilities.parse_sentences(utilities.get_random_300_sentences(
            file_name="preprocessing/holbrook-tagged.dat.txt"))

    print("\n==== Trigram approach ====")
    tri_approach = calculate_accuracy(words=words)
    print("Trigram approach accuracy ", tri_approach, "%")

    print("\n==== Dictionary approach ====")
    dict_approach = task0.calculate_accuracy(words=words)
    print("Dictionary approach accuracy", dict_approach, "%")

    print("\n==== Comparison ====")
    print("Dictionary approach:", dict_approach, "|| Trigram approach", tri_approach)

# print("Accuracy", calculate_accuracy(), "%")
if __name__ == "__main__":
    compare_trigram_with_dictionary()
