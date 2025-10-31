N-Queens Problem: Hill Climbing with Random Restarts
Problem Description
The N-Queens problem involves placing N queens on an N×N chessboard such that no two queens threaten each other (i.e., no two queens share the same row, column, or diagonal). This project implements a hill climbing algorithm with random restarts to solve the problem for various values of N.

Hill Climbing with Random Restarts
Hill climbing is an optimization algorithm that starts with a random configuration and iteratively improves the solution by making the best possible move that reduces conflicts between queens. Random restarts are used to avoid getting stuck in local optima: when a local minimum is found but it's not a solution, the algorithm restarts with a new random configuration.

