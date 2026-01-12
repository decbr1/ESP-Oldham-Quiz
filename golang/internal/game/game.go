package game

import (
	"bufio"
	"fmt"
	"oldham-quiz-go/internal/colours"
	"oldham-quiz-go/internal/database"
	"oldham-quiz-go/internal/input"
	"oldham-quiz-go/internal/models"
	"os"
	"sort"
	"strings"
)

// QuizGame is the interface for quiz game modes
type QuizGame interface {
	SetupPlayers()
	PlayQuestion(question *models.Question, questionNum int) bool
	DisplayFinalResults()
	GetGameMode() string
	Run()
}

// BaseGame contains common game functionality
type BaseGame struct {
	Questions   []*models.Question
	NumPlayers  int
	Players     map[string]*models.Player
	HighScoreDB *database.HighScoreDatabase
}

// NewBaseGame creates a new BaseGame instance
func NewBaseGame(questions []*models.Question, numPlayers int, highScoreDB *database.HighScoreDatabase) *BaseGame {
	return &BaseGame{
		Questions:   questions,
		NumPlayers:  numPlayers,
		Players:     make(map[string]*models.Player),
		HighScoreDB: highScoreDB,
	}
}

// DisplayFinalResults displays final game results
func (bg *BaseGame) DisplayFinalResults(gameMode string) {
	fmt.Println("\n" + strings.Repeat("=", 50))
	fmt.Printf("%s%s%s\n", colours.Bold, colours.Magenta, "FINAL RESULTS"+colours.Reset)
	fmt.Println(strings.Repeat("=", 50))

	// Sort players by score
	sortedPlayers := make([]*models.Player, 0, len(bg.Players))
	for _, player := range bg.Players {
		sortedPlayers = append(sortedPlayers, player)
	}
	sort.Slice(sortedPlayers, func(i, j int) bool {
		return sortedPlayers[i].Score > sortedPlayers[j].Score
	})

	// Save scores to database
	for _, player := range sortedPlayers {
		bg.HighScoreDB.AddScore(player.Name, player.Score, len(bg.Questions), gameMode)
	}

	// Display results
	for rank, player := range sortedPlayers {
		percentage := 0.0
		if len(bg.Questions) > 0 {
			percentage = (float64(player.Score) / float64(len(bg.Questions))) * 100
		}
		fmt.Printf("%s%d. %s:%s %s%d/%d%s (%.1f%%)\n",
			colours.Cyan, rank+1, player.Name, colours.Reset,
			colours.Bold, player.Score, len(bg.Questions), colours.Reset,
			percentage)
	}

	return
}

// SinglePlayerGame represents single player quiz game mode
type SinglePlayerGame struct {
	*BaseGame
}

// NewSinglePlayerGame creates a new SinglePlayerGame instance
func NewSinglePlayerGame(questions []*models.Question, numPlayers int, highScoreDB *database.HighScoreDatabase) *SinglePlayerGame {
	return &SinglePlayerGame{
		BaseGame: NewBaseGame(questions, numPlayers, highScoreDB),
	}
}

// SetupPlayers sets up the single player
func (spg *SinglePlayerGame) SetupPlayers() {
	reader := bufio.NewReader(os.Stdin)
	fmt.Print("Player name: ")
	name, _ := reader.ReadString('\n')
	name = strings.TrimSpace(name)
	if name == "" {
		name = "Player 1"
	}
	spg.Players["Q"] = models.NewPlayer(name, "Q")
}

// PlayQuestion plays a question in single player mode
func (spg *SinglePlayerGame) PlayQuestion(question *models.Question, questionNum int) bool {
	player := spg.Players["Q"]
	userAnswer := input.GetValidAnswer()

	if userAnswer == question.Answer {
		player.AddPoint()
		fmt.Printf("%sCorrect! +1 point.%s Score: %s%d/%d%s\n",
			colours.Green, colours.Reset,
			colours.Bold, player.Score, questionNum+1, colours.Reset)
	} else {
		fmt.Printf("%sIncorrect.%s The correct answer was %s%s%s. Score: %s%d/%d%s\n",
			colours.Red, colours.Reset,
			colours.Bold, question.Answer, colours.Reset,
			colours.Bold, player.Score, questionNum+1, colours.Reset)
	}

	return true
}

// DisplayFinalResults displays single player results
func (spg *SinglePlayerGame) DisplayFinalResults() {
	spg.BaseGame.DisplayFinalResults("single")
	fmt.Println(strings.Repeat("=", 50))
}

// GetGameMode returns the game mode identifier
func (spg *SinglePlayerGame) GetGameMode() string {
	return "single"
}

// Run runs the complete quiz game
func (spg *SinglePlayerGame) Run() {
	spg.SetupPlayers()

	for i, question := range spg.Questions {
		question.Display()
		spg.PlayQuestion(question, i)
	}

	spg.DisplayFinalResults()
}

// MultiPlayerGame represents multi-player quiz game mode with buzzer support
type MultiPlayerGame struct {
	*BaseGame
	Buzzer      *input.BuzzerInput
	MaxAttempts int
	BuzzerKeys  []string
}

// NewMultiPlayerGame creates a new MultiPlayerGame instance
func NewMultiPlayerGame(questions []*models.Question, numPlayers int, highScoreDB *database.HighScoreDatabase) *MultiPlayerGame {
	return &MultiPlayerGame{
		BaseGame:    NewBaseGame(questions, numPlayers, highScoreDB),
		Buzzer:      input.NewBuzzerInput(),
		MaxAttempts: 2,
		BuzzerKeys:  []string{"Q", "P", "B"},
	}
}

// SetupPlayers sets up multiple players
func (mpg *MultiPlayerGame) SetupPlayers() {
	reader := bufio.NewReader(os.Stdin)
	for i := 0; i < mpg.NumPlayers; i++ {
		key := mpg.BuzzerKeys[i]
		fmt.Printf("Player %d (Key: %s): ", i+1, key)
		name, _ := reader.ReadString('\n')
		name = strings.TrimSpace(name)
		if name == "" {
			name = fmt.Sprintf("Player %d", i+1)
		}
		mpg.Players[key] = models.NewPlayer(name, key)
	}

	mpg.displayBuzzerInfo()
}

// displayBuzzerInfo displays buzzer key assignments and setup info
func (mpg *MultiPlayerGame) displayBuzzerInfo() {
	fmt.Println("\n" + strings.Repeat("=", 50))
	fmt.Printf("%s%sBUZZER KEYS:%s\n", colours.Bold, colours.Blue, colours.Reset)
	for _, player := range mpg.Players {
		fmt.Printf("  %s%s%s - %s%s%s\n",
			colours.Yellow, player.Key, colours.Reset,
			colours.Cyan, player.Name, colours.Reset)
	}
	fmt.Println(strings.Repeat("=", 50) + "\n")

	if !mpg.Buzzer.IsTTY() {
		fmt.Println("It looks like you're running in an IDE console.")
		fmt.Println("No worries! On buzz in, you will have to press enter after your key.")
		fmt.Println("To have the buzzer more realistic, run the game with `go run cmd/main.go` in a terminal.")
		reader := bufio.NewReader(os.Stdin)
		fmt.Print("Press enter to confirm you have read the above...")
		reader.ReadString('\n')
	}
}

// PlayQuestion plays a question in multiplayer mode
func (mpg *MultiPlayerGame) PlayQuestion(question *models.Question, questionNum int) bool {
	attempts := 0
	var firstBuzzer string

	for attempts < mpg.MaxAttempts {
		fmt.Printf("\n%s%sBUZZ IN WITH YOUR KEY%s\n", colours.Bold, colours.Magenta, colours.Reset)
		buzzerKey := mpg.Buzzer.WaitForBuzz()

		if !mpg.isValidBuzz(buzzerKey, firstBuzzer, attempts) {
			continue
		}

		player := mpg.Players[buzzerKey]
		fmt.Printf("%s%s%s buzzed in.\n", colours.Cyan, player.Name, colours.Reset)

		if attempts == 0 {
			firstBuzzer = buzzerKey
		}

		userAnswer := input.GetValidAnswer()
		attempts++

		if userAnswer == question.Answer {
			player.AddPoint()
			if attempts == 1 {
				fmt.Printf("%sCorrect. +1 point to %s%s\n", colours.Green, player.Name, colours.Reset)
			} else {
				fmt.Printf("%sCorrect! Steal successful. +1 point to %s%s\n", colours.Green, player.Name, colours.Reset)
			}
			break
		} else {
			if attempts == 1 {
				fmt.Printf("%sIncorrect.%s Steal opportunity available.\n", colours.Red, colours.Reset)
			} else {
				fmt.Printf("%sIncorrect.%s The correct answer was %s%s%s\n",
					colours.Red, colours.Reset,
					colours.Bold, question.Answer, colours.Reset)
				fmt.Println("Question skipped.")
				break
			}
		}
	}

	mpg.displayCurrentScores()

	if questionNum < len(mpg.Questions)-1 {
		reader := bufio.NewReader(os.Stdin)
		fmt.Print("\nPress Enter for next question...")
		reader.ReadString('\n')
	}

	return true
}

// isValidBuzz checks if a buzz is valid
func (mpg *MultiPlayerGame) isValidBuzz(buzzerKey, firstBuzzer string, attempts int) bool {
	if _, exists := mpg.Players[buzzerKey]; !exists {
		fmt.Printf("\n%sKey %s is not assigned to a player.%s\n", colours.Red, buzzerKey, colours.Reset)
		return false
	}

	if attempts == 1 && buzzerKey == firstBuzzer {
		fmt.Printf("%s%s already attempted this question.%s\n",
			colours.Red, mpg.Players[buzzerKey].Name, colours.Reset)
		return false
	}

	return true
}

// displayCurrentScores displays current scores for all players
func (mpg *MultiPlayerGame) displayCurrentScores() {
	fmt.Println("\n" + strings.Repeat("-", 50))
	fmt.Printf("%s%sCURRENT SCORES:%s\n", colours.Bold, colours.Blue, colours.Reset)

	// Sort players by key for consistent display
	keys := make([]string, 0, len(mpg.Players))
	for key := range mpg.Players {
		keys = append(keys, key)
	}
	sort.Strings(keys)

	for _, key := range keys {
		player := mpg.Players[key]
		fmt.Printf("  %s%s:%s %s%d%s\n",
			colours.Cyan, player.Name, colours.Reset,
			colours.Bold, player.Score, colours.Reset)
	}
	fmt.Println(strings.Repeat("-", 50))
}

// DisplayFinalResults displays the game winner
func (mpg *MultiPlayerGame) DisplayFinalResults() {
	mpg.BaseGame.DisplayFinalResults("multiplayer")

	// Find winner
	sortedPlayers := make([]*models.Player, 0, len(mpg.Players))
	for _, player := range mpg.Players {
		sortedPlayers = append(sortedPlayers, player)
	}
	sort.Slice(sortedPlayers, func(i, j int) bool {
		return sortedPlayers[i].Score > sortedPlayers[j].Score
	})

	if len(sortedPlayers) > 0 {
		winner := sortedPlayers[0]
		fmt.Printf("\n%s\n", colours.C(fmt.Sprintf("Winner: %s with %d points!", winner.Name, winner.Score)).Green().Bold())
	}

	fmt.Println(strings.Repeat("=", 50))
}

// GetGameMode returns the game mode identifier
func (mpg *MultiPlayerGame) GetGameMode() string {
	return "multiplayer"
}

// Run runs the complete quiz game
func (mpg *MultiPlayerGame) Run() {
	mpg.SetupPlayers()

	for i, question := range mpg.Questions {
		question.Display()
		mpg.PlayQuestion(question, i)
	}

	mpg.DisplayFinalResults()
}
