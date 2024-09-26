'''
1.5 Examen Tema 1. Introducción al paradigma de la programación orientada a objetos
(Buscaminas)
'''

import tkinter as tk
import random
from tkinter import messagebox
import time

class Minesweeper:
    def __init__(self, master, rows=10, cols=10, mines=10):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.buttons = []
        self.minefield = []
        self.game_over = False
        self.start_time = None
        self.score = 0
        self.level_scores = []  # Almacena los puntajes de cada nivel
        self.total_score = 0  # Puntaje acumulado

        self.create_menu()  # Menú con opciones
        self.create_widgets()
        self.new_game()  # Iniciar el primer juego

    def create_menu(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        # Menú del juego
        game_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Juego", menu=game_menu)
        game_menu.add_command(label="Nuevo Juego", command=self.new_game)
        game_menu.add_command(label="Instrucciones", command=self.show_instructions)
        game_menu.add_command(label="Ver Puntaje", command=self.show_scores)  # Opción para ver puntajes
        game_menu.add_separator()
        game_menu.add_command(label="Salir", command=self.master.quit)

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

    def new_game(self):
        # Restablecer el juego
        self.game_over = False
        self.start_time = time.time()
        self.score = 0

        # Reiniciar el estado del campo y los botones
        for row in self.buttons:
            for button in row:
                button.config(text="", state="normal", bg="SystemButtonFace", relief=tk.RAISED)

        self.place_mines()  # Colocar minas para el nuevo juego

    def create_widgets(self):
        # Crear botones y agregar al grid
        for row in range(self.rows):
            button_row = []
            for col in range(self.cols):
                button = tk.Button(self.master, width=2, height=1, command=lambda r=row, c=col: self.on_click(r, c))
                button.bind("<Button-3>", lambda e, r=row, c=col: self.on_right_click(r, c))
                button.grid(row=row, column=col)
                button_row.append(button)
            self.buttons.append(button_row)

    def place_mines(self):
        # Crear un campo de minas vacío
        self.minefield = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        # Colocar minas aleatoriamente
        mines_placed = 0
        while mines_placed < self.mines:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            if self.minefield[r][c] == 0:
                self.minefield[r][c] = -1
                mines_placed += 1
        # Calcular los números de las celdas alrededor de las minas
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
        if self.buttons[row][col]['text'] != "":
            return
        button = self.buttons[row][col]
        value = self.minefield[row][col]
        if value > 0:
            button.config(text=str(value), state="disabled", relief=tk.SUNKEN)
        else:
            button.config(text="", state="disabled", relief=tk.SUNKEN)
            # Si el valor es 0, revelar las celdas alrededor
            for i in range(max(0, row - 1), min(self.rows, row + 2)):
                for j in range(max(0, col - 1), min(self.cols, col + 2)):
                    if self.buttons[i][j]['state'] != "disabled":
                        self.reveal_cells(i, j)

    def on_right_click(self, row, col):
        if self.game_over:
            return
        button = self.buttons[row][col]
        if button['text'] == "":
            button.config(text="F", fg="red")  # Marcar como mina
        elif button['text'] == "F":
            button.config(text="")  # Desmarcar

    def reveal_mines(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.minefield[r][c] == -1:
                    self.buttons[r][c].config(text="*", bg="red")

    def check_win(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.minefield[r][c] != -1 and self.buttons[r][c]['state'] != "disabled":
                    return False
        return True

    def show_score(self, win, time_elapsed):
        if win:
            self.score = max(0, 1000 - int(time_elapsed * 10))  # Ejemplo de puntuación basada en tiempo
            messagebox.showinfo("Puntaje", f"¡Has ganado!\nPuntaje: {self.score}\nTiempo: {int(time_elapsed)} segundos")
        else:
            self.score = 0
            messagebox.showinfo("Puntaje", f"¡Has perdido!\nTiempo: {int(time_elapsed)} segundos")

        # Guardar el puntaje de este nivel y actualizar el puntaje total
        self.level_scores.append(self.score)
        self.total_score += self.score

    def show_scores(self):
        # Mostrar los puntajes por nivel y el puntaje total
        score_message = "Puntaje por nivel:\n"
        for i, score in enumerate(self.level_scores):
            score_message += f"Nivel {i + 1}: {score} puntos\n"
        score_message += f"\nPuntaje total: {self.total_score} puntos"
        messagebox.showinfo("Puntajes", score_message)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Buscaminas")
    game = Minesweeper(root)
    root.mainloop()