import tkinter as tk
from tkinter import messagebox, PhotoImage
import math

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe by Huzi")
        self.root.iconphoto(True, PhotoImage(file="logo.png")) 
        self.players = ["Player 1", "AI"]
        self.current_player = "Player 1"
        self.board = [" " for _ in range(9)]
        self.buttons = []
        self.create_board()

    def create_board(self):
        for i in range(3):
            row = []
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
        if self.board[i * 3 + j] == " " and self.current_player == "Player 1":
            self.board[i * 3 + j] = "X"
            self.buttons[i][j].config(text="X")
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
        winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                                (0, 3, 6), (1, 4, 7), (2, 5, 8),
                                (0, 4, 8), (2, 4, 6)]

        for combination in winning_combinations:
            if all(self.board[idx] == player for idx in combination):
                return True
        return False

    def is_draw(self):
        return " " not in self.board

    def get_empty_cells(self):
        return [idx for idx, cell in enumerate(self.board) if cell == " "]

    def computer_move(self):
        empty_cells = self.get_empty_cells()
        if empty_cells:
            best_move = None
            best_eval = -math.inf
            for idx in empty_cells:
                self.board[idx] = "O"
                eval = self.minimax(self.board, 0, False)
                self.board[idx] = " "
                if eval > best_eval:
                    best_eval = eval
                    best_move = idx
            self.board[best_move] = "O"
            row, col = divmod(best_move, 3)
            self.buttons[row][col].config(text="O")
            if self.check_winner("O"):
                messagebox.showinfo("Game Over", "AI wins!")
                self.reset_board()
            elif self.is_draw():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_board()
            else:
                self.current_player = "Player 1"

    def minimax(self, board, depth, maximizing_player):
        if self.check_winner("X"):
            return -1
        if self.check_winner("O"):
            return 1
        if not any(cell == " " for cell in board):
            return 0

        if maximizing_player:
            max_eval = -math.inf
            for idx in self.get_empty_cells():
                board[idx] = "O"
                eval = self.minimax(board, depth + 1, False)
                board[idx] = " "
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = math.inf
            for idx in self.get_empty_cells():
                board[idx] = "X"
                eval = self.minimax(board, depth + 1, True)
                board[idx] = " "
                min_eval = min(min_eval, eval)
            return min_eval

    def reset_board(self):
        self.board = [" " for _ in range(9)]
        for row in self.buttons:
            for button in row:
                button.config(text="")
        self.current_player = "Player 1"

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()

