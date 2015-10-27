def compare_trigram_with_dictionary():
    """
    compares detection accuracy of trigram approach with dictionary approach
    """
    from preprocessing import utilities
    import task0
    import task1

    utilities.print_banner('Benchmarking Trigram approach against Dictionary approach')

    words_set = utilities.get_words_set(file_name="preprocessing/big.txt")
    test_data = utilities.parse_sentences(utilities.get_random_300_sentences(
            file_name="preprocessing/holbrook-tagged.dat.txt"))

    utilities.print_banner("Dictionary approach")
    dict_approach = task0.calculate_detection_accuracy(words_set=words_set, test_data=test_data)
    print("Dictionary approach accuracy", dict_approach, "%")

    utilities.print_banner("Trigram approach")
    tri_approach = task1.calculate_accuracies(test_data=test_data)
    print("Trigram approach accuracy ", tri_approach, "%")

    utilities.print_banner("Comparison")
    print("Dictionary approach:", dict_approach, "% || Trigram approach", tri_approach, "%")


def compare_dictionary_with_hashed_dictionary():
    """
    Compare performance (execution speed) between Linear Dictionary / Brute Force Approach
    and Hashed Dictionary / Bit map Approach
    :return:
    """
    from preprocessing import utilities
    import timeit
    setup = 'import task0 ;import task2;from preprocessing import utilities ;' \
            'test_data = utilities.parse_sentences(utilities.get_random_300_sentences(' \
            'file_name=\"preprocessing/holbrook-tagged.dat.txt\"))'
    utilities.print_banner('Comparing execution speeds and Accuracy')
    results = {}

    utilities.print_banner('Linear Dictionary / Brute Force Approach')
    runtime = timeit.timeit('print(task0.calculate_accuracies(test_data=test_data))', setup=setup, number=1)
    print('Execution time:', runtime, 'seconds')
    results['Linear Dictionary / Brute Force Approach'] = runtime

    utilities.print_banner('Hashed Dictionary / Bit map Approach')
    runtime = timeit.timeit('print(task2.calculate_accuracies(test_data=test_data))', setup=setup, number=1)
    print('Execution time:', runtime, 'seconds')
    results['Hashed Dictionary / Bit map Approach'] = runtime

    utilities.print_banner('Comparison')
    print(results)

if __name__ == '__main__':
    compare_trigram_with_dictionary()
    compare_dictionary_with_hashed_dictionary()
