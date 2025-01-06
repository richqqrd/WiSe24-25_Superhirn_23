# Mastermind/Superhirn Implementation

## Beschreibung
Eine Python-Implementierung des klassischen Mastermind/Superhirn Spiels mit mehreren Spielmodi und Features:

- Offline und Online Spielmöglichkeiten mit [`NetworkService`](src/network/network_service.py)
- Computer-Gegner mit [`ComputerGuesser`](src/business_logic/guesser/computer_guesser.py) (Knuth's Algorithmus)
- Mehrsprachige Unterstützung (DE, EN, FR, KO) via [`translations.py`](src/util/translations.py)
- Speichern/Laden von Spielständen mit [`PersistenceManager`](src/persistence/persistence_manager.py)
- Konfigurierbare Spielparameter

## Architektur
Das Projekt verwendet eine Schichtenarchitektur:

1. **Presentation Layer** ([`cli`](src/cli/)):
- [`Console`](src/cli/console.py): Hauptbenutzeroberfläche
- [`MenuRenderer`](src/cli/menu_renderer/menu_renderer.py): Menüdarstellung
- [`GameRenderer`](src/cli/game_renderer/game_renderer.py): Spieldarstellung

2. **Application Layer**:
- [`ApplicationLogic`](src/application_logic/application_logic.py): Spielablaufsteuerung

3. **Business Layer**:
- [`BusinessLogic`](src/business_logic/business_logic.py): Kernspiellogik

4. **Infrastructure Layer**:
- [`network`](src/network/): Online-Spielfunktionalität
- [`persistence`](src/persistence/): Speichermanagement

## Installation
```bash
# Abhängigkeiten installieren
pip install -r requirements.txt

# Spiel starten
python src/main.py
```

## Testing 
```bash
# Tests ausführen
pytest tests/

# Coverage Report erstellen
coverage run -m pytest tests/
coverage report
```