#!/usr/bin/env python3
"""
Oldham Quiz - Main entry point.

A multi-player quiz game about Oldham Athletic Football Club.
"""
from oldham_quiz.colours import c, Colours
from oldham_quiz import (
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

    print(c("\n=== OLDHAM QUIZ ===").bold.cyan)
    print(c("Copyright (C) 2026 DecBr1").white)
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
        print(c("MAIN MENU").bold.cyan)
        print(c("1. Start New Game").green)
        print(c("2. View High Scores").yellow)
        print(c("3. Exit").red)

        choice = input("\nSelect option (1-3): ").strip()

        if choice == '2':
            # View high scores
            print()
            print(c("1. All Scores").cyan)
            print(c("2. Single Player Only").cyan)
            print(c("3. Multiplayer Only").cyan)
            print(c("4. Back to Main Menu").cyan)

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
            print(c("\nThanks for playing!\n").cyan)
            break

        elif choice == '1':
            # start game
            print()
            num_players = 0
            while num_players < 1 or num_players > 3:
                try:
                    num_players = int(input("How many players? (1-3): "))
                    if num_players < 1 or num_players > 3:
                        print(c("Please enter a number between 1 and 3.").red)
                except ValueError:
                    print(c("Please enter a valid number.").red)

            print()

            if num_players == 1:
                game = SinglePlayerGame(questions, num_players, high_score_db)
            else:
                game = MultiPlayerGame(questions, num_players, high_score_db)

            game.run()

            # high score after game over logic
            print()
            view_scores = input(c("View high scores? (y/n): ").yellow).strip().lower()
            if view_scores == 'y':
                high_score_db.display_leaderboard()
                input("\nPress Enter to continue...")
        else:
            print(c("Invalid option. Please select 1, 2, or 3.").red)


if __name__ == "__main__":
    main()
