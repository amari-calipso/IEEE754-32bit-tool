"""
IEEE754 32bit Tool 2021 Copyright (C) thatsOven
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import colorama

def IEEE754ToBinary(number):
    sign     = -1 if number[0] == 1 else 1
    exp      = int(number[1:9], 2) - 127
    mantissa = number[9:32]
    if exp >= 0:
        integerPart = int("1" + mantissa[:exp], 2)
        decimalPart = mantissa[exp:]
    else:
        integerPart = 0
        exp = -exp - 1
        decimalPart = ("0" * exp) + "1" + mantissa
    return sign, integerPart, decimalPart

def binaryDecimalToFloat(number):
    i = 1
    result = 0
    while i - 1 < len(number):
        result += int(number[i - 1]) * (2 ** (-i)) 
        i += 1
    return result

def IEEE754ToFloat(number):
    sign, integerPart, decimalPart = IEEE754ToBinary(number)
    return sign * (integerPart + binaryDecimalToFloat(decimalPart))

def floatDecimalToBinary(number):
    i = 1
    finalString = ""
    while number != 0.0 and i < 23:
        number *= 2
        finalString += str(int(number))
        if number >= 1: number -= 1
        i += 1

    return finalString

def floatToBinary(number):
    if number < 0:
        sign = "1"
        number = -number
    else: sign = "0"
    return sign, bin(int(number))[2:] + "." + floatDecimalToBinary(number - int(number))

def getUntilDot(number, charPtr):
    while number[charPtr] != ".":
        charPtr += 1
    return charPtr - 1

def binaryToIEEE754(sign, number):
    if number[0] == "1":
        exp = bin(getUntilDot(number, 1) + 127)[2:]
        mantissa = number.replace(".", "")[1:]
    else:
        charPtr = 1
        while number[charPtr] != "1":
            charPtr += 1
        charPtr -= 1
        exp = bin(127 - charPtr)[2:]
        mantissa = number[charPtr + 2:]

    while len(exp) < 8:
        exp = "0" + exp

    if len(mantissa) < 23:
        while len(mantissa) < 23:
            mantissa += "0"
    else: mantissa = mantissa[:23]
    return sign + exp + mantissa

def floatToIEEE754(number):
    sign, binary = floatToBinary(number)
    return binaryToIEEE754(sign, binary)

# Internal program functions
def normalize(number):
    return number.replace(" ", "")

def takeNumber(message):
    while True:
        print(message)
        a = normalize(input().strip())
        try:    testing = float(a)
        except: print("Invalid number, retry.")
        else:
            if ieee and len(a) != 32:
                print("Invalid number, retry.")
            else: return a

def select(options):
    while True:
        print("Select:")
        for i in range(len(options)):
            print(str(i + 1) + ") " + options[i])
        sel = input()
        try: testing = int(sel)
        except: pass
        else:
            sel = int(sel)
            if sel in range(1, len(options) + 1): return sel

        print("Invalid option, retry.")

def prettifyMantissa(mantissa):
    return mantissa[:4] + " " + mantissa[4:8] + " " + mantissa[8:12] + " " + mantissa[12:16] + " " + mantissa[16:20] + " " + mantissa[20:23]

def prettyPrint(number):
    print(colorama.Fore.GREEN + number[0],   end="  ")
    print(colorama.Fore.RED   + number[1:9], end="  ")
    print(colorama.Fore.CYAN  + prettifyMantissa(number[9:32]))
    print(colorama.Style.RESET_ALL)

if __name__ == "__main__":
    colorama.init()
    print("thatsOven's IEEE754 32bit tool")

    sel = select(["Solve expressions",
                  "Convert"])

    if sel == 1:

        sel = select(["Expressions with decimal numbers",
                      "Expressions with IEEE754 numbers"])

        if sel == 1:
            while True:
                print("Insert expression:")
                op = input()
                try: testing = eval(op)
                except: print("Invalid expression, retry.")
                else:
                    print("Result:", end=" ")
                    prettyPrint(floatToIEEE754(float(eval(op))))
                    break
        else:
            v1 = takeNumber("Insert first number")

            while True:
                print("Insert operator:")
                op = normalize(input().strip())

                if op in ["+", "-", "*", "/", "**"]: break
                print("Invalid operator, retry.")
                
            v2 = takeNumber("Insert second number")

            v1 = str(IEEE754ToFloat(normalize(v1)))
            v2 = str(IEEE754ToFloat(normalize(v2)))
            
            print("Result:", end=" ")
            prettyPrint(str(floatToIEEE754(float(eval(v1 + op + v2)))))
    else:

        sel = select(["From decimal to IEEE754",
                      "From IEEE754 to decimal"])

        if sel == 1:
            v = takeNumber("Insert number to convert")

            print("Result:", end=" ")
            prettyPrint(str(floatToIEEE754(float(v))))
        else:
            v = takeNumber("Insert number to convert")

            print("Result: " + str(IEEE754ToFloat(normalize(v))))
