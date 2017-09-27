import cs50

def main():
    print("Oh hai! ", end="")
    while True:
        print("How much change is owed?")
        change = cs50.get_float()
        if change >= 0:
            break
    calc_change(change)

def calc_change(change):
    change *= 100

    coins = 0;

    coins += change // 25
    change -= (change // 25) * 25
    coins += change // 10
    change -= (change // 10) * 10
    coins += change // 5
    change -= (change // 5) * 5
    coins += change

    print("{}".format(coins))

if __name__ == "__main__":
    main()