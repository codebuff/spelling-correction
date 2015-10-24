def get_dictionary(file_name="big.txt"):
    """
    :param file_name: dictionary will be generated from this file.
    :return: dictionary = { char in alphabetical order :
                           list of unique words starting with this car
              }
    """
    import re
    from collections import defaultdict
    file = open(file_name, mode="r")
    file_content = file.read()
    file.close()
    word_set = set(re.sub('\W+', ' ', file_content).lower().split())
    print(len(word_set), "unique words found in", file_name)
    word_dict = defaultdict(list)
    for word in word_set:
        word_dict[word[0]].append(word)
    for char in word_dict:
        word_dict[char] = sorted(word_dict[char])
    return word_dict


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
    print("Taking sentences from line no", start, "to", start + 300, "from", file_name)
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


def get_trigrams(dictionary):
    print("generating trigrams")
    from collections import Counter
    trigrams = Counter()
    for key in dictionary:
        word_trigram = []
        for word in dictionary[key]:
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
