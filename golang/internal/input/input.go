package input

import (
	"bufio"
	"fmt"
	"oldham-quiz-go/internal/colours"
	"os"
	"runtime"
	"strings"
	"syscall"
	"unsafe"
)

// BuzzerInput handles buzzer input detection across different platforms
type BuzzerInput struct {
	validKeys []string
	isTTY     bool
}

// NewBuzzerInput creates a new BuzzerInput instance
func NewBuzzerInput() *BuzzerInput {
	isTTY := isTerminal()
	return &BuzzerInput{
		validKeys: []string{"Q", "P", "B"},
		isTTY:     isTTY,
	}
}

// isTerminal checks if stdin is a terminal
func isTerminal() bool {
	if runtime.GOOS == "windows" {
		return false
	}
	fileInfo, err := os.Stdin.Stat()
	if err != nil {
		return false
	}
	return (fileInfo.Mode() & os.ModeCharDevice) != 0
}

// WaitForBuzz waits for a valid buzzer key press
func (bi *BuzzerInput) WaitForBuzz() string {
	if runtime.GOOS == "windows" {
		return bi.waitForBuzzWindows()
	}
	return bi.waitForBuzzUnix()
}

// waitForBuzzWindows is currently unimplemented.
// it would wait for buzzer key on Windows.
func (bi *BuzzerInput) waitForBuzzWindows() string {
	return bi.waitForBuzzFallback()
}

// waitForBuzzUnix waits for buzzer key on Unix-like systems.
// im particularly proud of this function, low level syscalls are very scary
func (bi *BuzzerInput) waitForBuzzUnix() string {
	if !bi.isTTY {
		return bi.waitForBuzzFallback()
	}

	fd := int(os.Stdin.Fd())
	var oldState syscall.Termios
	if _, _, err := syscall.Syscall(syscall.SYS_IOCTL, uintptr(fd), syscall.TCGETS, uintptr(unsafe.Pointer(&oldState))); err != 0 {
		return bi.waitForBuzzFallback()
	}

	newState := oldState
	newState.Lflag &^= syscall.ICANON | syscall.ECHO
	if _, _, err := syscall.Syscall(syscall.SYS_IOCTL, uintptr(fd), syscall.TCSETS, uintptr(unsafe.Pointer(&newState))); err != 0 {
		return bi.waitForBuzzFallback()
	}

	defer func() {
		syscall.Syscall(syscall.SYS_IOCTL, uintptr(fd), syscall.TCSETS, uintptr(unsafe.Pointer(&oldState)))
	}()

	buf := make([]byte, 1)
	for {
		_, err := os.Stdin.Read(buf)
		if err != nil {
			continue
		}
		key := strings.ToUpper(string(buf[0]))
		if bi.isValidKey(key) {
			return key
		}
	}
}

// waitForBuzzFallback fallback input method for non-TTY environments
func (bi *BuzzerInput) waitForBuzzFallback() string {
	reader := bufio.NewReader(os.Stdin)
	for {
		input, err := reader.ReadString('\n')
		if err != nil {
			continue
		}
		key := strings.ToUpper(strings.TrimSpace(input))
		if bi.isValidKey(key) {
			return key
		}
		fmt.Println(colours.C(fmt.Sprintf("Invalid key! Please enter %s.", strings.Join(bi.validKeys, ", "))).Red())
	}
}

// isValidKey checks if a key is valid
func (bi *BuzzerInput) isValidKey(key string) bool {
	for _, validKey := range bi.validKeys {
		if key == validKey {
			return true
		}
	}
	return false
}

// IsTTY returns whether the input is from a TTY
func (bi *BuzzerInput) IsTTY() bool {
	return bi.isTTY
}

// GetValidAnswer gets a valid answer (A, B, or C) from the user
func GetValidAnswer() string {
	reader := bufio.NewReader(os.Stdin)
	for {
		fmt.Print("Answer >> ")
		input, err := reader.ReadString('\n')
		if err != nil {
			continue
		}
		answer := strings.ToUpper(strings.TrimSpace(input))
		if answer == "A" || answer == "B" || answer == "C" {
			return answer
		}
		fmt.Println(colours.C("Invalid input! Please enter A, B, or C.").Red())
	}
}
