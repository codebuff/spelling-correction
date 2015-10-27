#!/usr/bin/env python3
# class to calculate Minimum editing distance with backtrace
class WeightedMED:
    def __init__(self):
        from MED.confusion_matrices import  ConfusionMatrices
        self.path = None
        self.distance = None
        self.given_str = None
        self.desired_str = None
        self.mtx = ConfusionMatrices()

    def set_str(self, given_str=None, desired_str=None):
        if given_str is None:
            self.given_str = input("Enter the string to be changed\n")
        else:
            self.given_str = given_str
        if desired_str is None:
            self.desired_str = input("Enter the desired string\n")
        else:
            self.desired_str = desired_str

    def populate_matrices(self):
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
                directions = list([self.distance[row - 1][col] + self.mtx.get_del_cost(self.given_str[row - 1])])  # deletion
                directions.append(self.distance[row][col - 1] + self.mtx.get_insert_cost(self.desired_str[col - 1]))  # insertion
                if self.given_str[row - 1] == self.desired_str[col - 1]:  # substitution
                    directions.append(self.distance[row - 1][col - 1])
                else:
                    directions.append(self.distance[row - 1][col - 1] + self.mtx.get_sub_cost(self.given_str[row - 1],
                                                                                          self.desired_str[col - 1]))
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

    def validate(self):
        if self.given_str is None or self.desired_str is None:
            self.set_str()
        if self.distance is None or self.path is None:
            self.populate_matrices()

    def calculate(self):
        self.validate()
        return self.distance[len(self.given_str)][len(self.desired_str)]

    def get_operation(self, x, y):
        return self.path[x][y][3]

    def print_alignment(self, print_steps=False):
        from preprocessing import utilities

        self.validate()

        given = list(self.given_str)
        desired = list(self.desired_str)

        task = []

        row = len(self.given_str)
        col = len(self.desired_str)

        while self.path[row][col] is not None:
            if self.path[row][col][3] == "deletion":
                desired.insert(col, "*")
                task.append("delete " + given[row - 1])
            if self.path[row][col][3] == "insertion":
                given.insert(row, "*")
                task.append("insert " + desired[col - 1])
            if self.path[row][col][3] == "substitution":
                task.append("substitute " + given[row - 1] + " with " + desired[col - 1])
            if self.path[row][col][3] == "none":
                task.append("substitute/copy " + given[row - 1] + " with " + desired[col - 1] + " (NO OP)")
            # print(self.path[row][col])
            temp = row
            row = self.path[row][col][0]
            col = self.path[temp][col][1]
        while row != 0:
            desired.insert(col, "*")
            task.append("delete " + given[row - 1])
            row -= 1
        while col != 0:
                given.insert(row, "*")
                task.append("insert " + desired[col - 1])
                col -= 1

        utilities.print_banner('Alignment')
        print(' '.join(given))
        for i in range(len(given)):
            print('|', end=" ")
        print()
        print(' '.join(desired))

        if print_steps:
            utilities.print_banner('Steps')
            step = 1
            while task:
                print("Step", step, task.pop())
                step += 1

    def print_steps(self):
        self.print_alignment(print_steps=True)

if __name__ == '__main__':
    med = WeightedMED()
    print('Weighted MED', med.calculate())
    med.print_steps()
    med.print_alignment()
