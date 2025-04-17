import random
import sys
import time

# Set the desired probabilities (each between 0.0 and 1.0).
# Their sum CANNOT exceed 1.0.

# Probability that Player 1 (Human) wins the round.
PLAYER_WIN_PROBABILITY = 0  # <-- MODIFY THIS (e.g., 0.5)

# Probability that the round ends in a Tie.
TIE_PROBABILITY = 0        # <-- MODIFY THIS (e.g., 0.3)

# The AI's win probability will be calculated as 1.0 - PLAYER_WIN_PROBABILITY - TIE_PROBABILITY


OPTIONS = ['rock', 'paper', 'scissors']
WINNING_RULES = {
    'rock': 'scissors', # Rock beats Scissors
    'scissors': 'paper', # Scissors beats Paper
    'paper': 'rock'     # Paper beats Rock
}

# --- Input Validation ---
try:
    if not 0.0 <= PLAYER_WIN_PROBABILITY <= 1.0:
        raise ValueError("PLAYER_WIN_PROBABILITY must be between 0.0 and 1.0.")
    if not 0.0 <= TIE_PROBABILITY <= 1.0:
        raise ValueError("TIE_PROBABILITY must be between 0.0 and 1.0.")
    if PLAYER_WIN_PROBABILITY + TIE_PROBABILITY > 1.0:
         raise ValueError(f"The sum of PLAYER_WIN_PROBABILITY ({PLAYER_WIN_PROBABILITY}) and TIE_PROBABILITY ({TIE_PROBABILITY}) cannot exceed 1.0.")

    # Calculate the derived AI win probability for display/internal use
    AI_WIN_PROBABILITY = 1.0 - PLAYER_WIN_PROBABILITY - TIE_PROBABILITY
    # Small check for floating point issues, clamp if slightly below zero
    if AI_WIN_PROBABILITY < 0: AI_WIN_PROBABILITY = 0.0

except ValueError as e:
    print(f"Configuration Error: {e}", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"An unexpected configuration error occurred: {e}", file=sys.stderr)
    sys.exit(1)


def get_player_choice():
    """Gets and validates the player's choice."""
    while True:
        print("\nEnter your choice:")
        choice = input(" (rock, paper, scissors, or 'quit'): ").lower().strip()
        if choice in OPTIONS:
            return choice
        elif choice in ['q', 'quit', 'exit']:
            return 'quit'
        else:
            print("Invalid choice. Please try again.")

def get_ai_choice_biased(player_choice):
    ai_losing_move = WINNING_RULES[player_choice]

    ai_winning_move = None
    for move, beats in WINNING_RULES.items():
        if beats == player_choice:
            ai_winning_move = move
            break

    ai_tying_move = player_choice
    
    ai_prob_choosing_to_lose = PLAYER_WIN_PROBABILITY
    ai_prob_choosing_to_tie = TIE_PROBABILITY
    ai_prob_choosing_to_win = AI_WIN_PROBABILITY 

    possible_ai_moves = [ai_losing_move, ai_tying_move, ai_winning_move]
    weights = [ai_prob_choosing_to_lose, ai_prob_choosing_to_tie, ai_prob_choosing_to_win]

    chosen_move = random.choices(possible_ai_moves, weights=weights, k=1)[0]

    return chosen_move


def determine_winner(player_choice, ai_choice):
    """Determines the winner of a round."""
    if player_choice == ai_choice:
        return "tie"
    elif WINNING_RULES[player_choice] == ai_choice:
        return "player"
    else:
        return "ai"

# --- Main Game Logic ---
def play_game():
    player_score = 0
    ai_score = 0
    rounds = 0

    print("--- Rock Paper Scissors ---")
    print(f"(Settings: Player Win Prob={PLAYER_WIN_PROBABILITY:.0%}, Tie Prob={TIE_PROBABILITY:.0%}, AI Win Prob={AI_WIN_PROBABILITY:.0%})")

    while True:
        rounds += 1
        print(f"\n--- Round {rounds} ---")
        print(f"Score: Player {player_score} - AI {ai_score}")

        player_move = get_player_choice()
        if player_move == 'quit':
            print("\nThanks for playing!")
            print(f"Final Score: Player {player_score} - AI {ai_score}")
            break

        print("AI is thinking...")
        time.sleep(0.3) # Small delay

        ai_move = get_ai_choice_biased(player_move)

        print(f"\nYour choice: {player_move.capitalize()}")
        print(f"AI's choice: {ai_move.capitalize()}")

        winner = determine_winner(player_move, ai_move)

        if winner == "player":
            print(">>> You win this round! <<<")
            player_score += 1
        elif winner == "ai":
            print(">>> AI wins this round! <<<")
            ai_score += 1
        else:
            print(">>> It's a tie! <<<")

        print("-" * 20) # Separator

# --- Start the Game ---
if __name__ == "__main__":
    play_game()
