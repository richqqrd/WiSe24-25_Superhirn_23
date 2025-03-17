# Mastermind/Superhirn Implementation

## Course Information
This project was developed as part of the Software Engineering 2 course by Prof. Dr. Salinger.
**Grade: 1.7**


## Description
A Python implementation of the classic Mastermind/Superhirn game with multiple game modes and features:

- Offline and online gameplay options using [`NetworkService`](src/network/network_service.py)
- Computer opponent with [`ComputerGuesser`](src/business_logic/guesser/computer_guesser.py) (Knuth's algorithm)
- Multi-language support (DE, EN, FR, KO) via [`translations.py`](src/util/translations.py)
- Save/load game states with [`PersistenceManager`](src/persistence/persistence_manager.py)
- Configurable game parameters

## Architecture
The project uses a layered architecture:

1. **Presentation Layer** ([`cli`](src/cli/)):
- [`Console`](src/cli/console.py): Main user interface
- [`MenuRenderer`](src/cli/menu_renderer/menu_renderer.py): Menu rendering
- [`GameRenderer`](src/cli/game_renderer/game_renderer.py): Game rendering

2. **Application Layer**:
- [`ApplicationLogic`](src/application_logic/application_logic.py): Game flow control

3. **Business Layer**:
- [`BusinessLogic`](src/business_logic/business_logic.py): Core game logic

4. **Infrastructure Layer**:
- [`network`](src/network/): Online gameplay functionality
- [`persistence`](src/persistence/): Storage management

## CI/CD Pipeline
This project utilizes a GitLab CI/CD pipeline with the following stages:

1. **Lint**: 
   - Runs Flake8 on source code and tests to ensure code quality and adherence to PEP8 standards
   - Only executes on merge requests
   - Enforced as a required check (non-allowable failure)

2. **Test**:
   - Executes all tests using pytest
   - Generates comprehensive test coverage reports

The pipeline runs on Python 3.9 and automatically installs all dependencies from requirements.txt before execution. It's configured to use Linux runners with Python support.

The complete pipeline configuration can be found in the [.gitlab-ci.yml](.gitlab-ci.yml) file.

## Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Start the game
python3 src/main.py
```

## Testing 
```bash
# Run tests
pytest tests/

# Create coverage report
coverage run -m pytest tests/
coverage report
```

## Dokumentation
```bash
# Install pdoc3
pip install pdoc3

# Generate local documentation
pdoc --html src/* -o docs