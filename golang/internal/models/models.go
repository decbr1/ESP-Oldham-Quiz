package models

import (
	"fmt"
	"oldham-quiz-go/internal/colours"
)

// Player represents a quiz player with name and score
type Player struct {
	Name  string
	Key   string
	Score int
}

// NewPlayer creates a new Player instance
func NewPlayer(name, key string) *Player {
	return &Player{
		Name:  name,
		Key:   key,
		Score: 0,
	}
}

// AddPoint adds one point to the player's score
func (p *Player) AddPoint() {
	p.Score++
}

// String returns a string representation of the player
func (p *Player) String() string {
	return fmt.Sprintf("Player(name=%s, score=%d, key=%s)", p.Name, p.Score, p.Key)
}

// Question represents a quiz question with multiple choice options
type Question struct {
	Index   int
	Text    string
	Options []string
	Answer  string
}

// NewQuestion creates a new Question from map data
func NewQuestion(data map[string]interface{}) *Question {
	options := []string{}
	if opts, ok := data["options"].([]interface{}); ok {
		for _, opt := range opts {
			if optStr, ok := opt.(string); ok {
				options = append(options, optStr)
			}
		}
	}

	index := 0
	if idx, ok := data["question_index"].(float64); ok {
		index = int(idx)
	}

	text := ""
	if t, ok := data["question"].(string); ok {
		text = t
	}

	answer := ""
	if ans, ok := data["answer"].(string); ok {
		answer = ans
	}

	return &Question{
		Index:   index,
		Text:    text,
		Options: options,
		Answer:  answer,
	}
}

// Display displays the question and its options
func (q *Question) Display() {
	fmt.Printf("\n%s %s\n", colours.C(fmt.Sprintf("Question %d:", q.Index)).Cyan().Bold(), colours.C(q.Text).White())
	for _, option := range q.Options {
		fmt.Printf("  %s\n", colours.C(option).Yellow())
	}
}
