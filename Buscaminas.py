'''
1.5 Examen Tema 1. Introducción al paradigma de la programación orientada a objetos
(Buscaminas)
'''

import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import time

class MinesweeperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Buscaminas")
        self.scores = []  # Lista para almacenar los puntajes
        self.start_screen()

    def start_screen(self):
        self.clear_window()
        self.root.geometry("300x300")

        title = tk.Label(self.root, text="Buscaminas", font=("Helvetica", 18, "bold"))
        title.pack(pady=20)

        btn_start = tk.Button(self.root, text="Iniciar Juego", command=self.choose_mines)
        btn_start.pack(pady=10)

        btn_instructions = tk.Button(self.root, text="Instrucciones", command=self.show_instructions)
        btn_instructions.pack(pady=10)

        btn_scores = tk.Button(self.root, text="Puntuaciones", command=self.show_scores)
        btn_scores.pack(pady=10)

        btn_exit = tk.Button(self.root, text="Salir", command=self.root.quit)
        btn_exit.pack(pady=10)

    def choose_mines(self):
        mines = simpledialog.askinteger("Cantidad de Minas", "Ingresa la cantidad de minas:", minvalue=7, maxvalue=99)
        if mines is not None:
            self.start_game(mines)

    def start_game(self, mines):
        self.clear_window()
        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack()
        self.minesweeper = Minesweeper(self.game_frame, self, mines=mines)
        self.minesweeper.new_game()

    def show_instructions(self):
        instructions = (
            "Instrucciones de Buscaminas:\n"
            "1. El objetivo es encontrar todas las minas sin hacer clic en ellas.\n"
            "2. Haz clic izquierdo en una celda para revelarla.\n"
            "3. Si la celda contiene un número, indica cuántas minas hay alrededor.\n"
            "4. Haz clic derecho para marcar una celda como sospechosa de contener una mina.\n"
            "5. El juego termina cuando revelas todas las celdas sin minas o haces clic en una mina."
        )
        messagebox.showinfo("Instrucciones", instructions)

    def show_scores(self):
        if not self.scores:
            messagebox.showinfo("Puntajes", "No hay puntajes disponibles aún.")
        else:
            total_score = sum(self.scores)
            score_message = "Puntajes por partidas:\n\n"
            for i, score in enumerate(self.scores, 1):
                score_message += f"Partida {i}: {score} puntos\n"
            score_message += f"\nPuntaje total: {total_score} puntos"
            messagebox.showinfo("Puntajes", score_message)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

class Minesweeper:
    def __init__(self, master, app, rows=10, cols=10, mines=10):
        self.master = master
        self.app = app
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.buttons = []
        self.minefield = []
        self.game_over = False
        self.start_time = None
        self.score = 0

        self.create_widgets()

    def create_widgets(self):
        """Crea el tablero de botones."""
        for row in range(self.rows):
            button_row = []
            for col in range(self.cols):
                button = tk.Button(self.master, width=2, height=1, command=lambda r=row, c=col: self.on_click(r, c))
                button.bind("<Button-3>", lambda e, r=row, c=col: self.on_right_click(r, c))
                button.grid(row=row, column=col)
                button_row.append(button)
            self.buttons.append(button_row)

    def new_game(self):
        """Reinicia el estado del juego sin destruir el tablero."""
        self.game_over = False
        self.start_time = time.time()
        self.score = 0
        for row in self.buttons:
            for button in row:
                button.config(text="", state="normal", bg="SystemButtonFace", relief=tk.RAISED)
        self.place_mines()

    def place_mines(self):
        """Coloca minas aleatoriamente en el tablero."""
        self.minefield = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        mines_placed = 0
        while mines_placed < self.mines:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            if self.minefield[r][c] == 0:
                self.minefield[r][c] = -1
                mines_placed += 1
        # Calcular los números alrededor de las minas
        for r in range(self.rows):
            for c in range(self.cols):
                if self.minefield[r][c] == -1:
                    continue
                count = 0
                for i in range(max(0, r - 1), min(self.rows, r + 2)):
                    for j in range(max(0, c - 1), min(self.cols, c + 2)):
                        if self.minefield[i][j] == -1:
                            count += 1
                self.minefield[r][c] = count

    def on_click(self, row, col):
        """Maneja el evento de clic en una celda."""
        if self.game_over:
            return
        button = self.buttons[row][col]
        if self.minefield[row][col] == -1:
            button.config(text="*", bg="red")
            self.game_over = True
            end_time = time.time()
            self.show_score(False, end_time - self.start_time)
            self.reveal_mines()
            messagebox.showinfo("Game Over", "¡Has perdido!")
        else:
            self.reveal_cells(row, col)
            if self.check_win():
                self.game_over = True
                end_time = time.time()
                self.show_score(True, end_time - self.start_time)
                messagebox.showinfo("Ganaste", "¡Felicidades! Has encontrado todas las minas.")

    def reveal_cells(self, row, col):
        """Revela celdas vacías recursivamente."""
        if self.buttons[row][col]['text'] != "":
            return
        button = self.buttons[row][col]
        value = self.minefield[row][col]
        if value > 0:
            button.config(text=str(value), state="disabled", relief=tk.SUNKEN)
        else:
            button.config(text="", state="disabled", relief=tk.SUNKEN)
            for i in range(max(0, row - 1), min(self.rows, row + 2)):
                for j in range(max(0, col - 1), min(self.cols, col + 2)):
                    if self.buttons[i][j]['state'] != "disabled":
                        self.reveal_cells(i, j)

    def on_right_click(self, row, col):
        """Maneja el evento de clic derecho (marcar bandera)."""
        if self.game_over:
            return
        button = self.buttons[row][col]
        if button['text'] == "":
            button.config(text="F", fg="red")
        elif button['text'] == "F":
            button.config(text="")

    def reveal_mines(self):
        """Revela todas las minas después de perder."""
        for r in range(self.rows):
            for c in range(self.cols):
                if self.minefield[r][c] == -1:
                    self.buttons[r][c].config(text="*", bg="red")

    def check_win(self):
        """Verifica si el jugador ha ganado."""
        for r in range(self.rows):
            for c in range(self.cols):
                if self.minefield[r][c] != -1 and self.buttons[r][c]['state'] != "disabled":
                    return False
        return True

    def show_score(self, win, time_elapsed):
        """Muestra el puntaje y los botones al finalizar el juego."""
        if win:
            self.score = max(0, 1000 - int(time_elapsed * 10))
            messagebox.showinfo("Puntaje", f"¡Has ganado!\nPuntaje: {self.score}\nTiempo: {int(time_elapsed)} segundos")
        else:
            self.score = 0
            messagebox.showinfo("Puntaje", f"¡Has perdido!\nTiempo: {int(time_elapsed)} segundos")

        # Guardar el puntaje en la lista
        self.app.scores.append(self.score)

        # Mostrar botones de "Nuevo Juego" y "Regresar al Menú"
        btn_new_game = tk.Button(self.master, text="Nuevo Juego", command=self.app.choose_mines)
        btn_new_game.grid(row=self.rows + 1, column=0, columnspan=self.cols // 2, pady=10)

        btn_menu = tk.Button(self.master, text="Regresar al Menú", command=self.app.start_screen)
        btn_menu.grid(row=self.rows + 1, column=self.cols // 2, columnspan=self.cols // 2, pady=10)

# Ejecución de la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = MinesweeperApp(root)
    root.mainloop()