# example.py
# Dieses Skript zeigt einfache Funktionen für Begrüßung und Addition.

def greet(name):
    """
    Gibt eine Begrüßung für den angegebenen Namen aus.

    Args:
        name (str): Der Name der Person, die begrüßt wird.
    """
    print("Hello, " + name)


def add_numbers(a, b):
    """
    Addiert zwei Zahlen und gibt das Ergebnis aus..

    Args:
        a (int or float): Die erste Zahl.
        b (int or float): Die zweite Zahl.
    """
    result = a + b
    print(result)


if __name__ == "__main__":
    # Begrüßung ausgeben
    greet("World")

    # Zwei Zahlen addieren und das Ergebnis ausgeben
    add_numbers(3, 4)
