# Convert to PDF code and logical structure
import os
from tkinter import filedialog, messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image, ImageDraw, ImageFont

from src.T2B_code import T2BCode
from util.util_path import UtilPath
from src.vosk_recognition import VoskRecognizer

class ConvertTo():

    def __init__(self):
        print("convert")
        self.raw_braille = ''
        self.ruta_fuente = UtilPath().get_font_path()
        self.ruta_modelo = UtilPath().get_model_path()
        self.set_font()
        self.recognizer = VoskRecognizer(self.ruta_modelo)

    def get_raw_braille(self):
        return T2BCode().get_final_braille()

    def generar_pdf_espejo(self):
        archivo = self.get_save_name('0')
        if not archivo:
            return

        self.raw_braille = self.get_raw_braille()
        c = self.initialize_canvas(archivo)
        if not c:
            return

        self.draw_text_on_pdf(c)
        c.save()
        self.succesful_save()

    def initialize_canvas(self, archivo):
        ancho, _ = letter
        c = canvas.Canvas(archivo, pagesize=letter)
        c.setFont("Braille", 20)
        c.transform(-1, 0, 0, 1, ancho, 0)
        return c

    def draw_text_on_pdf(self, c):
        text_object = c.beginText(40, letter[1] - 40)
        for wrapped_line in self.wrap_text_to_fit_page():
            if text_object.getY() < 40:
                c.drawText(text_object)
                c.showPage()
                text_object = self.initialize_page(c)
            text_object.textLine(wrapped_line)
        c.drawText(text_object)

    def initialize_page(self, c):
        c.setFont("Braille", 20)
        c.transform(-1, 0, 0, 1, letter[0], 0)
        return c.beginText(40, letter[1] - 40)

    def wrap_text_to_fit_page(self):
        ancho, _ = letter
        lines = self.raw_braille.split('\n')
        wrapped_lines = []
        for line in lines:
            wrapped_lines.extend(self.wrap_text(line, ancho - 70))
        return wrapped_lines

    def wrap_text(self, text, max_width):
        wrapped_lines = []
        words = text.split(' ')
        current_line = ""

        for word in words:
            test_line = current_line + word if current_line else word
            if self.text_fits(test_line, max_width):
                current_line = test_line + ' '
            else:
                wrapped_lines.append(current_line)
                current_line = word + ' '

        if current_line:
            wrapped_lines.append(current_line)
        return wrapped_lines

    def text_fits(self, text, max_width):
        c = canvas.Canvas(None, pagesize=letter)
        return c.stringWidth(text, "Braille", 20) <= max_width

    def convert_2_image(self):
        archivo = self.get_save_name('1')
        if not archivo:
            return

        self.raw_braille = self.get_raw_braille()
        nombre = archivo.split('.png')[0]
        self.create_images_from_text(nombre)
        self.succesful_save()

    def create_images_from_text(self, nombre):
        ancho, alto = letter
        margen = 45
        max_lines_per_image = 30

        lines = self.raw_braille.split('\n')
        img_count, line_count = 1, 0
        y_inicial = margen

        imagen, draw, fuente = self.initialize_image(ancho, alto, margen)

        for line in lines:
            wrapped_lines = self.split_text_to_fit_line(line, ancho - 2 * margen, draw, fuente)
            for wrapped_line in wrapped_lines:
                if line_count >= max_lines_per_image:
                    self.save_image(imagen, nombre, img_count)
                    img_count += 1
                    line_count, y_inicial = 0, margen
                    imagen, draw, fuente = self.initialize_image(ancho, alto, margen)
                draw.text((margen, y_inicial), wrapped_line, font=fuente, fill=(0, 0, 0))
                y_inicial += 23
                line_count += 1

        if line_count > 0:
            self.save_image(imagen, nombre, img_count)

    def initialize_image(self, ancho, alto, margen):
        imagen = Image.new("RGB", (int(ancho), int(alto)), "white")
        draw = ImageDraw.Draw(imagen)
        fuente = self.get_font()
        return imagen, draw, fuente

    def save_image(self, imagen, nombre, img_count):
        imagen.save(f"{nombre}_parte_{img_count}.png")

    def get_font(self):
        try:
            return ImageFont.truetype(self.ruta_fuente, 20)
        except IOError:
            return ImageFont.load_default()

    def split_text_to_fit_line(self, text, max_width, draw, font):
        lines = []
        words = text.split(' ')
        current_line = ""

        for word in words:
            if word == '':
                current_line += '\n'
            else:
                test_line = current_line + word if current_line else word
                if draw.textlength(test_line, font=font) <= max_width:
                    current_line = test_line + ' '
                else:
                    lines.append(current_line)
                    current_line = word + ' '

        if current_line:
            lines.append(current_line)
        return lines

    def set_font(self):
        pdfmetrics.registerFont(TTFont('Braille', self.ruta_fuente))

    def get_save_name(self, code):
        if code == '0':
            return filedialog.asksaveasfilename(
                defaultextension=".*", title="Save File", filetypes=(("PDF Files", "*.pdf"), ("All Files", "*.*"))
            )
        else:
            return filedialog.asksaveasfilename(
                defaultextension=".*", title="Save File", filetypes=(("PNG Files", "*.png"), ("All Files", "*.*"))
            )

    def succesful_save(self):
        messagebox.showinfo("Success", "Archivo guardado con éxito")

    def voice_to_braille(self):
        self.transcribed_text = self.recognizer.transcribe_audio()
        if self.transcribed_text:
            self.raw_braille = T2BCode().texto_a_braille(self.transcribed_text)
            messagebox.showinfo("Transcription", f"Transcribed Text: {self.transcribed_text}\nBraille: {self.raw_braille}")
        else:
            messagebox.showwarning("Transcription", "No se pudo transcribir el audio.")

    def get_transcribed_text(self):
        return self.transcribed_text
