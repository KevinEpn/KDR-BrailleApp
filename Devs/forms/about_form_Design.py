# About form design

import tkinter as tk
import customtkinter as ctk
import util.util_ventana as util_vent
from util.util_config import FONT_AWSOME_20

class AboutFormDesign(ctk.CTkToplevel):
    
    def __init__(self) -> None:
        super().__init__()
        self.config_window()
        self.create_widgets()

    def config_window(self):
        # configuracion incial de la ventana
        self.title("About")
        w, h = 400, 100 
        self.geometry(f'{w}x{h}')
        self.resizable(False, False)
        self.grab_set()
        util_vent.centrar_ventana(self, w, h)

    def create_widgets(self):
        # configuracion de los widgets
        self.labelVersion = ctk.CTkLabel(
            self, text = "Version : 1.0"
        )
        self.labelVersion.configure(
            font = FONT_AWSOME_20            
        )
        self.labelVersion.pack(pady = 10)

        self.labelAutor = ctk.CTkLabel(
            self, text = "Autor : KDR CONSULTECH"
        )
        self.labelAutor.configure(
            font = FONT_AWSOME_20
            
        )
        self.labelAutor.pack(pady = 10)