package main

import (
	"bufio"
	"fmt"
	"oldham-quiz-go/internal/colours"
	"oldham-quiz-go/internal/database"
	"oldham-quiz-go/internal/game"
	"oldham-quiz-go/internal/utils"
	"os"
	"path/filepath"
	"strconv"
	"strings"
)

func main() {
	// determine the project root directory
	execPath, err := os.Executable()
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error determining executable path: %v\n", err)
		os.Exit(1)
	}
	projectRoot := filepath.Dir(filepath.Dir(execPath))

	questionsPath := filepath.Join(projectRoot, "questions.json")
	dbPath := filepath.Join(projectRoot, "high_scores.db")

	if _, err := os.Stat(questionsPath); os.IsNotExist(err) {
		// Try current directory
		if _, err := os.Stat("questions.json"); err == nil {
			questionsPath = "questions.json"
			dbPath = "high_scores.db"
		} else {
			// Try parent directory
			questionsPath = "../questions.json"
			dbPath = "../high_scores.db"
		}
	}

	// load questions
	questions, err := utils.LoadQuestions(questionsPath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error loading questions: %v\n", err)
		fmt.Fprintf(os.Stderr, "Looking for: %s\n", questionsPath)
		os.Exit(1)
	}

	// init high score database
	highScoreDB, err := database.NewHighScoreDatabase(dbPath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error initializing database: %v\n", err)
		os.Exit(1)
	}
	defer highScoreDB.Close()

	//
	fmt.Printf("\n%s\n", colours.C("=== OLDHAM QUIZ ===").Bold().Cyan())
	fmt.Println(colours.C("Copyright (C) 2026 DecBr1").White())
	fmt.Println("This program comes with ABSOLUTELY NO WARRANTY; for details type 'w'.")
	fmt.Println("This is free software, and you are welcome to redistribute it under certain conditions; for details type 'c'.")

	reader := bufio.NewReader(os.Stdin)
	fmt.Print("Press Enter to continue, or type 'w' or 'c': ")
	response, _ := reader.ReadString('\n')
	response = strings.ToLower(strings.TrimSpace(response))

	if response == "w" {
		utils.ShowWarranty()
		fmt.Print("\nPress Enter to continue...")
		reader.ReadString('\n')
	} else if response == "c" {
		utils.ShowConditions()
		fmt.Print("\nPress Enter to continue...")
		reader.ReadString('\n')
	}

	// main menu
	for {
		fmt.Println()
		fmt.Println(colours.C("MAIN MENU").Bold().Cyan())
		fmt.Println(colours.C("1. Start New Game").Green())
		fmt.Println(colours.C("2. View High Scores").Yellow())
		fmt.Println(colours.C("3. Exit").Red())

		fmt.Print("\nSelect option (1-3): ")
		choice, _ := reader.ReadString('\n')
		choice = strings.TrimSpace(choice)

		switch choice {
		case "2":
			// view high scores
			fmt.Println()
			fmt.Println(colours.C("1. All Scores").Cyan())
			fmt.Println(colours.C("2. Single Player Only").Cyan())
			fmt.Println(colours.C("3. Multiplayer Only").Cyan())
			fmt.Println(colours.C("4. Back to Main Menu").Cyan())

			fmt.Print("\nSelect option (1-4): ")
			viewChoice, _ := reader.ReadString('\n')
			viewChoice = strings.TrimSpace(viewChoice)

			switch viewChoice {
			case "1":
				highScoreDB.DisplayLeaderboard(10, "")
				fmt.Print("Press Enter to continue...")
				reader.ReadString('\n')
			case "2":
				highScoreDB.DisplayLeaderboard(10, "single")
				fmt.Print("Press Enter to continue...")
				reader.ReadString('\n')
			case "3":
				highScoreDB.DisplayLeaderboard(10, "multiplayer")
				fmt.Print("Press Enter to continue...")
				reader.ReadString('\n')
			}

		case "3":
			// exit game
			fmt.Println(colours.C("\nThanks for playing!\n").Cyan())
			return

		case "1":
			// start game
			fmt.Println()
			numPlayers := 0
			for numPlayers < 1 || numPlayers > 3 {
				fmt.Print("How many players? (1-3): ")
				input, _ := reader.ReadString('\n')
				input = strings.TrimSpace(input)
				num, err := strconv.Atoi(input)
				if err != nil || num < 1 || num > 3 {
					fmt.Println(colours.C("Please enter a number between 1 and 3.").Red())
					continue
				}
				numPlayers = num
			}

			fmt.Println()

			var gameInstance game.QuizGame
			if numPlayers == 1 {
				gameInstance = game.NewSinglePlayerGame(questions, numPlayers, highScoreDB)
			} else {
				gameInstance = game.NewMultiPlayerGame(questions, numPlayers, highScoreDB)
			}

			gameInstance.Run()

			// high score after game over logic
			fmt.Println()
			fmt.Print(colours.C("View high scores? (y/n): ").Yellow())
			viewScores, _ := reader.ReadString('\n')
			viewScores = strings.ToLower(strings.TrimSpace(viewScores))
			if viewScores == "y" {
				highScoreDB.DisplayLeaderboard(10, "")
				fmt.Print("\nPress Enter to continue...")
				reader.ReadString('\n')
			}

		default:
			fmt.Println(colours.C("Invalid option. Please select 1, 2, or 3.").Red())
		}
	}
}
