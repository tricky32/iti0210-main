import os
import random


# Define constants for the game
ROWS = 6
COLS = 7
WIN = 4

def create_board():
    # Generate an empty board for the game
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def dump_pos(board):
    # Print the current layout of the board to the console
    for row in board:
        print("| " + " | ".join(row) + " |")  # Display each row
    print("  0   1   2   3   4   5   6")  # Show column indices

def moves(board):
    # Identify columns where a move can be made (top row is empty)
    return [col for col in range(COLS) if board[0][col] == " "]

def make_move(board, col, side):
    # Add a piece for the specified player in the selected column
    for row in reversed(range(ROWS)):  # Check from the bottom row up
        if board[row][col] == " ":  # Find the first empty space
            board[row][col] = side  # Place the player's piece
            return board

def is_winner(board, side):
    # Verify if the given player has won
    for row in range(ROWS):
        for col in range(COLS):
            # Check for winning conditions (horizontal, vertical, diagonal)
            if (check_line(board, row, col, 1, 0, side) or  # Horizontal check
                check_line(board, row, col, 0, 1, side) or  # Vertical check
                check_line(board, row, col, 1, 1, side) or  # Diagonal check \
                check_line(board, row, col, 1, -1, side)):  # Diagonal check /
                return True  # Player has achieved victory
    return False  # No winner detected

def check_line(board, row, col, delta_row, delta_col, side):
    # Count if there are enough pieces in a line for a win
    count = 0  # Start counting connected pieces
    for i in range(WIN):
        r = row + delta_row * i  # Compute the current row index
        c = col + delta_col * i  # Compute the current column index
        # Ensure indices are within board limits and match the player's piece
        if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == side:
            count += 1  # Increment the count if pieces match
        else:
            break  # Stop counting if the line is broken
    return count == WIN  # Return whether the count meets the winning threshold

def is_over(board):
    # Determine if the game has ended (win or full board)
    if any(is_winner(board, side) for side in ["X", "O"]):  # Check for any wins
        return True
    return all(board[0][col] != " " for col in range(COLS))  # Check if the board is completely filled

def parse_move(movestr):
    # Transform the input move string into an integer
    return int(movestr)

def simulate(pos, move, side):
    # Run a simulation of the game from the current position after making a move
    board_copy = [row[:] for row in pos["board"]]  # Duplicate the current board
    make_move(board_copy, move, side)  # Execute the move for the current player
    current_side = "O" if side == "X" else "X"  # Switch to the opponent's turn

    # Keep playing until the game is over
    while not is_over(board_copy):
        legal_moves = moves(board_copy)  # Determine available moves for the current player
        if not legal_moves:
            break  # Exit if there are no valid moves
        make_move(board_copy, random.choice(legal_moves), current_side)  # Randomly select and execute a move
        current_side = "O" if current_side == "X" else "X"  # Alternate turns

    # Assess the outcome of the simulation
    if is_winner(board_copy, side):
        return "WIN"  # The current player wins
    elif is_winner(board_copy, "O" if side == "X" else "X"):
        return "LOSE"  # The opponent wins
    else:
        return "DRAW"  # No victor; the game ends in a draw

def pure_mc(pos, N=200):
    # Conduct Monte Carlo simulations to identify the best move
    my_side = pos["to_move"]  # Determine which player is currently making a move
    initial_moves = moves(pos["board"])  # Retrieve a list of possible moves
    win_counts = dict((move, 0) for move in initial_moves)  # Set up win counts for each potential move

    # Simulate each initial move N times
    for move in initial_moves:
        for _ in range(N):
            res = simulate(pos, move, my_side)  # Execute the simulation
            if res == "WIN":
                win_counts[move] += 1  # Tally wins for successful moves
            elif res == "DRAW":
                win_counts[move] += 0.5  # Increment for draw scenarios

    # Identify the move with the highest number of wins
    best_move = max(win_counts, key=win_counts.get)
    return best_move, win_counts  # Return the optimal move and its win statistics

def save_results_to_file(pos, win_counts):
    # Specify the file name and path for saving results
    file_name = "results.txt"  
    current_directory = os.path.dirname(os.path.abspath(__file__))  # Acquire the current directory
    file_path = os.path.join(current_directory, file_name)  # Construct the full file path

    # Open the file in append mode for writing
    with open(file_path, "a") as file:
       
        # Document the current board position in the specified format
        file.write("Position:\n")
        for row in pos["board"]:
            file.write("| " + " | ".join(row) + " |\n")  # Write each row of the board layout
        file.write("  0   1   2   3   4   5   6\n")  # Add column labels

        # Record available moves and their winning percentages
        file.write("\nLegal Moves:\n")
        file.write(str(moves(pos["board"])) + "\n")  # List of legal moves

        file.write("\nWinning Percentages:\n")  # Start the section for win percentages
        for move, wins in win_counts.items():
            percentage = (wins / 200) * 100  # Compute win percentage
            file.write(f"Move {move}: {percentage:.2f}%\n")  # Log the calculated percentage

        # Include a visual separator for clarity between game results
        file.write("\n" + "="*30 + "\n")

def play_game():
    # Primary function to facilitate gameplay in Connect 4
    board = create_board()  # Set up the initial game board
    pos = {"board": board, "to_move": "X"}  # Define the starting position

    playing = True  # Flag to manage the game loop
    while playing:
        dump_pos(board)  # Show the current state of the board
        if pos["to_move"] == "X":  # Player's turn to act
            valid_move = False
            while not valid_move:  # Ensure a valid selection is made
                movestr = input("Your move (0-6)? ")  # Prompt player for input
                if movestr.isdigit():  # Validate input as a digit
                    move = int(movestr)  # Convert input string to an integer
                    if 0 <= move <= 6 and move in moves(pos["board"]):  # Confirm the move is valid
                        valid_move = True  # Confirm a valid move has been made
                    else:
                        print("Invalid move. Please choose a column between 0-6 that is not full.")  # Notify of invalid move
                else:
                    print("Please enter a number between 0 and 6.")  # Alert for non-numeric input
        else:  # Computer's turn to make a move
            move, win_counts = pure_mc(pos)  # Use Monte Carlo to identify the best move
            print(f"Computer's move: {move}")  # Announce the computer's move
            save_results_to_file(pos, win_counts)  # Log the results in a file

        pos["board"] = make_move(board, move, pos["to_move"])  # Update the board with the chosen move

        if is_winner(pos["board"], pos["to_move"]):  # Assess if the current player has won
            dump_pos(board)  # Show the final state of the board
            playing = False  # Conclude the game loop
            if pos["to_move"] == "X":
                print("Congratulations! You win!")  # Message for player victory
            else:
                print("Computer wins. Better luck next time!")  # Message for computer victory

        pos["to_move"] = "O" if pos["to_move"] == "X" else "X"  # Toggle to the next player

if __name__ == "__main__":
    play_game()  # Initiate gameplay when the script is executed
