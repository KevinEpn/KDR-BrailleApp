# Building form design

import tkinter as tk
from tkinter import font, messagebox
import customtkinter as ctk
from customtkinter import CTkFont
from util.util_config import FONT_AWSOME_20, FONT_ROBOTO_15, FONT_ARIAL_15, FG_TEXTBOX
from src.T2B_code import T2BCode
from src.convertTo import ConvertTo
from src.audio_recorder import AudioRecorder
import threading

class B2TformDesign():
    def __init__(self, main_panel):
        self.traslator = T2BCode()
        self.converter = ConvertTo()
        self.recorder = AudioRecorder()
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
        ancho = 20
        alto = 1

        self.label_output = ctk.CTkLabel(self.top_frame, text="Texto en Braille", font=FONT_AWSOME_20)
        self.label_output.pack(pady=5, side='top', fill='both', expand=False)

        self.textBox_output = ctk.CTkTextbox(
            self.top_frame, font=FONT_ARIAL_15, fg_color=FG_TEXTBOX, wrap='word', state='disabled'
        )
        self.textBox_output.pack(padx=100, pady=5, side='top', fill='both', expand=True)
        self.desabilitar_eventos_textbox(self.textBox_output)

    def create_center_widgets(self):
        self.label_input = ctk.CTkLabel(self.center_frame, text="Texto en Español", font=FONT_AWSOME_20)
        self.label_input.pack(pady=5, side='top', fill='both', expand=False)

        self.textBox_input = ctk.CTkTextbox(
            self.center_frame, font=FONT_ARIAL_15, fg_color=FG_TEXTBOX, wrap='word', state='disabled'
        )
        self.textBox_input.pack(padx=100, pady=5, side='top', fill='both', expand=True)
        self.desabilitar_eventos_textbox(self.textBox_input)

    def desabilitar_eventos_textbox(self, textbox):
        for event in ["<Button-1>", "<B1-Motion>", "<Double-1>", "<Triple-1>",
                      "<ButtonRelease-1>", "<Button-2>", "<B2-Motion>", "<Double-2>", "<Triple-2>",
                      "<ButtonRelease-2>", "<Button-3>", "<B3-Motion>", "<Double-3>", "<Triple-3>",
                      "<ButtonRelease-3>", "<Motion>", "<Enter>", "<Leave>", "<MouseWheel>", "<Button-4>",
                      "<Button-5>", "<Shift-Button-1>", "<Shift-B1-Motion>", "<Control-Button-1>",
                      "<Control-B1-Motion>", "<Shift-ButtonRelease-1>", "<Control-ButtonRelease-1>",
                      "<Control-Shift-Button-1>", "<Control-Shift-B1-Motion>"]:
            textbox.bind(event, self.disable_event)

        for event in ["<Key>", "<Control-Key>", "<Shift-Key>", "<Alt-Key>", "<Meta-Key>", "<KeyPress>", "<KeyRelease>"]:
            textbox.bind(event, self.disable_event)

    def disable_event(self, event):
        return "break"

    def create_bottom_widgets(self):
        self.button_clear_box = ctk.CTkButton(self.bottom_frame)
        self.button_img = ctk.CTkButton(self.bottom_frame)
        self.button_espejo = ctk.CTkButton(self.bottom_frame)
        self.button_start_recording = ctk.CTkButton(self.bottom_frame, command=self.start_recording)
        self.button_stop_recording = ctk.CTkButton(self.bottom_frame, command=self.stop_recording, state='disabled')
        self.button_copy_braille = ctk.CTkButton(self.bottom_frame, text="Copiar Braille", command=self.copy_braille)

        buttons_info = [
            ("Limpiar", self.button_clear_box, "\uf00d", self.clear_textbox),
            ("Por Voz", self.button_start_recording, "\uf130", self.start_recording),
            ("Detener Grabación", self.button_stop_recording, "\uf04d", self.stop_recording),
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

    def clear_textbox(self):
        self.textBox_input.configure(state='normal')
        self.textBox_output.configure(state='normal')
        self.textBox_input.delete("1.0", 'end')
        self.textBox_output.delete("1.0", 'end')
        self.textBox_input.configure(state='disabled')
        self.textBox_output.configure(state='disabled')
        self.traslator.set_final_braille()

    def start_recording(self):
        self.button_start_recording.configure(state='disabled')
        self.button_stop_recording.configure(state='normal')
        self.recorder.stop_event.clear()
        self.recorder.record_audio()

    def stop_recording(self):
        self.button_start_recording.configure(state='normal')
        self.button_stop_recording.configure(state='disabled')
        self.recorder.stop_recording()
        self.converter.voice_to_braille()
        self.process_recorded_audio()

    def process_recorded_audio(self):
        transcribed_text = self.converter.get_transcribed_text()
        if transcribed_text:
            self.textBox_input.configure(state='normal')
            self.textBox_input.delete("1.0", 'end')
            self.textBox_input.insert("1.0", transcribed_text)
            self.textBox_input.configure(state='disabled')
            self.trad_2_braille(None)
        else:
            messagebox.showwarning("Transcription", "No se pudo transcribir el audio.")

    def trad_2_braille(self, event):
        new_text = self.get_text()
        final_text = self.traslator.texto_a_braile(new_text)
        self.textBox_output.configure(state='normal')
        self.textBox_output.delete("1.0", 'end-1c')
        self.textBox_output.insert("1.0", final_text)
        self.textBox_output.configure(state='disabled')
        self.textBox_input.edit_modified(False)

    def get_text(self):
        return self.textBox_input.get("1.0", 'end-1c')

    def copy_braille(self):
        self.textBox_output.configure(state='normal')
        self.textBox_output.clipboard_clear()
        self.textBox_output.clipboard_append(self.textBox_output.get("1.0", 'end-1c'))
        self.textBox_output.configure(state='disabled')
        messagebox.showinfo("Copiar Braille", "El texto en Braille ha sido copiado.")


    def clear_panel(self, panel):
        for widget in panel.winfo_children():
            widget.destroy()
