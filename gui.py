#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created by lativ on 13/10/18 at 08:17
"""

from tkinter import Tk, Label, Entry, IntVar, StringVar, Button, Radiobutton, Frame
from tkinter import N, S, W, E

class Matrix:

    def __init__(self, master):
        self.master = master
        master.title("PO Game Theory to LP")

        self.number_a = 0
        self.number_b = 0
        self.payoff_matrix = [[0 for _ in range(self.number_b)] for _ in range(self.number_a)]

        self.mainframe = Frame(root)

        # Validate entries
        vcmd_a = master.register(self.validate_a)
        vcmd_b = master.register(self.validate_b)
        vcmd_matrix = master.register(self.validate_matrix)

        # Create widgets
        self.na_label = Label(self.mainframe, text="Number of Strategies for A: ")
        self.na_entry = Entry(self.mainframe, width=3, validate="key", validatecommand=(vcmd_a, '%P'))
        self.na_entry.insert(0, "0")

        self.nb_label = Label(self.mainframe, text="Number of Strategies for B: ")
        self.nb_entry = Entry(self.mainframe, width=3, validate="key", validatecommand=(vcmd_b, '%P'))
        self.nb_entry.insert(0, "0")

        matrix = StringVar()
        self.payoff_label = Label(self.mainframe, text="Pay-off matrix: ")
        self.payoff_entry = Entry(self.mainframe, width=15, textvariable=matrix)

        # Gambiarra?
        self.payoff_entry_validate = Button(self.mainframe, text="Validate matrix",
                                            command=lambda: self.validate_matrix(self.payoff_entry.get()))

        MODES = [("Pure strategy", "P"), ("Mixed strategy", "M")]
        strategy = StringVar()
        strategy.set("M")
        strat_bts = []
        for text, mode in MODES:
            b = Radiobutton(self.mainframe, text=text, variable=strategy, value=mode)
            strat_bts.append(b)

        self.make_matrix_button = Button(self.mainframe, text="Make matrix", command=self.make_matrix)

        self.solve_game_button = Button(self.mainframe, text="Solve", command=self.solve_game)

        # LAYOUT
        self.mainframe.grid(padx=5, pady=5)

        self.na_label.grid()
        self.na_entry.grid(column=1, row=0)

        self.nb_label.grid()
        self.nb_entry.grid(column=1, row=1)

        self.payoff_label.grid(sticky=W)
        self.payoff_entry.grid(column=1, row=2, sticky=E)
        self.payoff_entry_validate.grid(column=2, row=2, sticky=E)

        actual_column = 0
        for b in strat_bts:
            b.grid(column=actual_column, row=3, sticky=W)
            actual_column += 1

        self.make_matrix_button.grid(column=0, row=4, sticky=W)

        self.solve_game_button.grid(column=1, row=4, sticky=W)


    def validate_a(self, new_text):
        if not new_text:
            self.number_a = 0
            return True

        try:
            self.number_a = int(new_text)
            return True
        except:
            return False

    def validate_b(self, new_text):
        if not new_text:
            self.number_b = 0
            return True

        try:
            self.number_b = int(new_text)
            return True
        except:
            return False

    def validate_matrix(self, new_text):
        if not new_text:
            self.payoff_matrix = [[0 for _ in range(self.number_b)]
                                 for _ in range(self.number_a)]
            return True

        try:
            numbers = [int(x) for x in new_text.split()]

            self.payoff_matrix = [[0 for _ in range(self.number_b)]
                                  for _ in range(self.number_a)]

            if len(numbers) < self.number_a * self.number_b:
                return False

            for i in range(self.number_a):
                for j in range(self.number_b):
                    self.payoff_matrix[i][j] = numbers[self.number_b * i + j]
            return True
        except:
            return False

    def make_matrix(self):
        # Labels for B
        matrix_frame = Frame(self.mainframe)
        matrix_frame.grid(padx=5, pady=5)
        b_lbs = []
        for i in range(self.number_b):
            lb = Label(matrix_frame, text="B{}".format(i+1))
            lb.grid(column=i+1, row=0)
            b_lbs.append(lb)

        a_lbs = []
        for i in range(self.number_a):
            lb = Label(matrix_frame, text="A{}".format(i+1))
            lb.grid(column=0, row=i+1)
            a_lbs.append(lb)

        payoff_lbs = []
        for i in range(self.number_a):
            for j in range(self.number_b):
                lb = Label(matrix_frame, text=str(self.payoff_matrix[i][j]))
                lb.grid(column=j+1, row=i+1)
                payoff_lbs.append(lb)


    def solve_game(self):
        row_min = [min(row) for row in self.payoff_matrix]
        maximin_val = max(row_min)
        maximin_idx = row_min.index(maximin_val)
        print("{} -> Maximin: {} at index = {}".format(row_min, maximin_val, maximin_idx))

        print("Column max")
        payoff_matrix_transp = [[row[j] for row in self.payoff_matrix] for j in range(self.number_b)]
        col_max = [max(col) for col in payoff_matrix_transp]
        minimax_val = min(col_max)
        minimax_idx = col_max.index(minimax_val)
        print("{} -> Minimax: {} at index = {}".format(col_max, minimax_val, minimax_idx))


        if maximin_val == minimax_val:
            print("Best strategy: (A{}, B{})".format(maximin_idx+1, minimax_idx+1))
            print("Value of the game: {}".format(maximin_val))
        else:
            print("There is not a pure strategy solution.")
            print("Value of the game is between {} and {}.".format(maximin_val, minimax_val))
            print("Trying mixed strategy solution... ")
            self._solve_game_mixed_strategy()

    def _solve_game_mixed_strategy(self):
        print("Not implemented!")


root = Tk()
game = Matrix(root)
root.mainloop()

"""
Max z = v

subject to

v - 3x1 + 2x2 + 5x3 <= 0
v + x1 - 4x2 + 6x3 <= 0
v + 3x1 + x2 - 2x3 <= 0
x1 + x2 + x3 = 1
x1, x2, x3 >=0
v unrestricted

v = min ( sum i to m a_i1 * x_i, sum i to m a_i2 * xi, ..., sum i to m a_in * xi )

x1 = .39
x2 = .31
x3 = .29
v  = -0.91
"""


