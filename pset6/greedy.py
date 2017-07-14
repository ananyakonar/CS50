import cs50

def main():
    while True:
        print("O hai! How much change is owed?")
        amount = cs50.get_float()
        if amount >= 0:
            break
    
    number_of_coins = 0
    cents = int(round(amount * 100))
    
    quarter= cents // 25
    amount_left=cents%25;
    dime=  amount_left // 10
    amount_left%= 10
    
    nickel=  amount_left// 5
    amount_left %= 5
    
    number_of_coins = quarter + dime + nickel + amount_left;
    
    print("{}".format(number_of_coins))
    
if __name__ == "__main__":
    main()
