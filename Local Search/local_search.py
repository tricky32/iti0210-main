import random
import matplotlib.pyplot as plt
import numpy as np
import time

class NQPosition:
    def __init__(self, N):
        self.N = N
        # Randomly place queens such that each column contains one queen
        self.board = [random.randint(0, N - 1) for _ in range(N)]

    def value(self):
        # Calculate the number of conflicting queen pairs (same row or diagonal)
        conflicts = 0
        for i in range(self.N):
            for j in range(i + 1, self.N):
                if self.board[i] == self.board[j] or abs(self.board[i] - self.board[j]) == abs(i - j):
                    conflicts += 1
        return conflicts

    def make_move(self, move):
        # Apply a move by moving the queen in the specified column to a new row
        col, new_row = move
        self.board[col] = new_row

    def best_move(self):
        # Find the move that reduces the number of conflicts the most
        current_value = self.value()
        best_move = None
        best_value = current_value

        for col in range(self.N):
            original_row = self.board[col]
            for row in range(self.N):
                if row != original_row:
                    self.board[col] = row
                    new_value = self.value()
                    if new_value < best_value:
                        best_value = new_value
                        best_move = (col, row)
            # Restore the original row after checking all potential moves for this column
            self.board[col] = original_row

        return best_move, best_value

def hill_climbing(pos):
    # Perform hill climbing to iteratively reduce conflicts until a solution is found or no improvement is possible
    curr_value = pos.value()
    steps = 0

    while curr_value > 0:
        move, new_value = pos.best_move()
        if new_value >= curr_value:
            # No improvement, return the current board state
            return pos, curr_value, steps
        else:
            # Apply the best move and continue searching
            pos.make_move(move)
            curr_value = new_value
            steps += 1

    return pos, curr_value, steps

def random_restart_hill_climbing(n, max_attempts=50):
    """
    Execute hill climbing multiple times with random restarts if necessary.
    Measures the total time taken and visualizes the initial and final board configurations.
    """
    start_time = time.time()  # Start the clock

    for attempt in range(max_attempts):
        pos = NQPosition(n)
        initial_board = pos.board.copy()  # Save initial board for visualization
        best_pos, best_value, steps = hill_climbing(pos)

        if best_value == 0:
            # Solution found, print the result and time taken
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Solution found in {steps} steps on attempt {attempt + 1}")
            visualize_boards(initial_board, best_pos.board)
            print(f"Time taken: {elapsed_time:.4f} seconds")
            return best_pos

    # If no solution is found after all attempts
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Failed to find a solution after {max_attempts} attempts.")
    print(f"Time taken: {elapsed_time:.4f} seconds")
    return None

def visualize_boards(initial_board, final_board):
    # Visualize the chessboard with the initial and final queen placements
    N = len(initial_board)
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    # Generate chessboard patterns
    chessboard1 = np.zeros((N, N))
    chessboard2 = np.zeros((N, N))

    for row in range(N):
        for col in range(N):
            if (row + col) % 2 == 0:
                chessboard1[row, col] = 0.9  # White square
                chessboard2[row, col] = 0.9  # White square
            else:
                chessboard1[row, col] = 0.5  # Gray square
                chessboard2[row, col] = 0.5  # Gray square

    # Plot the initial board configuration
    axes[0].imshow(chessboard1, cmap='gray', vmin=0, vmax=1)
    for col, row in enumerate(initial_board):
        axes[0].text(col, row, 'Q', ha='center', va='center', color='black', fontsize=16, fontweight='bold')
    axes[0].set_xticks(np.arange(N))
    axes[0].set_yticks(np.arange(N))
    axes[0].set_xticklabels([])
    axes[0].set_yticklabels([])
    axes[0].set_title('Initial Configuration')

    # Plot the final board configuration
    axes[1].imshow(chessboard2, cmap='gray', vmin=0, vmax=1)
    for col, row in enumerate(final_board):
        axes[1].text(col, row, 'Q', ha='center', va='center', color='black', fontsize=16, fontweight='bold')
    axes[1].set_xticks(np.arange(N))
    axes[1].set_yticks(np.arange(N))
    axes[1].set_xticklabels([])
    axes[1].set_yticklabels([])
    axes[1].set_title('Final Configuration')

    plt.show()

# Run the random restart hill climbing on a 128x128 board
random_restart_hill_climbing(8)
