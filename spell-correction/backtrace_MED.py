# module to calculate Minimum editing distance by normal method

given_str = input("Enter the string to be changed\n")
desired_str = input("Enter the desired string\n")

# distance(given_str, desired_str) , matrix form
"""
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

# initialize first row  ie dist(0, j)
distance = [[j for j in range(len(desired_str) + 1)]]

# initialize first column ie dist(j, 0)
# using (nested) list comprehension and ternary operator
distance += [[i if k == 0 else -1 for k in range(len(desired_str) + 1)] for i in range(1, len(given_str) + 1)]
for i in range(1, len(given_str) + 1):
    for j in range(1, len(desired_str) + 1):
        paths = list([distance[i - 1][j] + 1])
        paths.append(distance[i][j - 1] + 1)
        if given_str[i - 1] == desired_str[j - 1]:
            paths.append(distance[i - 1][j - 1])
        else:
            paths.append(distance[i - 1][j - 1] + 2)
        distance[i][j] = min(paths)
        print(paths)
print(distance)
print(distance[len(given_str) - 1][len(desired_str) - 1])
