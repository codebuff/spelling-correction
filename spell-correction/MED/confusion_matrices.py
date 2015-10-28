#!/usr/bin/env python3
class ConfusionMatrices:
    def __init__(self, test_data=None):
        self.path = None
        self.distance = None
        if test_data is None:
            self.get_test_data()
        else:
            self.test_data = test_data
        self.given_str = None
        self.desired_str = None
        self.del_matrix = [0] * 26
        self.insert_matrix = [0] * 26
        self.sub_matrix = [[chr(i + 96) for i in range(27)]]
        self.sub_matrix += [[chr(j+97) if i == 0 else 0 for i in range(27)] for j in range(26)]
        self.process_test_data()

    def get_test_data(self):
        from ..preprocessing import utilities
        import os
        import re
        file_name = os.getcwd() + '/spell-correction/MED/spell-errors.txt'
        self.test_data = dict()
        sentences_list = utilities.get_all_sentences(file_name=file_name)
        for sentence in sentences_list:
            sections = sentence.split(sep=':')
            self.test_data[sections[0]] = re.sub('\W+', ' ', sections[1]).lower().split()

    def populate_dist_and_path_matrices(self):
        """
        distance(given_str, desired_str) , matrix form
            d e s i r e d s t r
          0 1 2 3 4 5 6 7 8 9 10
        g 1
        i 2
        v 3
        e 4
        n 5
        s 7
        t 8
        r 9                    MED

        MED = distance[len(given_str)][len(desired_str)]
        """

        # initialize the path matrix
        self.path = [[None for i in range(len(self.desired_str) + 1)]
                     for j in range(len(self.given_str) + 1)]
        # initialize first row  ie dist(0, j)
        self.distance = [[j for j in range(len(self.desired_str) + 1)]]

        # initialize first column ie dist(j, 0)
        # using (nested) list comprehension and ternary operator
        self.distance += [[i if k == 0 else -1 for k in range(len(self.desired_str) + 1)]
                          for i in range(1, len(self.given_str) + 1)]
        for row in range(1, len(self.given_str) + 1):
            for col in range(1, len(self.desired_str) + 1):
                directions = list([self.distance[row - 1][col] + 1])  # deletion
                directions.append(self.distance[row][col - 1] + 1)  # insertion
                if self.given_str[row - 1] == self.desired_str[col - 1]:  # substitution
                    directions.append(self.distance[row - 1][col - 1])
                else:
                    directions.append(self.distance[row - 1][col - 1] + 2)
                minimum = min(directions)
                self.distance[row][col] = minimum
                # todo(dt) take care of multiple paths
                if minimum == directions[0]:
                    self.path[row][col] = [(row-1), col, "top", "deletion"]
                elif minimum == directions[1]:
                    self.path[row][col] = [row, (col-1), "left", "insertion"]
                elif minimum == directions[2]:
                    if self.given_str[row - 1] == self.desired_str[col - 1]:  # substitution
                        self.path[row][col] = [(row-1), (col-1), "diagonal", "none"]
                    else:
                        self.path[row][col] = [(row-1), (col-1), "diagonal", "substitution"]

    def update_confusion_matrices(self, print_procedure=False):
        given = list(self.given_str)
        desired = list(self.desired_str)
        row = len(self.given_str)
        col = len(self.desired_str)

        while self.path[row][col] is not None:

            if self.path[row][col][3] == "deletion":
                if -1 < (ord(given[row-1]) - 97) < 26:
                    self.del_matrix[ord(given[row-1]) - 97] += 1

            if self.path[row][col][3] == "insertion":
                if -1 < (ord(desired[col - 1]) - 97) < 26:
                    self.insert_matrix[ord(desired[col - 1]) - 97] += 1

            if self.path[row][col][3] == "substitution":
                if 0 < (ord(desired[col - 1]) - 96) < 27 and 0 < (ord(given[row-1]) - 96) < 27:
                    self.sub_matrix[ord(given[row-1]) - 96][ord(desired[col - 1]) - 96] += 1

            temp = row
            row = self.path[row][col][0]
            col = self.path[temp][col][1]
        while row != 0:
            if -1 < (ord(given[row-1]) - 97) < 26:
                self.del_matrix[ord(given[row-1]) - 97] += 1
            row -= 1
        while col != 0:
            if -1 < (ord(desired[col - 1]) - 97) < 26:
                self.insert_matrix[ord(desired[col - 1]) - 97] += 1
            col -= 1

    def process_test_data(self):
        print('creating confusion matrices')
        for correct_word in self.test_data:
            self.desired_str = correct_word
            for incorrect_word in self.test_data[correct_word]:
                self.given_str = incorrect_word
                self.populate_dist_and_path_matrices()
                self.update_confusion_matrices()

    def get_del_cost(self, char):
        if -1 < (ord(char) - 97) < 26:
            return self.del_matrix[ord(char) - 97]
        else:
            return 0

    def get_insert_cost(self, char):
        if -1 < (ord(char) - 97) < 26:
            return self.insert_matrix[ord(char) - 97]
        else:
            return 0

    def get_sub_cost(self, given_char, desired_char):
        if 0 < (ord(given_char) - 96) < 27 and 0 < (ord(desired_char) - 96) < 27:
            return self.sub_matrix[ord(given_char) - 96][ord(desired_char) - 96]
        else:
            return 0
