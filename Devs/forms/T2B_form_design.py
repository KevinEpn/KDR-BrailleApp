# T2B Form design
import tkinter as tk
from tkinter import font, messagebox
import customtkinter as ctk
from customtkinter import CTkFont
from util.util_config import FONT_AWSOME_20, FONT_ROBOTO_15, FONT_ARIAL_15, FG_TEXTBOX
from src.T2B_code import T2BCode
from src.convertTo import ConvertTo
import threading

class T2BFormDesign():
    # Define constants for duplicated literals
    COPY_BRAILLE_TEXT = "Copiar Braille"
    NO_TRANSLATED_TEXT_WARNING = "No hay texto traducido. Por favor, realiza una conversión antes."
    
    def __init__(self, main_panel):
        self.traslator = T2BCode()
        self.converter = ConvertTo()
        self.create_frames(main_panel)
        self.create_top_widgets()
        self.create_center_widgets()
        self.create_bottom_widgets()
        
    def create_frames(self, main_panel):
        self.top_frame = ctk.CTkFrame(main_panel)
        self.top_frame.pack(side='top', fill='both', expand=True)

        self.center_frame = ctk.CTkFrame(main_panel)
        self.center_frame.pack(side='top', fill='both', expand=True)

        self.bottom_frame = ctk.CTkFrame(main_panel)
        self.bottom_frame.pack(side='top', fill='both', expand=False)

    def create_top_widgets(self):
        self.label_input = ctk.CTkLabel(self.top_frame, text="Texto a Convertir", font=FONT_AWSOME_20)
        self.label_input.pack(pady=5, side='top', fill='both', expand=False)    

        # Crear Entry widget
        self.textbox_input = ctk.CTkTextbox(
            self.top_frame, font=FONT_ARIAL_15, fg_color=FG_TEXTBOX, wrap='word'
        )
        self.textbox_input.pack(padx=100, pady=5, side='top', fill='both', expand=True)
        self.textbox_input.bind("<<Modified>>", self.trad_2_braille)
        self.textbox_input.edit_modified(False)

    def create_center_widgets(self):
        self.label_output = ctk.CTkLabel(
            self.center_frame, text="Texto en Braille", font=FONT_AWSOME_20
        )
        self.label_output.pack(pady=5, side='top', fill='both', expand=False)

        # Crear textbox de salida
        self.textbox_output = ctk.CTkTextbox(
            self.center_frame, font=FONT_ARIAL_15, fg_color=FG_TEXTBOX, wrap='word', state='disabled'
        )
        self.textbox_output.pack(padx=100, pady=5, side='top', fill='both', expand=True)

        # Deshabilitar eventos de teclado y mouse en el textbox de salida
        self.desabilitar_eventos_textbox()

    def desabilitar_eventos_textbox(self):
        for event in ["<Button-1>", "<B1-Motion>", "<Double-1>", "<Triple-1>",
                      "<ButtonRelease-1>", "<Button-2>", "<B2-Motion>", "<Double-2>", "<Triple-2>",
                      "<ButtonRelease-2>", "<Button-3>", "<B3-Motion>", "<Double-3>", "<Triple-3>",
                      "<ButtonRelease-3>", "<Motion>", "<Enter>", "<Leave>", "<MouseWheel>", "<Button-4>",
                      "<Button-5>", "<Shift-Button-1>", "<Shift-B1-Motion>", "<Control-Button-1>",
                      "<Control-B1-Motion>", "<Shift-ButtonRelease-1>", "<Control-ButtonRelease-1>",
                      "<Control-Shift-Button-1>", "<Control-Shift-B1-Motion>"]:
            self.textbox_output.bind(event, self.disable_event)

        for event in ["<Key>", "<Control-Key>", "<Shift-Key>", "<Alt-Key>", "<Meta-Key>", "<KeyPress>", "<KeyRelease>"]:
            self.textbox_output.bind(event, self.disable_event)

    def disable_event(self, event):
        return "break"
        
    def create_bottom_widgets(self):
        # Crear botones
        self.button_clear_box = ctk.CTkButton(self.bottom_frame)
        self.button_img = ctk.CTkButton(self.bottom_frame)
        self.button_espejo = ctk.CTkButton(self.bottom_frame)
        self.button_copy_braille = ctk.CTkButton(self.bottom_frame, text=self.COPY_BRAILLE_TEXT, command=self.copy_braille)

        buttons_info = [
            ("Limpiar", self.button_clear_box, "\uf00d", self.clear_textbox),
            ("IMG", self.button_img, "\uf1c5", self.to_img_normal),
            ("PDF", self.button_espejo, "\uf1c1", self.to_pdf_espejo),
            (self.COPY_BRAILLE_TEXT, self.button_copy_braille, "\uf0c5", self.copy_braille)
        ]

        for text, button, icon, cm in buttons_info:
            self.bottom_buttons_config(button, text, icon, FONT_ROBOTO_15, cm)
        
    def bottom_buttons_config(self, button, text, icon, font, cm):
        button.configure(
            text=f"{icon}  {text}", anchor="c", font=font, width=20, height=1, command=cm
        )
        button.pack(padx=25, pady=5, side='right', fill='y', expand=True)

    def trad_2_braille(self, event):
        try:
            new_text = self.get_text()
            final_text = self.traslator.texto_a_braile(new_text)
            self.textbox_output.configure(state='normal')
            self.textbox_output.delete("1.0", 'end-1c')
            self.textbox_output.insert("1.0", final_text)
            self.textbox_output.configure(state='disabled')
            self.textbox_input.edit_modified(False)
        except Exception as e:
            messagebox.showerror("Error", f"Error al convertir el texto a Braille: {e}")
        
    def clear_textbox(self):
        if not self.textbox_output.get("1.0", 'end-1c').strip():
            messagebox.showwarning("Advertencia", self.NO_TRANSLATED_TEXT_WARNING)
            return
        if messagebox.askyesno("Confirmación", "¿Estás seguro de que deseas limpiar el texto? Este cambio no se puede deshacer"):
            self.textbox_input.delete("1.0", 'end')
            self.textbox_output.delete("1.0", 'end')
            self.traslator.set_final_braille()

    def get_text(self):
        return self.textbox_input.get("1.0", 'end-1c')

    def get_text_braille(self):
        return self.trad_2_braille()

    def clear_panel(self, panel):
        for widget in panel.winfo_children():
            widget.destroy()

    def to_pdf_espejo(self):
        if not self.textbox_output.get("1.0", 'end-1c').strip():
            messagebox.showwarning("Advertencia", self.NO_TRANSLATED_TEXT_WARNING)
            return
        self.converter.generar_pdf_espejo()

    def to_img_normal(self):
        if not self.textbox_output.get("1.0", 'end-1c').strip():
            messagebox.showwarning("Advertencia", self.NO_TRANSLATED_TEXT_WARNING)
            return
        self.converter.convert_2_image()

    def copy_braille(self):
        # Verifica si el textBox_output está vacío
        if not self.textbox_output.get("1.0", 'end-1c').strip():
            messagebox.showwarning("Advertencia", self.NO_TRANSLATED_TEXT_WARNING)
            return
    
        self.textbox_output.configure(state='normal')
        self.textbox_output.clipboard_clear()
        self.textbox_output.clipboard_append(self.textbox_output.get("1.0", 'end-1c'))
        self.textbox_output.configure(state='disabled')
        messagebox.showinfo(self.COPY_BRAILLE_TEXT, "El texto en Braille ha sido copiado.")
