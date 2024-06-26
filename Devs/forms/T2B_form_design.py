# T# T2B Form design

import tkinter as tk
from tkinter import font, messagebox, messagebox
import customtkinter as ctk
from customtkinter import CTkFont
from util.util_config import FONT_AWSOME_20, FONT_ROBOTO_15, FONT_ARIAL_15, FG_TEXTBOX
from src.T2B_code import T2BCode
from src.convertTo import ConvertTo
import threading

class T2BFormDesign():
    def __init__(self, main_panel):
        self.traslator = T2BCode()
        self.converter = ConvertTo()
        self.is_recording = False
        self.create_frames(main_panel)
        self.create_top_widgets()
        self.create_center_widgets()
        self.create_bottom_widgets()
        
    def create_frames(self, main_panel):
        self.top_frame = ctk.CTkFrame(main_panel)
        self.top_frame.pack(side='top', fill='both', expand=True)
        self.top_frame.pack(side='top', fill='both', expand=True)

        self.center_frame = ctk.CTkFrame(main_panel)
        self.center_frame.pack(side='top', fill='both', expand=True)
        self.center_frame.pack(side='top', fill='both', expand=True)

        self.bottom_frame = ctk.CTkFrame(main_panel)
        self.bottom_frame.pack(side='top', fill='both', expand=False)
        self.bottom_frame.pack(side='top', fill='both', expand=False)

    def create_top_widgets(self):
        ancho = 20
        alto = 1

        self.label_input = ctk.CTkLabel(self.top_frame, text="Texto a Convertir", font=FONT_AWSOME_20)
        self.label_input.pack(pady=5, side='top', fill='both', expand=False)    

        # Crear Entry widget
        self.textBox_input = ctk.CTkTextbox(
            self.top_frame, font=FONT_ARIAL_15, fg_color=FG_TEXTBOX
        )
        self.textBox_input.pack(padx=100, pady=5, side='top', fill='both', expand=True)
        self.textBox_input.bind("<<Modified>>", self.trad_2_braille)
        self.textBox_input.edit_modified(False)

    def create_center_widgets(self):
        self.label_output = ctk.CTkLabel(
            self.center_frame, text="Texto en Braille", font=FONT_AWSOME_20
        )
        self.label_output.pack(pady=5, side='top', fill='both', expand=False)

        # Crear textbox de salida
        self.textBox_output = ctk.CTkTextbox(
            self.center_frame, font=FONT_ARIAL_15, fg_color=FG_TEXTBOX, state='disabled'
        )
        self.textBox_output.pack(padx=100, pady=5, side='top', fill='both', expand=True)

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
            self.textBox_output.bind(event, self.disable_event)

        for event in ["<Key>", "<Control-Key>", "<Shift-Key>", "<Alt-Key>", "<Meta-Key>", "<KeyPress>", "<KeyRelease>"]:
            self.textBox_output.bind(event, self.disable_event)

    def disable_event(self, event):
        return "break"
        
    def create_bottom_widgets(self):
        # Crear botones
        self.button_clear_box = ctk.CTkButton(self.bottom_frame)
        self.button_img = ctk.CTkButton(self.bottom_frame)
        self.button_espejo = ctk.CTkButton(self.bottom_frame)
        self.button_start_recording = ctk.CTkButton(self.bottom_frame, command=self.start_recording)
        self.button_stop_recording = ctk.CTkButton(self.bottom_frame, command=self.stop_recording, state='disabled')
        self.button_copy_braille = ctk.CTkButton(self.bottom_frame, text="Copiar Braille", command=self.copy_braille)

        buttons_info = [
            ("Limpiar", self.button_clear_box, "\uf00d", self.clear_textbox),
            ("IMG", self.button_img, "\uf04b", self.to_img_normal),
            ("PDF", self.button_espejo, "\uf04b", self.to_pdf_espejo),
            ("Por Voz",self.button_start_recording,"\uf04b", self.start_recording),
            ("Detener Grabación",self.button_stop_recording,"\uf04b", self.stop_recording),          
            ("Copiar", self.button_copy_braille, "\uf0c5", self.copy_braille)
        ]

        for text, button, icon, cm in buttons_info:
            ancho = 20
            alto = 1
            self.bottom_buttons_config(button, text, icon, FONT_ROBOTO_15, ancho, alto, cm)
        
        self.button_start_recording.pack(padx=25, pady=5, side='left', fill='y', expand=True)
        self.button_stop_recording.pack(padx=25, pady=5, side='left', fill='y', expand=True)

    def bottom_buttons_config(self, button, text, icon, font, ancho, alto, cm):
        button.configure(
            text=f"{icon}  {text}", anchor="c", font=font, width=ancho, height=alto, command=cm
        )
        button.pack(padx=25, pady=5, side='right', fill='y', expand=True)

    def trad_2_braille(self, event):
        new_text = self.get_text()
        final_text = self.traslator.texto_a_braile(new_text)
        self.textBox_output.configure(state='normal')
        self.textBox_output.delete("1.0", 'end-1c')
        self.textBox_output.insert("1.0", final_text)
        self.textBox_output.configure(state='disabled')
        self.textBox_input.edit_modified(False)

    def clear_textbox(self):
        self.textBox_input.delete("1.0", 'end')
        self.textBox_output.delete("1.0", 'end')
        self.traslator.set_final_braille()

    def get_text(self):
        return self.textBox_input.get("1.0", 'end-1c').strip()

    def get_text_braille(self, text):
        return self.trad_2_braille()

    def clear_panel(self, panel):
        for widget in panel.winfo_children():
            widget.destroy()

    def to_pdf_espejo(self):
        self.converter.generar_pdf_espejo()

    def to_img_normal(self):
        self.converter.convert_2_image()
    
    def start_recording(self):
        self.is_recording = True
        self.button_start_recording.configure(state='disabled')
        self.button_stop_recording.configure(state='normal')
        self.recording_thread = threading.Thread(target=self.record_audio)
        self.recording_thread.start()
        messagebox.showinfo("Grabación", "La grabación ha comenzado.")
    
    def stop_recording(self):
        self.is_recording = False
        self.button_start_recording.configure(state='normal')
        self.button_stop_recording.configure(state='disabled')
        self.recording_thread.join()
        self.process_recorded_audio()
        messagebox.showinfo("Grabación", "La grabación ha finalizado.")
    
    def record_audio(self):
        self.audio_filename = "temp_audio.wav"
        self.converter.recognizer.record_audio(self.audio_filename, duration=30)  # Ajusta la duración con 60 es muy lento
    
    def process_recorded_audio(self):
        transcribed_text = self.converter.recognizer.transcribe_audio(self.audio_filename)
        if transcribed_text:
            self.textBox_input.delete("1.0", 'end')
            self.textBox_input.insert("1.0", transcribed_text)
            self.trad_2_braille(None)
        else:
            messagebox.showwarning("Transcription", "No se pudo transcribir el audio.")

    def copy_braille(self):
        self.textBox_output.configure(state='normal')
        self.textBox_output.clipboard_clear()
        self.textBox_output.clipboard_append(self.textBox_output.get("1.0", 'end-1c'))
        self.textBox_output.configure(state='disabled')
        messagebox.showinfo("Copiar Braille", "El texto en Braille ha sido copiado.")
