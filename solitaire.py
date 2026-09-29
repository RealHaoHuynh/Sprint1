import tkinter as tk
from tkinter import ttk, messagebox

class PegSolitaireGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Peg Solitaire Game")
        self.root.resizable(False, False)

        # Game Configuration Defaults
        self.selected_size = tk.StringVar(value="7x7")
        self.selected_type = tk.StringVar(value="English")
        self.selected_peg = None  # Stores (r, c) of currently selected peg

        # Define Board Templates (1: Peg present, 0: Empty space, -1: Invalid position)
        self.boards = {
            "7x7": {
                "English": [
                    [-1, -1,  1,  1,  1, -1, -1],
                    [-1, -1,  1,  1,  1, -1, -1],
                    [ 1,  1,  1,  1,  1,  1,  1],
                    [ 1,  1,  1,  0,  1,  1,  1],  # Center empty
                    [ 1,  1,  1,  1,  1,  1,  1],
                    [-1, -1,  1,  1,  1, -1, -1],
                    [-1, -1,  1,  1,  1, -1, -1]
                ],
                "Diamond": [
                    [-1, -1, -1,  1, -1, -1, -1],
                    [-1, -1,  1,  1,  1, -1, -1],
                    [-1,  1,  1,  1,  1,  1, -1],
                    [ 1,  1,  1,  0,  1,  1,  1],
                    [-1,  1,  1,  1,  1,  1, -1],
                    [-1, -1,  1,  1,  1, -1, -1],
                    [-1, -1, -1,  1, -1, -1, -1]
                ],
                "Hexagon": [
                    [-1, -1,  1,  1,  1, -1, -1],
                    [-1,  1,  1,  1,  1, -1, -1],
                    [ 1,  1,  1,  1,  1,  1, -1],
                    [ 1,  1,  1,  0,  1,  1,  1],
                    [-1,  1,  1,  1,  1,  1,  1],
                    [-1, -1,  1,  1,  1,  1, -1],
                    [-1, -1,  1,  1,  1, -1, -1]
                ]
            }
        }

        self.current_board = []
        self.grid_buttons = {}

        self.create_widgets()
        self.start_new_game()

    def create_widgets(self):
        # Top Frame: Controls
        top_frame = ttk.Frame(self.root, padding="10")
        top_frame.pack(side=tk.TOP, fill=tk.X)

        # Right-aligned Board Size label/selector
        ttk.Label(top_frame, text="Board size").grid(row=0, column=2, padx=5, sticky=tk.E)
        size_cb = ttk.Combobox(top_frame, textvariable=self.selected_size, values=["7x7"], width=5, state="readonly")
        size_cb.grid(row=0, column=3, padx=5, sticky=tk.W)

        # Board Type Label & Options Frame
        ttk.Label(top_frame, text="Board Type", font=('Arial', 10, 'bold')).grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(10, 2))

        type_frame = ttk.Frame(top_frame)
        type_frame.grid(row=2, column=0, columnspan=2, sticky=tk.W)

        rb_english = ttk.Radiobutton(type_frame, text="English", variable=self.selected_type, value="English")
        rb_english.pack(anchor=tk.W)
        rb_hex = ttk.Radiobutton(type_frame, text="Hexagon", variable=self.selected_type, value="Hexagon")
        rb_hex.pack(anchor=tk.W)
        rb_diamond = ttk.Radiobutton(type_frame, text="Diamond", variable=self.selected_type, value="Diamond")
        rb_diamond.pack(anchor=tk.W)

        # New Game Button
        btn_new_game = ttk.Button(top_frame, text="New Game", command=self.start_new_game)
        btn_new_game.grid(row=2, column=3, padx=10, pady=10, sticky=tk.SE)

        # Separator Line
        ttk.Separator(self.root, orient='horizontal').pack(fill='x', padx=10, pady=5)

        # Center Board Container Frame
        self.board_frame = ttk.Frame(self.root, padding="10")
        self.board_frame.pack(side=tk.TOP)

    def start_new_game(self):
        # Clear existing grid elements
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        self.grid_buttons.clear()
        self.selected_peg = None

        # Load board layout
        size = self.selected_size.get()
        b_type = self.selected_type.get()
        
        # Deep copy template layout
        template = self.boards[size][b_type]
        self.current_board = [row[:] for row in template]

        # Render grid UI
        for r in range(len(self.current_board)):
            for c in range(len(self.current_board[0])):
                cell_val = self.current_board[r][c]
                if cell_val != -1:
                    btn = tk.Button(
                        self.board_frame,
                        width=4,
                        height=2,
                        font=('Arial', 12, 'bold'),
                        command=lambda row=r, col=c: self.handle_cell_click(row, col)
                    )
                    btn.grid(row=r, column=c, padx=1, pady=1)
                    self.grid_buttons[(r, c)] = btn

        self.update_ui()

    def update_ui(self):
        for (r, c), btn in self.grid_buttons.items():
            val = self.current_board[r][c]
            if (r, c) == self.selected_peg:
                btn.config(text="●", bg="#4CAF50", fg="white", relief=tk.SUNKEN)  # Highlighted selected peg
            elif val == 1:
                btn.config(text="●", bg="#E0E0E0", fg="black", relief=tk.RAISED)  # Peg present
            elif val == 0:
                btn.config(text="○", bg="#FFFFFF", fg="gray", relief=tk.RAISED)   # Empty hole

    def handle_cell_click(self, r, c):
        # If no peg is currently selected, attempt to select one
        if self.selected_peg is None:
            if self.current_board[r][c] == 1:
                self.selected_peg = (r, c)
                self.update_ui()
        else:
            sr, sc = self.selected_peg
            
            # Clicked on the same peg: deselect
            if (sr, sc) == (r, c):
                self.selected_peg = None
                self.update_ui()
            # Clicked on an empty spot: attempt to execute a jump move
            elif self.current_board[r][c] == 0:
                if self.is_valid_move(sr, sc, r, c):
                    self.execute_move(sr, sc, r, c)
                    self.selected_peg = None
                    self.update_ui()
                    self.check_game_over()
                else:
                    # Invalid move: change selection if clicking another peg
                    if self.current_board[r][c] == 1:
                        self.selected_peg = (r, c)
                    else:
                        self.selected_peg = None
                    self.update_ui()
            # Clicked on another peg: switch selection
            elif self.current_board[r][c] == 1:
                self.selected_peg = (r, c)
                self.update_ui()

    def is_valid_move(self, sr, sc, er, ec):
        # Check standard orthogonal jump (distance of 2 horizontally or vertically)
        row_diff = abs(er - sr)
        col_diff = abs(ec - sc)

        if (row_diff == 2 and col_diff == 0) or (row_diff == 0 and col_diff == 2):
            mid_r = (sr + er) // 2
            mid_c = (sc + ec) // 2
            # Must jump over an existing peg
            return self.current_board[mid_r][mid_c] == 1
        return False

    def execute_move(self, sr, sc, er, ec):
        mid_r = (sr + er) // 2
        mid_c = (sc + ec) // 2

        self.current_board[sr][sc] = 0
        self.current_board[mid_r][mid_c] = 0
        self.current_board[er][ec] = 1

    def check_game_over(self):
        pegs_remaining = 0
        valid_moves_exist = False

        for r in range(len(self.current_board)):
            for c in range(len(self.current_board[0])):
                if self.current_board[r][c] == 1:
                    pegs_remaining += 1
                    # Check if this peg has any valid jumps
                    for dr, dc in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < len(self.current_board) and 0 <= nc < len(self.current_board[0]):
                            if self.current_board[nr][nc] == 0 and self.is_valid_move(r, c, nr, nc):
                                valid_moves_exist = True

        if pegs_remaining == 1:
            messagebox.showinfo("Game Over", "Congratulations! You won!")
        elif not valid_moves_exist:
            messagebox.showinfo("Game Over", f"No more valid moves! Pegs remaining: {pegs_remaining}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PegSolitaireGUI(root)
    root.mainloop()