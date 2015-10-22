# class to calculate Minimum editing distance with backtrace
class BackTraceMED:
    def __init__(self):
        self.path = None
        self.distance = None
        self.given_str = None
        self.desired_str = None

    def set_str(self, given_str=input("Enter the string to be changed\n")
                , desired_str=input("Enter the desired string\n")):
        self.given_str = given_str
        self.desired_str = desired_str

    def print_matrix(self, matrix, matrix_name):
        print(matrix_name + " matrix")
        for row in matrix:
            print(row)

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

        MED = distance[len(given_str) - 1][len(desired_str) - 1]
        """

        # initialize the path matrix
        self.path = [[None] * (len(self.desired_str) + 1)] * (len(self.given_str) + 1)

        # initialize first row  ie dist(0, j)
        self.distance = [[j for j in range(len(self.desired_str) + 1)]]

        # initialize first column ie dist(j, 0)
        # using (nested) list comprehension and ternary operator
        self.distance += [[i if k == 0 else -1 for k in range(len(self.desired_str) + 1)]
                          for i in range(1, len(self.given_str) + 1)]
        for i in range(1, len(self.given_str) + 1):
            for j in range(1, len(self.desired_str) + 1):
                directions = list([self.distance[i - 1][j] + 1])  # deletion
                directions.append(self.distance[i][j - 1] + 1)  # insertion
                if self.given_str[i - 1] == self.desired_str[j - 1]:  # substitution
                    directions.append(self.distance[i - 1][j - 1])
                else:
                    directions.append(self.distance[i - 1][j - 1] + 2)
                minimum = min(directions)
                self.distance[i][j] = minimum
                if minimum == directions[0]:
                    self.path[i][j] = [(i-1), j]
                elif minimum == directions[1]:
                    self.path[i][j] = [i, (j-1)]
                elif minimum == directions[2]:
                    self.path[i][j] = [(i-1), (j-1)]

    def calculate(self):
        if self.given_str is None or self.desired_str is None:
            self.set_str()
        if self.distance is None or self.path is None:
            self.populate_matrices()
        return self.distance[len(self.given_str) - 1][len(self.desired_str) - 1]

if __name__ == "__main__":
    med = BackTraceMED
    print("MED ", med.calculate())
