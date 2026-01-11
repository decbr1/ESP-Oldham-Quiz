package colours

import "fmt"

// ANSI color codes
const (
	Red       = "\033[91m"
	Green     = "\033[92m"
	Yellow    = "\033[93m"
	Blue      = "\033[94m"
	Magenta   = "\033[95m"
	Cyan      = "\033[96m"
	White     = "\033[97m"
	Bold      = "\033[1m"
	Underline = "\033[4m"
	Reset     = "\033[0m"
)

// ColouredStr represents a string with ANSI color codes
type ColouredStr struct {
	text  string
	codes []string
}

// C creates a new ColouredStr
func C(text string) *ColouredStr {
	return &ColouredStr{
		text:  text,
		codes: []string{},
	}
}

// String returns the coloured string with ANSI codes
func (cs *ColouredStr) String() string {
	result := ""
	for _, code := range cs.codes {
		result += code
	}
	result += cs.text + Reset
	return result
}

func (cs *ColouredStr) Red() *ColouredStr       { cs.codes = append(cs.codes, Red); return cs }
func (cs *ColouredStr) Green() *ColouredStr     { cs.codes = append(cs.codes, Green); return cs }
func (cs *ColouredStr) Yellow() *ColouredStr    { cs.codes = append(cs.codes, Yellow); return cs }
func (cs *ColouredStr) Blue() *ColouredStr      { cs.codes = append(cs.codes, Blue); return cs }
func (cs *ColouredStr) Magenta() *ColouredStr   { cs.codes = append(cs.codes, Magenta); return cs }
func (cs *ColouredStr) Cyan() *ColouredStr      { cs.codes = append(cs.codes, Cyan); return cs }
func (cs *ColouredStr) White() *ColouredStr     { cs.codes = append(cs.codes, White); return cs }
func (cs *ColouredStr) Bold() *ColouredStr      { cs.codes = append(cs.codes, Bold); return cs }
func (cs *ColouredStr) Underline() *ColouredStr { cs.codes = append(cs.codes, Underline); return cs }

func (cs *ColouredStr) Print()   { fmt.Print(cs.String()) }
func (cs *ColouredStr) Println() { fmt.Println(cs.String()) }
