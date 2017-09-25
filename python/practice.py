import cs50
import sys

print("s: ", end="")
s = cs50.get_string()

print("t: ", end="")
t = cs50.get_string()

if s != None and t != None:
    if s == t:
        print("same")
    else:
        print("different")


# for s in sys.argv[1]:
#     for c in s:
#         print(c)
#     print()


# for i in range(65, 65 + 26):
#     print("{} is {}".format(chr(i), i))

# def main():
#     cough(3)

# def cough(n):
#     for i in range(n):
#         print("cough")

# if __name__ == "__main__":
#     main()

# #Here is a number test
# print("Number tests")

# print("x: ", end="")
# x = cs50.get_int();
# print("y: ", end="")
# y = cs50.get_int();

# print("{} plus {} is {}".format(x, y, x+y))
# print("{} minus {} is {}".format(x, y, x-y))
# print("{} times {} is {}".format(x, y, x*y))
# print("{} divided by {} is {}".format(x, y, x/y))
# print("{} to the {} is {}".format(x, y, x**y))

# print()
# #Logical test
# print("Logical tests")

# print("Enter 'Y' for yes and 'N' for no: ", end = "")
# c = cs50.get_char()

# if c == 'Y' or c == 'y':
#     print("Yes")
# elif c == 'N' or c == 'n':
#     print("No")
# else:
#     print("Error")