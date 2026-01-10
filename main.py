#!/usr/bin/env python3
"""
Oldham Quiz - Main entry point.

A multi-player quiz game about Oldham Athletic Football Club.
"""

from oldham_quiz import (
    Colours,
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

    print(f"\n{Colours.BOLD}{Colours.CYAN}=== OLDHAM QUIZ ==={Colours.RESET}")
    print(f"{Colours.WHITE}Copyright (C) 2026 DecBr1{Colours.RESET}")
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
        print(f"{Colours.BOLD}{Colours.CYAN}MAIN MENU{Colours.RESET}")
        print(f"1. {Colours.GREEN}Start New Game{Colours.RESET}")
        print(f"2. {Colours.YELLOW}View High Scores{Colours.RESET}")
        print(f"3. {Colours.RED}Exit{Colours.RESET}")

        choice = input("\nSelect option (1-3): ").strip()

        if choice == '2':
            # View high scores
            print()
            print(f"1. {Colours.CYAN}All Scores{Colours.RESET}")
            print(f"2. {Colours.CYAN}Single Player Only{Colours.RESET}")
            print(f"3. {Colours.CYAN}Multiplayer Only{Colours.RESET}")
            print(f"4. {Colours.CYAN}Back to Main Menu{Colours.RESET}")

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
            print(f"\n{Colours.CYAN}Thanks for playing!{Colours.RESET}\n")
            break

        elif choice == '1':
            # start game
            print()
            num_players = 0
            while num_players < 1 or num_players > 3:
                try:
                    num_players = int(input("How many players? (1-3): "))
                    if num_players < 1 or num_players > 3:
                        print(f"{Colours.RED}Please enter a number between 1 and 3.{Colours.RESET}")
                except ValueError:
                    print(f"{Colours.RED}Please enter a valid number.{Colours.RESET}")

            print()

            if num_players == 1:
                game = SinglePlayerGame(questions, num_players, high_score_db)
            else:
                game = MultiPlayerGame(questions, num_players, high_score_db)

            game.run()

            # high score after game over logic
            print()
            view_scores = input(f"{Colours.YELLOW}View high scores? (y/n): {Colours.RESET}").strip().lower()
            if view_scores == 'y':
                high_score_db.display_leaderboard()
                input("\nPress Enter to continue...")
        else:
            print(f"{Colours.RED}Invalid option. Please select 1, 2, or 3.{Colours.RESET}")


if __name__ == "__main__":
    main()

