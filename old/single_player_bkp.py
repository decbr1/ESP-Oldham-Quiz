import json  

def question(index):
    """Print question and options. Arg of question index. Returns question answer."""

    print(f"\nQuestion {QUESTIONS[index]['question_index']}: {QUESTIONS[index]['question']}")
    for option in QUESTIONS[index]['options']:
        print(f"  {option}")
        
    return QUESTIONS[index]['answer']

def get_valid_answer():
    """Get a valid answer (A, B, or C) from the user."""
    
    while True:
        user_answer = input(">> ").upper().strip()
        if user_answer in ('A', 'B', 'C'):
            return user_answer
        else:
            print("Invalid input! Please enter A, B, or C.")

def main():
    user_score = 0
    
    for i in range(len(QUESTIONS)):
        answer = question(i)
        user_answer = get_valid_answer()
        
        if user_answer == answer:
            user_score += 1
            print(f"Correct! Score: {user_score}")
        else:
            print(f"Incorrect! It was {answer}")
           
    print(f"\n{'-=' * 40}-")
    print(f"Your final score was {user_score}/{len(QUESTIONS)} ({user_score/len(QUESTIONS)*100:.1f}%)")

if __name__ == "__main__":
    with open('../questions.json', 'r', encoding='utf-8') as f:
        QUESTIONS = json.load(f)
    
    main()