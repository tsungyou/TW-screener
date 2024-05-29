import customtkinter as ctk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Searcher(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.canvas         = None
        self.pq_loc_dir     = "../tw-stock-screener/database/"
        #
        self.inputBox1 = ctk.CTkEntry(self, placeholder_text='Stock symbol')
        self.inputBox1.grid(row=0, column=0, padx=10, pady=10)

        self.inputButton1 = ctk.CTkButton(self, text='Show Plot', command=self.plotting)
        self.inputButton1.grid(row=0, column=2, padx=10, pady=10)
        self.inputButton1.bind("<Return>", self.plotting)

        self.menu_ma = ctk.CTkOptionMenu(self, values=["20", "60", "120", "100"], command=self.plotting)
        self.menu_ma.grid(row=0, column=3, padx=10, pady=10)

        self.menu_inputDate = ctk.CTkOptionMenu(self, values=['2019', '2020', '2021', '2022', '2023', '2024'], command=self.plotting)
        self.menu_inputDate.grid(row=0, column=4, padx=10, pady=10)

        self.plotting()
    def plotting(self):
        # set ticker default
        ma      = self.menu_ma.get()
        ticker  = self.inputBox1.get()
        date    = self.menu_inputDate.get()
        print(ticker, date, ma)
        if ticker == "":
            ticker = "2330"
        # set ma default
        try:
            tw = self.pq_loc_dir + f"{ticker}_TW.parquet"
            df = pd.read_parquet(tw)
            df = df[df.index >= f'{date}-01-01']
        
        except:
            try:
                two = self.pq_loc_dir + f"{ticker}_TWO.parquet"
                df = pd.read_parquet(two)
                df = df[df.index >= f'{date}-01-01']

            except:
                print("no symbol existed")
        
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None
        df['ma'] = df['Close'].rolling(int(ma)).mean()

        fig, ax = plt.subplots()
        fig.set_size_inches(8,4)
        ax.plot(df['ma'], label='ma')
        ax.plot(df["Close"], label='close')
        ax.set_title(ticker)
        ax.legend()
        fig.subplots_adjust(left=0, right=1, bottom=0, top=1, wspace=0, hspace=0)
        self.canvas = FigureCanvasTkAgg(fig,master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=2, column=0)

plt.plot()