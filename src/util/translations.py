"""Translation dictionary module for the Mastermind game.

This module contains translations for all game text in multiple languages
(en, de, fr, ko).
Each language contains key-value pairs for every text element in the game.

Attributes:
    translations (dict): A nested dictionary containing all translations.
        Structure:
        {
            "language_code": {
                "text_key": "translated_text",
                ...
            },
            ...
        }

Available Languages:
    - en: English
    - de: German
    - fr: French
    - ko: Korean
"""
import os

translations = {
    "en": {
        "main_menu": "Main Menu",
        "ingame_menu": "Menu",
        "start_game": "Start Game",
        "start_offline_game": "1. Start Offline Game",
        "start_online_game": "2. Start Online Game",
        "change_language": "Change Language",
        "end_game": "End Game",
        "save_game": "Save Game",
        "resume_game": "Resume Interrupted Game",
        "select_game_mode": "Select game mode:",
        "offline_guesser": "Start Offline Game as guesser",
        "offline_coder": "Start Offline Game as coder",
        "online_guesser": "Start Online Game as guesser",
        "back_to_menu": "Back to Main Menu",
        "select_language": "Select a language:",
        "language_en": "English",
        "language_de": "German",
        "language_fr": "French",
        "language_ko": "Korean",
        "game_ended": "Game ended.",
        "game_saved": "Game saved.",
        "loads_resumed_game": "loads resumed game",
        "game_started": "Game started.",
        "available_colors": "Available colors and their codes:",
        "give_feedback": "Give feedback for the guess:",
        "feedback_instructions":
            f"8: Black (correct color in correct position){os.linesep}"
            f"7: White (correct color in wrong position){os.linesep}"
            f" Enter feedback (e.g. 887 for two black, one white):",
        "secret_code": "Secret Code",
        "game_title": "Super Mastermind",
        "round": "Round",
        "feedback": "Feedback",
        "guess": "Guess",
        "warning": "WARNING",
        "enter_secret_code": "Enter input for secret code ({} digits): ",
        "enter_guess": "Enter your guess ({} digits): ",
        "enter_feedback": "Enter feedback ({} digits): ",
        "enter_command": "Enter command: ",
        "enter_game_mode": "Enter game mode: ",
        "enter_server_ip": "Enter server IP address:",
        "enter_server_port": "Enter server port:",
        "connecting": "Connecting to server...",
        "connection_failed": "Connection failed!",
        "cheating_warning": "CHEATING DETECTED!",
        "pick_player_name": "Pick a player name",
        "pick_positions": "Pick with how many positions you want to play",
        "pick_colors": "Pick how many colors you want to play with",
        "pick_max_attempts": "Pick the maximum number of attempts",
        "enter_player_name": "Enter player name: ",
        "enter_positions": "Enter number of positions: ",
        "enter_colors": "Enter number of colors: ",
        "enter_max_attempts": "Enter maximum number of attempts: ",
        "save_warning": "Warning: A saved game already exists "
        "and will be overwritten. Continue?",
        "yes": "Yes",
        "no": "No",
        "player_label": "Player:",
        "settings_label": "Settings:",
        "settings_format": "{} positions, {} colors, {} attempts",
        "invalid_configuration": "Invalid configuration. "
        "Please check your input values.",
        "game_won": f"Congratulations! You've won the game!{os.linesep}"
                    f"Return to main menu in 3 seconds...",
        "game_lost": f"Game Over! You've reached the maximum number of attempts."
                     f"{os.linesep}"f"Return to main menu in 3 seconds...",
        "menu_hint": "Type 'menu' to open the game menu",
        "computer_online_guesser": "Let the computer guess (online)"
    },
    "de": {
        "main_menu": "Hauptmenü",
        "ingame_menu": "Menü",
        "start_game": "Spiel starten",
        "start_offline_game": "Offline-Spiel starten",
        "start_online_game": "Online-Spiel starten",
        "change_language": "Sprache ändern",
        "end_game": "Spiel beenden",
        "save_game": "Spiel speichern",
        "resume_game": "Unterbrochenes Spiel fortsetzen",
        "select_game_mode": "Wähle den Spielmodus:",
        "offline_guesser": "Starte Offline-Spiel als Rater",
        "offline_coder": "Starte Offline-Spiel als Codierer",
        "online_guesser": "Starte Online-Spiel als Rater",
        "back_to_menu": "Zurück zum Hauptmenü",
        "select_language": "Wähle eine Sprache:",
        "language_en": "Englisch",
        "language_de": "Deutsch",
        "language_fr": "Französisch",
        "language_ko": "Koreanisch",
        "game_ended": "Spiel beendet.",
        "game_saved": "Spiel gespeichert.",
        "loads_resumed_game": "lädt fortgesetztes Spiel",
        "game_started": "Spiel gestartet.",
        "available_colors": "Verfügbare Farben und ihre Codes:",
        "give_feedback": "Gib Feedback für den Tipp:",
        "feedback_instructions": f"8: Schwarz (richtige Farbe an richtiger Position)"
                                 f"{os.linesep}"
                                 f"7: Weiß (richtige Farbe an falscher Position)"
                                 f"{os.linesep}"
                                 f"Gib Feedback ein "
                                 f"(z.B. 887 für zwei Schwarz, ein Weiß):",
        "secret_code": "Geheimer Code",
        "game_title": "Super Superhirn",
        "round": "Runde",
        "feedback": "Feedback",
        "guess": "Tipp",
        "warning": "WARNUNG",
        "enter_secret_code": "Geben Sie den geheimen Code ein ({} Ziffern): ",
        "enter_guess": "Geben Sie Ihren Tipp ein ({} Ziffern): ",
        "enter_feedback": "Geben Sie das Feedback ein ({} Ziffern): ",
        "enter_command": "Befehl eingeben: ",
        "enter_game_mode": "Spielemodus eingeben: ",
        "enter_server_ip": "Server IP-Adresse eingeben:",
        "enter_server_port": "Server Port eingeben:",
        "connecting": "Verbinde mit Server...",
        "connection_failed": "Verbindung fehlgeschlagen!",
        "cheating_warning": "BETRUG ERKANNT!",
        "pick_player_name": "Wähle einen Spielernamen",
        "pick_positions": "Wähle mit wie vielen Positionen du spielen möchtest",
        "pick_colors": "Wähle mit wie vielen Farben du spielen möchtest",
        "pick_max_attempts": "Wähle die maximale Anzahl an Versuchen",
        "enter_player_name": "Geben Sie den Spielernamen ein: ",
        "enter_positions": "Geben Sie die Anzahl der Positionen ein: ",
        "enter_colors": "Geben Sie die Anzahl der Farben ein: ",
        "enter_max_attempts": "Geben Sie die maximale Anzahl an Versuchen ein: ",
        "save_warning": "Warnung! Ein gespeichertes Spiel existiert bereits "
        "und wird überschrieben. Fortfahren?",
        "yes": "Ja",
        "no": "Nein",
        "player_label": "Spieler:",
        "settings_label": "Einstellungen:",
        "settings_format": "{} Positionen, {} Farben, {} Versuche",
        "invalid_configuration": "Ungültige Konfiguration."
        " Bitte überprüfen Sie Ihre Eingaben",
        "game_won": f"Herzlichen Glückwunsch! Sie haben das Spiel gewonnen!{os.linesep}"
                    f"Kehre in 3 Sekunden zum Hauptmenü zurück...",
        "game_lost": f"Spiel vorbei, sie haben Verloren!{os.linesep}"
                     f"Kehre in 3 Sekunden zum Hauptmenü zurück... "
        "Sie haben die maximale Anzahl an Versuchen erreicht.",
        "menu_hint": "Tippe 'menu' um das Spielmenü zu öffnen",
        "computer_online_guesser": "Lass den Computer raten (online)"
            },
    "fr": {
        "main_menu": "Menu Principal",
        "ingame_menu": "Menu",
        "start_game": "Démarrer le jeu",
        "start_offline_game": "1. Démarrer un jeu hors ligne",
        "start_online_game": "2. Démarrer un jeu en ligne",
        "change_language": "Changer de langue",
        "end_game": "Terminer le jeu",
        "save_game": "Sauvegarder le jeu",
        "resume_game": "Reprendre le jeu interrompu",
        "select_game_mode": "Sélectionnez le mode de jeu:",
        "offline_guesser": "Démarrer un jeu hors ligne en tant que devineur",
        "offline_coder": "Démarrer un jeu hors ligne en tant que codeur",
        "online_guesser": "Démarrer un jeu en ligne en tant que devineur",
        "back_to_menu": "Retour au menu principal",
        "select_language": "Sélectionnez une langue:",
        "language_en": "Anglais",
        "language_de": "Allemand",
        "language_fr": "Français",
        "language_ko": "Coréen",
        "game_ended": "Jeu terminé.",
        "game_saved": "Jeu sauvegardé.",
        "loads_resumed_game": "charge le jeu repris",
        "game_started": "Jeu démarré.",
        "available_colors": "Couleurs disponibles et leurs codes:",
        "give_feedback": "Donnez un retour pour la supposition:",
        "feedback_instructions": f"8: Noir (couleur correcte à la bonne position)"
                                 f"{os.linesep}"
                                 f"7: Blanc (couleur correcte à la mauvaise position"
                                 f"{os.linesep}"
                                 f"Entrez le retour (par exemple 887 pour deux noirs,"
                                 f"un blanc):",
        "secret_code": "Code Secret",
        "game_title": "Super Super cerveau",
        "round": "Tour",
        "feedback": "Retour",
        "guess": "Supposition",
        "warning": "AVERTISSEMENT",
        "enter_secret_code": "Entrez le code secret ({} chiffres): ",
        "enter_guess": "Entrez votre supposition ({} chiffres): ",
        "enter_feedback": "Entrez le retour ({} chiffres): ",
        "enter_command": "Entrez la commande: ",
        "enter_game_mode": "Entrez le mode de jeu: ",
        "enter_server_ip": "Entrez l'adresse IP du serveur:",
        "enter_server_port": "Entrez le port du serveur:",
        "connecting": "Connexion au serveur...",
        "connection_failed": "Échec de la connexion!",
        "cheating_warning": "TRICHERIE DÉTECTÉE!",
        "pick_player_name": "Choisissez un nom de joueur",
        "pick_positions": "Choisissez avec combien de positions vous voulez jouer",
        "pick_colors": "Choisissez avec combien de couleurs vous voulez jouer",
        "pick_max_attempts": "Choisissez le nombre maximum de tentatives",
        "enter_player_name": "Entrez le nom du joueur: ",
        "enter_positions": "Entrez le nombre de positions: ",
        "enter_colors": "Entrez le nombre de couleurs: ",
        "enter_max_attempts": "Entrez le nombre maximum de tentatives: ",
        "save_warning": "Attention! Un jeu sauvegardé existe déjà ",
        "yes": "Oui",
        "no": "Non",
        "player_label": "Joueur:",
        "settings_label": "Paramètres:",
        "settings_format": "{} positions, {} couleurs, {} tentatives",
        "invalid_configuration": "Configuration invalide. ",
        "game_won": f"Félicitations! Vous avez gagné la partie!{os.linesep}"
                    f"Retour au menu principal dans 3 secondes...",
        "game_lost": f"Partie terminée! Vous avez atteint le nombre maximum "
                     f"de tentatives.{os.linesep}"
                     f"Retour au menu principal dans 3 secondes...",
        "menu_hint": "Tapez 'menu' pour ouvrir le menu du jeu",
        "computer_online_guesser": "TODO"

    },
    "ko": {
        "main_menu": "메인 메뉴",
        "ingame_menu": "메뉴",
        "start_game": "게임 시작",
        "start_offline_game": "1. 오프라인 게임 시작",
        "start_online_game": "2. 온라인 게임 시작",
        "change_language": "언어 변경",
        "end_game": "게임 종료",
        "save_game": "게임 저장",
        "resume_game": "중단된 게임 재개",
        "select_game_mode": "게임 모드 선택:",
        "offline_guesser": "오프라인 게임으로 추측자로 시작",
        "offline_coder": "오프라인 게임으로 코드 작성자로 시작",
        "online_guesser": "온라인 게임으로 추측자로 시작",
        "back_to_menu": "메인 메뉴로 돌아가기",
        "select_language": "언어를 선택하세요:",
        "language_en": "영어",
        "language_de": "독일어",
        "language_fr": "프랑스어",
        "language_ko": "한국어",
        "game_ended": "게임 종료.",
        "game_saved": "게임 저장됨.",
        "loads_resumed_game": "중단된 게임을 불러옵니다",
        "game_started": "게임 시작됨.",
        "available_colors": "사용 가능한 색상 및 코드:",
        "give_feedback": "추측에 대한 피드백을 제공하세요:",
        "feedback_instructions": f"8: 검정 (올바른 위치에 올바른 색상){os.linesep}"
                                 f"7: 흰색 (잘못된 위치에 올바른 색상){os.linesep}"
                                 f"피드백 입력 (예: 두 개의 검정, 하나의 흰색을 위해 887 입력):",
        "secret_code": "비밀 코드",
        "game_title": "슈퍼 슈퍼히른",
        "round": "라운드",
        "feedback": "피드백",
        "guess": "추측",
        "warning": "경고",
        "enter_secret_code": "비밀 코드를 입력하세요 ({}자리 숫자): ",
        "enter_guess": "추측을 입력하세요 ({}자리 숫자): ",
        "enter_feedback": "피드백을 입력하세요 ({}자리 숫자): ",
        "enter_command": "명령을 입력하세요: ",
        "enter_game_mode": "게임 모드를 입력하세요: ",
        "enter_server_ip": "서버 IP 주소를 입력하세요:",
        "enter_server_port": "서버 포트를 입력하세요:",
        "connecting": "서버에 연결 중...",
        "connection_failed": "연결 실패!",
        "cheating_warning": "사기 감지됨!",
        "pick_player_name": "플레이어 이름을 선택하세요",
        "pick_positions": "플레이할 위치 수를 선택하세요",
        "pick_colors": "플레이할 색상 수를 선택하세요",
        "pick_max_attempts": "최대 시도 횟수를 선택하세요",
        "enter_player_name": "플레이어 이름을 입력하세요: ",
        "enter_positions": "위치 수를 입력하세요: ",
        "enter_colors": "색상 수를 입력하세요: ",
        "enter_max_attempts": "최대 시도 횟수를 입력하세요: ",
        "save_warning": "경고! 저장된 게임이 이미 존재합니다 ",
        "yes": "예",
        "no": "아니요",
        "player_label": "플레이어:",
        "settings_label": "설정:",
        "settings_format": "{} 위치, {} 색상, {} 시도",
        "invalid_configuration": "잘못된 구성입니다. ",
        "game_won": f"축하합니다! 게임에서 승리했습니다!{os.linesep}3초 후 메인 메뉴로 돌아갑니다...",
        "game_lost": f"게임 오버! 최대 시도 횟수에 도달했습니다.{os.linesep}3초 후 메인 메뉴로 돌아갑니다...",
        "menu_hint": "게임 메뉴를 열려면 'menu'를 입력하세요",
        "computer_online_guesser": "TODO"
    },
}
