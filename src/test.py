# example.py
import os

def greet(name):   # Funktion definiert, aber die Konventionen ignoriert
    print("Hello, " + name)

def add_numbers(a,b):  # Parameter ohne Leerzeichen
    result=a+b   # Variablen ohne Leerzeichen
    print(result)

if __name__ == "__main__":
    greet("World")
    add_numbers(3,4)  # Testaufruf ohne Leerzeichen
