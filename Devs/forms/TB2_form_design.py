2B Form design

import tkinter as tk
from tkinter import font
import customtkinter as ctk
from customtkinter import CTkFont

from Util.util_config import FONT_AWSOME_20, FONT_ROBOTO_15, FONT_ARIAL_15, FG_TEXTBOX

from Code.T2B_code import T2BCode
from Code.convertTo import ConvertTo

class T2BFormDesign():
    def __init__(self, main_panel):
        self.create_frames(main_panel)
        self.create_top_widgets()
        self.create_center_widgets()
        self.create_bottom_widgets()
        
    def create_frames(self, main_panel):
        self.top_frame = ctk.CTkFrame(main_panel)
        self.top_frame.pack(side = 'top', fill = 'both', expand = True)

        self.center_frame = ctk.CTkFrame(main_panel)
        self.center_frame.pack(side = 'top', fill = 'both', expand = True)

        self.bottom_frame = ctk.CTkFrame(main_panel)
        self.bottom_frame.pack(side = 'top', fill = 'both', expand = False)

    def create_top_widgets(self):
        ancho = 20
        alto = 1

        self.label_input = ctk.CTkLabel(self.top_frame, text = "Texto a Convertir", font = FONT_AWSOME_20)
        self.label_input.pack(pady=5, side = 'top', fill='both', expand=False)    

        # Crear Entry widget
        self.textBox_input = ctk.CTkTextbox(
            self.top_frame, font = FONT_ARIAL_15, fg_color = FG_TEXTBOX
        )
        self.textBox_input.pack(padx=100, pady=5, side = 'top', fill='both', expand=True)
        self.textBox_input.bind("<KeyRelease>", self.trad_2_braille)

    def create_center_widgets(self):
        self.label_output = ctk.CTkLabel(
            self.center_frame, text = "Texto en Braille", font = FONT_AWSOME_20
            )
        self.label_output.pack(pady=5, side = 'top', fill='both', expand=False)

        self.textBox_output = ctk.CTkTextbox(
            self.center_frame, font = FONT_ARIAL_15, fg_color = FG_TEXTBOX
            )
        self.textBox_output.pack(padx=100, pady=5, side = 'top', fill='both', expand=True)
        
    def create_bottom_widgets(self):
        # Crear botones
        self.button_clear_box = ctk.CTkButton(self.bottom_frame)
        self.button_img = ctk.CTkButton(self.bottom_frame)
        self.button_espejo = ctk.CTkButton(self.bottom_frame)

        buttons_info =[
            ("Limpiar", self.button_clear_box, "\uf00d", self.clear_textbox),
            ("IMG", self.button_img, "\uf04b", self.to_img_normal),
            ("PDF", self.button_espejo, "\uf04b", self.to_pdf_espejo)
        ]

        for text, button, icon, cm in buttons_info:
            ancho = 20
            alto = 1

            self.bottom_buttons_config(button, text, icon, FONT_ROBOTO_15, ancho, alto, cm)
    
    def bottom_buttons_config(self, button, text, icon, font, ancho, alto, cm):
        button.configure(
            text = f"{icon}  {text}", anchor = "c", font = font, width = ancho, height = alto, command = cm
        )
        button.pack(padx = 25, pady = 5, side = 'right', fill = 'y',expand = True)


    #########
    def trad_2_braille(self, event):
        if not self.get_text():
            new_text = " "
        else:
            print("Traducir")
            
            new_text = self.get_text()
            print(new_text)
    
            T2BCode(new_text)
            final_text = T2BCode.get_final_braille()

            self.textBox_output.delete("1.0", 'end')
            self.textBox_output.insert("1.0", final_text)

    def clear_textbox(self):
        print("Limpiar")
        self.textBox_input.delete("1.0", 'end')
        self.textBox_output.delete("1.0", 'end')
        T2BCode.set_final_braille()
    
    def get_text(self):
        return self.textBox_input.get("1.0", 'end-1c')
    
    def get_text_braille(self, text):
        return self.trad_2_braille()
    
    def clear_panel(self, panel):
        for widget in panel.winfo_children():
            widget.destroy()

    def to_pdf_espejo(self):
        print("PDF Espejo")
        ConvertTo().generar_pdf_espejo()

    def to_img_normal(self):
        print("IMG Normal")
        ConvertTo().convert_2_image()