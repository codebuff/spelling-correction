from preprocessing import utilities


def process_trigrams():
    from collections import Counter
    import math
    trigrams = utilities.get_trigrams(utilities.get_dictionary(file_name="preprocessing/big.txt"))
    total_trigrams = len(trigrams)
    top_20_percent = trigrams.most_common(math.ceil(0.2 * total_trigrams))
    normalized_trigrams = Counter()
    for trigram in top_20_percent:
        normalized_trigrams[trigram[0]] = trigram[1] / total_trigrams
    #print(total_trigrams, len(normalized_trigrams))
    return normalized_trigrams


def get_scores():
    sentences = utilities.get_all_sentences(file_name="preprocessing/holbrook-tagged.dat.txt")

    incorrect_words = utilities.parse_sentences(sentences)

    sentences = utilities.sanitize_sentences(sentences)

    normalized_trigrams = process_trigrams()

    total_correct_words = 0

    def calculate_score(word, correct_word=True):
        index = 0
        score = 0
        while (index + 2) < len(word):
            score += normalized_trigrams[word[index:index + 3]]
            index += 1
        if correct_word and len(word) > 2:
            nonlocal total_correct_words
            total_correct_words += 1
        return score / len(word)

    total_correct_words_score = 0
    total_incorrect_words_score = 0
    """for sentence in sentences:
        words = sentence.split()
        for word in words:
            total_correct_words_score += calculate_score(word)"""

    for incorrect_word in incorrect_words:
        # incorrect_words[incorrect_word] = corresponding correct word
        total_correct_words_score += calculate_score(incorrect_words[incorrect_word])
        total_incorrect_words_score += calculate_score(incorrect_word, correct_word=False)
    total_correct_words += len(incorrect_words)
    average_correct_words_score = total_correct_words_score / total_correct_words
    average_incorrect_words_score = total_incorrect_words_score / len(incorrect_words)
    print(total_correct_words,total_correct_words_score, len(incorrect_words), total_incorrect_words_score)

    return [average_correct_words_score, average_incorrect_words_score]


print(get_scores())
