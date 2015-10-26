def get_words_set(file_name="big.txt"):
    import re
    file = open(file_name, mode="r")
    file_content = file.read()
    file.close()
    words_set = set(re.sub('\W+', ' ', file_content).lower().split())
    print(len(words_set), "unique words found in", file_name)
    return words_set


def get_dictionary(words_set):
    """
    :param words_set: dictionary will be generated from this file.
    :return: dictionary = { char in alphabetical order :
                           list of unique words starting with this char
              }
    """
    from collections import defaultdict
    words_dict = defaultdict(list)
    for word in words_set:
        words_dict[word[0]].append(word)
    for char in words_dict:
        words_dict[char] = sorted(words_dict[char])
    return words_dict


def get_sorted_linear_dictionary(words_set):
    """
    :param words_set:
    :return: a list first sorted alphabetically and then by length of word
    """
    words_list = list(words_set)
    words_list = sorted(words_list)
    words_list = sorted(words_list, key=len)
    return words_list


def get_indexes_list(sorted_linear_dictionary):
    """
    :return:a list which contains positions at which length of string changes
    in size sorted word_list
    """
    indexes = {}
    length = 0
    for pos in range(len(sorted_linear_dictionary)):
        if len(sorted_linear_dictionary[pos]) > length:
            indexes[len(sorted_linear_dictionary[pos])] = pos
        length = len(sorted_linear_dictionary[pos])


def get_all_sentences(file_name="holbrook-tagged.dat.txt"):
    file = open(file_name, "r")
    sentences_list = file.read().splitlines()
    file.close()
    return sentences_list


def get_random_300_sentences(file_name="holbrook-tagged.dat.txt", start=None):
    file = open(file_name, "r")
    sentences_list = file.read().splitlines()
    file.close()
    if start is None:
        import random
        start = random.randint(0, len(sentences_list) - 301)
    print("Taking 300 sentences from line no", start, "to", start + 300, "from", file_name)
    return sentences_list[start:start+301]


def sanitize_sentences(sentences):
    import re
    sent = 0
    while sent != len(sentences):
        sentences[sent] = re.sub('<ERR.*ERR>', '', sentences[sent])
        sentences[sent] = re.sub('\W+', ' ', sentences[sent])
        sent += 1
    return sentences


def parse_sentences(sentences_list):
    """
    :param sentences_list:
    :return: dictionary = { incorrect_word : correct_word }
    """

    words = dict()
    for sentence in sentences_list:
        if '<ERR' in sentence:
            temp = sentence.split(sep='<ERR')[1].split(sep='</ERR>')[0].split(sep='>')
            words[temp[1].strip().lower()] = temp[0].split(sep='=')[1].lower().strip()
    return words


def get_trigrams(words_set):
    print("generating trigrams")
    from collections import Counter
    trigrams = Counter()
    word_trigram = []
    for word in words_set:
        index = 0
        while (index+2) < len(word):
            word_trigram.append(word[index:index+3])
            index += 1
        trigrams.update(word_trigram)
    return trigrams

"""tri = get_trigrams(get_dictionary())
print(len(tri))
for trigram in tri:
    if len(trigram) != 3:
        print(trigram)
      """
