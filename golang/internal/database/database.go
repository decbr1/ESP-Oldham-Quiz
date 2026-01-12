package database

import (
	"database/sql"
	"fmt"
	"oldham-quiz-go/internal/colours"
	"time"

	_ "github.com/mattn/go-sqlite3"
)

// HighScoreDatabase manages high scores using SQLite database
type HighScoreDatabase struct {
	dbPath string
	db     *sql.DB
}

// HighScore represents a single high score entry
type HighScore struct {
	PlayerName     string
	Score          int
	TotalQuestions int
	Percentage     float64
	GameMode       string
	Timestamp      string
}

// NewHighScoreDatabase creates a new HighScoreDatabase instance
func NewHighScoreDatabase(dbPath string) (*HighScoreDatabase, error) {
	db, err := sql.Open("sqlite3", dbPath)
	if err != nil {
		return nil, fmt.Errorf("failed to open database: %w", err)
	}

	hsd := &HighScoreDatabase{
		dbPath: dbPath,
		db:     db,
	}

	if err := hsd.initDatabase(); err != nil {
		return nil, err
	}

	return hsd, nil
}

// initDatabase creates the high scores table if it doesn't exist
func (hsd *HighScoreDatabase) initDatabase() error {
	query := `
		CREATE TABLE IF NOT EXISTS high_scores (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			player_name TEXT NOT NULL,
			score INTEGER NOT NULL,
			total_questions INTEGER NOT NULL,
			percentage REAL NOT NULL,
			game_mode TEXT NOT NULL,
			timestamp TEXT NOT NULL
		)
	`

	_, err := hsd.db.Exec(query)
	if err != nil {
		return fmt.Errorf("failed to create table: %w", err)
	}

	return nil
}

// AddScore adds a new high score to the database
func (hsd *HighScoreDatabase) AddScore(playerName string, score, totalQuestions int, gameMode string) error {
	percentage := 0.0
	if totalQuestions > 0 {
		percentage = (float64(score) / float64(totalQuestions)) * 100
	}

	timestamp := time.Now().Format("2006-01-02 15:04:05")

	query := `
		INSERT INTO high_scores (player_name, score, total_questions, percentage, game_mode, timestamp)
		VALUES (?, ?, ?, ?, ?, ?)
	`

	_, err := hsd.db.Exec(query, playerName, score, totalQuestions, percentage, gameMode, timestamp)
	if err != nil {
		return fmt.Errorf("failed to add score: %w", err)
	}

	return nil
}

// GetTopScores retrieves the top high scores
func (hsd *HighScoreDatabase) GetTopScores(limit int, gameMode string) ([]HighScore, error) {
	var query string
	var rows *sql.Rows
	var err error

	if gameMode != "" {
		query = `
			SELECT player_name, score, total_questions, percentage, game_mode, timestamp
			FROM high_scores
			WHERE game_mode = ?
			ORDER BY percentage DESC, score DESC, timestamp ASC
			LIMIT ?
		`
		rows, err = hsd.db.Query(query, gameMode, limit)
	} else {
		query = `
			SELECT player_name, score, total_questions, percentage, game_mode, timestamp
			FROM high_scores
			ORDER BY percentage DESC, score DESC, timestamp ASC
			LIMIT ?
		`
		rows, err = hsd.db.Query(query, limit)
	}

	if err != nil {
		return nil, fmt.Errorf("failed to query scores: %w", err)
	}
	defer rows.Close()

	var scores []HighScore
	for rows.Next() {
		var hs HighScore
		err := rows.Scan(&hs.PlayerName, &hs.Score, &hs.TotalQuestions, &hs.Percentage, &hs.GameMode, &hs.Timestamp)
		if err != nil {
			return nil, fmt.Errorf("failed to scan row: %w", err)
		}
		scores = append(scores, hs)
	}

	return scores, nil
}

// DisplayLeaderboard displays the high scores leaderboard
func (hsd *HighScoreDatabase) DisplayLeaderboard(limit int, gameMode string) error {
	scores, err := hsd.GetTopScores(limit, gameMode)
	if err != nil {
		return err
	}

	if len(scores) == 0 {
		fmt.Printf("\n%s\n\n", colours.C("No high scores yet. Be the first!").Yellow())
		return nil
	}

	modeText := " (ALL MODES)"
	if gameMode != "" {
		modeText = fmt.Sprintf(" (%s)", gameMode)
	}

	fmt.Println("\n" + "======================================================================")
	fmt.Println(colours.C(fmt.Sprintf("HIGH SCORES LEADERBOARD%s", modeText)).Bold().Magenta())
	fmt.Println("======================================================================")

	for rank, score := range scores {
		modeBadge := "[S]"
		if score.GameMode == "multiplayer" {
			modeBadge = "[M]"
		}

		// extract just the date from timestamp
		timestamp := score.Timestamp
		if len(timestamp) >= 10 {
			timestamp = timestamp[:10]
		}

		fmt.Printf("%s %s (%5.1f%%)  %s  %s\n",
			colours.C(fmt.Sprintf("%2d. %-20s", rank+1, score.PlayerName)).Cyan(),
			colours.C(fmt.Sprintf("%2d/%2d", score.Score, score.TotalQuestions)).Bold(),
			score.Percentage,
			colours.C(modeBadge).Yellow(),
			colours.C(timestamp).White())
	}

	fmt.Println("======================================================================")
	fmt.Printf("%s\n\n", colours.C("Legend: [S] = Single Player, [M] = Multiplayer").White())

	return nil
}

func (hsd *HighScoreDatabase) Close() error {
	return hsd.db.Close()
}
