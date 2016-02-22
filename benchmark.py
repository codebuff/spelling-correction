def compare_dictionary_with_hashed_dictionary():
    """ 
    fixme way too many import errors

    Compare performance (execution speed) between Linear Dictionary / Brute Force Approach
    and Hashed Dictionary / Bit map Approach
    :return:
    """
    import timeit
    import os
    import sys
    CWD = os.getcwd()
    sys.path.insert(0, CWD)
    print(sys.path)
    file_name = CWD + '/spell-correction/preprocessing/holbrook-tagged.dat.txt'

    setup = 'import spell-correction.task0 ;import spell-correction.task2;from .preprocessing import utilities;' \
            'test_data = utilities.parse_sentences(utilities.get_random_300_sentences())'
    print('\n  === Comparing execution speeds and Accuracy ===  \n')
    results = {}

    print('Linear Dictionary / Brute Force Approach')
    runtime = timeit.timeit('print(task0.calculate_accuracies(test_data=test_data))', setup=setup, number=1)
    print('Execution time:', runtime, 'seconds')
    results['Linear Dictionary / Brute Force Approach'] = runtime

    print('Hashed Dictionary / Bit map Approach')
    runtime = timeit.timeit('print(task2.calculate_accuracies(test_data=test_data))', setup=setup, number=1)
    print('Execution time:', runtime, 'seconds')
    results['Hashed Dictionary / Bit map Approach'] = runtime

    print('Comparison')
    print(results)

if __name__ == '__main__':
    #compare_trigram_with_dictionary()
    compare_dictionary_with_hashed_dictionary()
