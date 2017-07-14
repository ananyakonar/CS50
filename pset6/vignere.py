import cs50
import sys

def main():
    if len(sys.argv) != 2:
        print("You should provide a command line arguments!")
        exit(1)
    
    if sys.argv[1].isalpha() == False:
        print("You should provide valid keyword!")
        exit(1)
        
    print("plaintext:", end = "")    
    plaintext = cs50.get_string()
    translated = []
    keyIndex = 0
    length = len(sys.argv[1])
    print("ciphertext:", end = "")
    
    for symbol in plaintext:
        if symbol.isalpha():
            key = ord(sys.argv[1][keyIndex % length].lower()) - 97
            keyIndex += 1
            translated.append(caesar(symbol, key))
        else:
            translated.append(symbol)
    
    print("".join(translated))
    exit(0)
    
def caesar(char, key):
    if char.isupper():
        return chr(((ord(char) - 65 + key) % 26) + 65)
    else:
        return chr(((ord(char) - 97 + key) % 26) + 97)

if __name__ == "__main__":
    main()
