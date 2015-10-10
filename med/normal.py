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

MED = dist(len(given_str) - 1 ,len(desired_str) - 1 )
"""

# initialize first row  ie dist(0, j)
dist = [[desired_str[j] for j in range(len(desired_str))]]

print(dist)

# initialize first column ie dist(j, 0)
# using conditional expression ie ternary operators
# for i in range(len(given_str)):
#    dist.append([given_str[i] if k == 0 else -1 for k in range(len(desired_str))])

# using (nested) list comprehension and ternary operator
dist += [[given_str[i] if k == 0 else -1 for k in range(len(desired_str))] for i in range(len(given_str))]

print(dist)
