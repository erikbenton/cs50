import cs50

def mario(h):
    for i in range(h):
        for j in range(h):
            if(j < h-i-1):
                print(" ",end="")
            else:
                print("#",end="")
        print("# #", end="")
        for j in range(i+1):
            print("#", end="")
        print()

def main():
    while True:
        print("Height: ", end="")
        height = cs50.get_int()
        if height >= 0:
            break
    mario(height)


if __name__ == "__main__":
    main()