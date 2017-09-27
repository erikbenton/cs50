import sys
import cs50

def main():

    if len(sys.argv) < 2:
        print("Usage: python caesar.py k")
        return
    else:
        k = ord(sys.argv[1]) - 48

    print("plaintext: ", end="")
    plain = cs50.get_string()
    caesar(plain, k)

def caesar(plain, k):
    cipher = []

    for i in range(len(plain)):
        if plain[i] >= 'a' and plain[i] <= 'z':
            print("{}".format(chr( ord('a') + (ord(plain[i])-ord('a') + k )%26) ),end="")
        elif plain[i] >= 'A' and plain[i] <= 'Z':
            print("{}".format(chr( ord('A') + (ord(plain[i])-ord('A') + k )%26) ),end="")
        else:
            print("{}".format(plain[i]),end="")
    print()


if __name__ == "__main__":
    main()