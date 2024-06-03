# Building form design

import tkinter as tk
import customtkinter as ctk
from Util.util_config import COLOR_FONDO_BUILDING, FONT_AWSOME_20

class BuildingFormDesign():
    
    def __init__(self, main_panel):
        self.top_bar = ctk.CTkFrame(main_panel)
        self.top_bar.pack(side='top', fill='both', expand = False)

        self.bottom_bar = ctk.CTkFrame(main_panel)
        self.bottom_bar.pack(side='bottom', fill='both', expand = True)

        self.labelTitulo = tk.Label(
            self.top_bar, text = "EN CONSTRUCCION"
        )
        self.labelTitulo = ctk.CTkLabel(
            self.top_bar, text = "EN CONSTRUCCION"
        )
        self.labelTitulo.configure(
            text_color = "DARKRED", font = FONT_AWSOME_20,
            fg_color = COLOR_FONDO_BUILDING
        )
        self.labelTitulo.pack(side='top', fill='both', expand = False)