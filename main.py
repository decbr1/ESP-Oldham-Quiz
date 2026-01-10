#!/usr/bin/env python3
"""
Oldham Quiz - Main entry point.

A multi-player quiz game about Oldham Athletic Football Club.
"""

from oldham_quiz import (
    Colours as C,
    HighScoreDatabase,
    SinglePlayerGame,
    MultiPlayerGame,
    load_questions,
    show_warranty,
    show_conditions,
)


def main():
    """Main entry point for the quiz game."""
    questions = load_questions('questions.json')
    high_score_db = HighScoreDatabase()

    print(f"\n{C.BOLD}{C.CYAN}=== OLDHAM QUIZ ==={C.RESET}")
    print(f"{C.WHITE}Copyright (C) 2026 DecBr1{C.RESET}")
    print("This program comes with ABSOLUTELY NO WARRANTY; for details type 'w'.")
    print("This is free software, and you are welcome to redistribute it under certain conditions; for details type 'c'.\n")
    response = input("Press Enter to continue, or type 'w' or 'c': ").strip().lower()
    if response == 'w':
        show_warranty()
        input("\nPress Enter to continue...")
    elif response == 'c':
        show_conditions()
        input("\nPress Enter to continue...")

    # Main menu loop
    while True:
        print()
        print(f"{C.BOLD}{C.CYAN}MAIN MENU{C.RESET}")
        print(f"1. {C.GREEN}Start New Game{C.RESET}")
        print(f"2. {C.YELLOW}View High Scores{C.RESET}")
        print(f"3. {C.RED}Exit{C.RESET}")

        choice = input("\nSelect option (1-3): ").strip()

        if choice == '2':
            # View high scores
            print()
            print(f"1. {C.CYAN}All Scores{C.RESET}")
            print(f"2. {C.CYAN}Single Player Only{C.RESET}")
            print(f"3. {C.CYAN}Multiplayer Only{C.RESET}")
            print(f"4. {C.CYAN}Back to Main Menu{C.RESET}")

            view_choice = input("\nSelect option (1-4): ").strip()

            if view_choice == '1':
                high_score_db.display_leaderboard()
                input("Press Enter to continue...")
            elif view_choice == '2':
                high_score_db.display_leaderboard(game_mode='single')
                input("Press Enter to continue...")
            elif view_choice == '3':
                high_score_db.display_leaderboard(game_mode='multiplayer')
                input("Press Enter to continue...")
            continue

        elif choice == '3':
            # exit Game
            print(f"\n{C.CYAN}Thanks for playing!{C.RESET}\n")
            break

        elif choice == '1':
            # start game
            print()
            num_players = 0
            while num_players < 1 or num_players > 3:
                try:
                    num_players = int(input("How many players? (1-3): "))
                    if num_players < 1 or num_players > 3:
                        print(f"{C.RED}Please enter a number between 1 and 3.{C.RESET}")
                except ValueError:
                    print(f"{C.RED}Please enter a valid number.{C.RESET}")

            print()

            if num_players == 1:
                game = SinglePlayerGame(questions, num_players, high_score_db)
            else:
                game = MultiPlayerGame(questions, num_players, high_score_db)

            game.run()

            # high score after game over logic
            print()
            view_scores = input(f"{C.YELLOW}View high scores? (y/n): {C.RESET}").strip().lower()
            if view_scores == 'y':
                high_score_db.display_leaderboard()
                input("\nPress Enter to continue...")
        else:
            print(f"{C.RED}Invalid option. Please select 1, 2, or 3.{C.RESET}")


if __name__ == "__main__":
    main()

