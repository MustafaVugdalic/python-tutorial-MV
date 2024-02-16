from gpiozero import LED
from time import sleep
import sys
file_path = sys.argv[1]  #prende argomento da linea di comando

#print(file_path)

file = open(file_path,'r')  


stringa = file.read()

morse_dict = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
    'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
    'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.', '.': '.-.-.-', ',': '--..--',
    '?': '..--..', "'": '.----.', '!': '-.-.--', '/': '-..-.', '(': '-.--.', ')': '-.--.-', '&': '.-...',
    ':': '---...', ';': '-.-.-.', '=': '-...-', '+': '.-.-.', '-': '-....-', '_': '..--.-', '"': '.-..-.',
    '$': '...-..-', '@': '.--.-.', 
    'è': '.', 'é': '.', 'à': '.-', 'ù': '..-', 'ì': '..', 'ò': '---',  #filtro per lettere italiane, trattali come quei normali
}

morse_dict = {k.lower(): v for k, v in morse_dict.items()} #trasforma in maiuscolo

def encrypt(message):
    cipher = ''
    for letter in message.lower():
        if letter in morse_dict:
            cipher += morse_dict[letter] + ' ' #spazio tra le lettere
        elif letter == ' ':
            cipher += '/' #spazio tra le parole
    return cipher

led=LED(17)

oneUnit = 0.1 # un unita di tempo
def lampeggia(mors):
    for letter in mors:
        if letter == ' ': 
            led.off()
            sleep(3*oneUnit) #spazio tra le lettere di Stessa parola
        elif letter == '.': 
            led.on()
            sleep(oneUnit) #shortmark
            led.off()
            sleep(oneUnit)  #interelement gap
        elif letter == '-':
            led.on()
            sleep(3*oneUnit) #longmark
            led.off()
            sleep(oneUnit) #interelement gap
        elif letter == '/':
            led.off()
            sleep(5*oneUnit) #spazio tra le parole 


print(encrypt(stringa))

lampeggia(encrypt(stringa))