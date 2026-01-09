import json
import sys

# Platform-specific key press detection
if sys.platform.startswith('win'):
    import msvcrt
    
    def wait_for_buzz():
        """wait for Q, P, or B key press on windows."""
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getch().decode('utf-8').upper()
                if key in ('Q', 'P', 'B'):
                    return key
else:
    import tty
    import termios
    
    def wait_for_buzz():
        """wait for Q, P, or B key press on *nix."""
        
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                key = sys.stdin.read(1).upper()
                if key in ('Q', 'P', 'B'):
                    return key
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def setup_players():
    """get player names. returns dictionary of players."""
    
    players = {}
    key_map = {'Q': None, 'P': None, 'B': None}
    
    print("=== oldham quiz ===\n")
    num_players = 0

    while num_players < 1 or num_players > 3:
        try:
            num_players = int(input("How many players? (1-3): "))
            if num_players < 1 or num_players > 3:
                print("Please enter a number between 1 and 3.")
        except ValueError:
            print("Please enter a valid number.")
    
    keys = ('Q', 'P', 'B')
    
    for i in range(num_players):
        if num_players == 1:
            name = input("Player name: ").strip()
        else:
            name = input(f"Player {i+1} (Key: {keys[i]}): ").strip()
        
        if not name:
            name = f"Player {i+1}"
        
        players[keys[i]] = {
            'name': name,
            'score': 0
        }
        key_map[keys[i]] = name
    
    if num_players > 1:
        print("\n" + "=" * 50)
        print("BUZZER KEYS:")
        for key, player in players.items():
            print(f"  {key} - {player['name']}")
        print("=" * 50 + "\n")
    
    return players


def display_question(index, show_buzz=True):
    """print question and options. Returns question answer."""
    
    print(f"\nQuestion {QUESTIONS[index]['question_index']}: {QUESTIONS[index]['question']}")
    for option in QUESTIONS[index]['options']:
        print(f"  {option}")
    
    return QUESTIONS[index]['answer']


def get_valid_answer():
    """get a valid answer (A, B, or C) from the user."""
    
    while True:
        user_answer = input("Answer >> ").upper().strip()
        if user_answer in ('A', 'B', 'C'):
            return user_answer
        else:
            print("Invalid input! Please enter A, B, or C.")


def display_scores(players):
    """display current scores for all players."""
    
    print("\n" + "-" * 50)
    print("CURRENT SCORES:")
    for key, player in sorted(players.items()):
        print(f"  {player['name']}: {player['score']}")
    print("-" * 50)


def main():
    players = setup_players()
    single_player = len(players) == 1
    
    for i in range(len(QUESTIONS)):
        correct_answer = display_question(i, show_buzz=not single_player)
        question_answered = False
        attempts = 0
        first_buzzer = None
        
        if single_player:
            # Single player mode - just answer directly
            player_key = list(players.keys())[0]
            buzzing_player = players[player_key]
            user_answer = get_valid_answer()
            
            if user_answer == correct_answer:
                buzzing_player['score'] += 1
                print(f"Correct. +1 point to {buzzing_player['name']}")
            else:
                print(f"Incorrect. The correct answer was {correct_answer}")
            
            question_answered = True
            
        else:
            # Multiplayer mode - allow up to 2 attempts
            while not question_answered and attempts < 2:
                print("\nBUZZ IN WITH YOUR KEY")
                buzzer_key = wait_for_buzz()
                
                if buzzer_key not in players:
                    print(f"\nKey {buzzer_key} is not assigned to a player.")
                    continue
                
                # check if this is the same player who already tried
                if attempts == 1 and buzzer_key == first_buzzer:
                    print(f"{players[buzzer_key]['name']} already attempted this question.")
                    continue
                
                buzzing_player = players[buzzer_key]
                print(f"\n{buzzing_player['name']} buzzed in.")
                
                if attempts == 0:
                    first_buzzer = buzzer_key
                
                # Get their answer
                user_answer = get_valid_answer()
                attempts += 1
                
                if user_answer == correct_answer:
                    buzzing_player['score'] += 1
                    if attempts == 1:
                        print(f"Correct. +1 point to {buzzing_player['name']}")
                    else:
                        print(f"Correct! Steal successful. +1 point to {buzzing_player['name']}")
                    question_answered = True
                else:
                    if attempts == 1:
                        print("Incorrect. Steal opportunity available.")
                    else:
                        print(f"Incorrect. The correct answer was {correct_answer}")
                        print("Question skipped.")
                        question_answered = True
        
        display_scores(players)
        
        if i < len(QUESTIONS) - 1:
            input("\nPress Enter for next question...")
    
    # Final results
    print("\n" + "=" * 50)
    print("FINAL RESULTS")
    print("=" * 50)
    
    # Sort players by score (descending)
    sorted_players = sorted(players.items(), key=lambda x: x[1]['score'], reverse=True)
    
    for rank, (key, player) in enumerate(sorted_players, 1):
        percentage = (player['score'] / len(QUESTIONS)) * 100
        print(f"{rank}. {player['name']}: {player['score']}/{len(QUESTIONS)} ({percentage:.1f}%)")
    
    if not single_player:
        winner = sorted_players[0][1]
        print(f"\nWinner: {winner['name']} with {winner['score']} points")
    print("=" * 50)

if __name__ == "__main__":
    with open('questions.json', 'r', encoding='utf-8') as f:
        QUESTIONS = json.load(f)
    
    main()