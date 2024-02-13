import tkinter as tk
from tkinter import messagebox, PhotoImage
import math

class TicTacToe:
    def __init__(self, root):
        """
         Initialize the Tic Tac Toe. This is the method that will be called by the constructor
         
         @param root - The root of the
        """
        self.root = root
        self.root.title("Tic Tac Toe by Huzi")
        self.root.iconphoto(True, PhotoImage(file="logo.png")) 
        self.players = ["Player 1", "AI"]
        self.current_player = "Player 1"
        self.board = [" " for _ in range(9)]
        self.buttons = []
        self.create_board()

    def create_board(self):
        """
         Create the board and buttons for the game. This is called by __init__ and should not be called directly
        """
        # Create 3 rows of the button
        for i in range(3):
            row = []
            # Add a button to the top of the grid.
            for j in range(3):
                color = "white" if (i + j) % 2 == 0 else "grey"
                button = tk.Button(self.root, text="", font=("Arial", 24), width=5, height=2,
                                command=lambda i=i, j=j: self.on_click(i, j), bg=color, fg="red")
                button.grid(row=i, column=j, sticky="nsew")
                row.append(button)
            self.buttons.append(row)


        for i in range(3):
            self.root.grid_rowconfigure(i, weight=1)
            self.root.grid_columnconfigure(i, weight=1)

        self.root.grid_propagate(False)


    def on_click(self, i, j):
        """
         Called when a button is clicked. This is where you can change the state of the board to X or AI
         
         @param i - The row of the button that was clicked
         @param j - The column of the button that was clicked ( 0 = left 1 = right
        """
        # This function is called by the game.
        if self.board[i * 3 + j] == " " and self.current_player == "Player 1":
            self.board[i * 3 + j] = "X"
            self.buttons[i][j].config(text="X")
            # This method is called by the game.
            if self.check_winner("X"):
                messagebox.showinfo("Game Over", "Player 1 wins!")
                self.reset_board()
            elif self.is_draw():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_board()
            else:
                self.current_player = "AI"
                self.computer_move()

    def check_winner(self, player):
        """
         Checks if a player wins. This is used to determine if there is a winner or not.
         
         @param player - The player to check. This can be a string or a number.
         
         @return True if the player wins False otherwise. Note that the board is sorted by player. position and player.
        """
        winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                                (0, 3, 6), (1, 4, 7), (2, 5, 8),
                                (0, 4, 8), (2, 4, 6)]

        # Returns true if all players in winning_combinations are in the board
        for combination in winning_combinations:
            # Check if player is in combination
            if all(self.board[idx] == player for idx in combination):
                return True
        return False

    def is_draw(self):
        """
         Checks if the board is a draw. This is used to determine if we are going to draw or not.
         
         
         @return True if there is a draw False otherwise. >>> board. is_draw () Traceback ( most recent call last ) : NoDraw
        """
        return " " not in self.board

    def get_empty_cells(self):
        """
         Returns a list of indices of empty cells in the board. This is useful for debugging. If you want to check if a cell is empty use get_empty_cells_by_index
         
         
         @return list of indices of
        """
        return [idx for idx, cell in enumerate(self.board) if cell == " "]

    def computer_move(self):
        """
         Move to the winner if there are empty cells. This is called by self. computer_play
        """
        empty_cells = self.get_empty_cells()
        # This method is called when the board is empty
        if empty_cells:
            best_move = None
            best_eval = -math.inf
            # This function will draw the best cell to the board
            for idx in empty_cells:
                self.board[idx] = "O"
                eval = self.minimax(self.board, 0, False)
                self.board[idx] = " "
                # Set the best evaluation to the best move.
                if eval > best_eval:
                    best_eval = eval
                    best_move = idx
            self.board[best_move] = "O"
            row, col = divmod(best_move, 3)
            self.buttons[row][col].config(text="O")
            # This method is called when the game is over a game
            if self.check_winner("O"):
                messagebox.showinfo("Game Over", "AI wins!")
                self.reset_board()
            elif self.is_draw():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_board()
            else:
                self.current_player = "Player 1"

    def minimax(self, board, depth, maximizing_player):
        """
         Minimax method to find the winner. This method is used by the minimax method in order to find the winner of the game.
         
         @param board - The board that is being solved. This will be modified in place.
         @param depth - The depth of the game. This is used to prevent infinite loops
         @param maximizing_player - True if the game is maximizing
         
         @return The min or
        """
        # Check if the window is visible.
        if self.check_winner("X"):
            return -1
        # Check if the current window is winner
        if self.check_winner("O"):
            return 1
        # Return 0 if board is empty
        if not any(cell == " " for cell in board):
            return 0

        if maximizing_player:
            max_eval = -math.inf
            # This method is used to generate the cells of the board
            for idx in self.get_empty_cells():
                board[idx] = "O"
                eval = self.minimax(board, depth + 1, False)
                board[idx] = " "
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = math.inf
            # Add the cells to the board
            for idx in self.get_empty_cells():
                board[idx] = "X"
                eval = self.minimax(board, depth + 1, True)
                board[idx] = " "
                min_eval = min(min_eval, eval)
            return min_eval

    def reset_board(self):
        """
         Reset Board to default state for new game. This is called when game is reloaded from a file
        """
        self.board = [" " for _ in range(9)]
        # Set text to text in each button
        for row in self.buttons:
            for button in row:
                button.config(text="")
        self.current_player = "Player 1"

# This function is called by the TicTacToe class
if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()

