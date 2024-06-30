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
        self.pos = []
        self.ruta_fuente = UtilPath().get_font_path()
        self.set_font()
        
        #ruta personal, se cuelga cuando se manda el modelo general
        model_path = r"C:\Users\johan\OneDrive\Escritorio\2024-A\CALIDAD DE SOFTWARE\PROYECTO pt2\vosk-model-small-es-0.42"
        self.recognizer = VoskRecognizer(model_path)

    def get_raw_brallie(self):
        return T2BCode().get_final_braille()
    
    def get_pos(self):
        return T2BCode().get_pos()

    # Generar archivo PDF espejo
    def generar_pdf_espejo(self):

        archivo = self.get_save_name('0')
        # self.pos = self.get_pos()
        self.raw_braille = self.get_raw_brallie()


        
        # Crear un objeto canvas para el documento PDF
        if archivo:
            nombre = archivo

            # Definir el tamaño de la página
            ancho, alto = letter

            # Inicializar el lienzo (canvas)
            c = canvas.Canvas(nombre, pagesize=letter)

            # Configurar la fuente personalizada
            c.setFont("Braille", 20)  

            
            # Configurar la impresión en modo espejo horizontalmente
            c.transform(-1, 0, 0, 1, letter[0], 0)
            text_object = c.beginText(40, letter[1] - 40)

            # Dividir el texto en líneas para que quepa en la página
            for linea in self.raw_braille.split('\n'):
                # Escribir el texto en el lienzo
                text_object.textLine(linea)
            c.drawText(text_object)
            c.showPage()

            # Guardar el PDF
            c.save()

            if c:
                self.succesful_save()

    def convert_2_image(self):        
        BACKGROUND_COLOR = "white"
        text_color = "black"

        # Filediallog para preguntar ruta para guardar la imagen
        archivo = self.get_save_name('1')
        self.raw_braille = self.get_raw_brallie()

        if archivo:
            nombre = archivo
            ancho, alto = letter            

            # Crear nueva imagen con el tama;o especificado y el color de fondo
            imagen = Image.new("RGB", (int(ancho), int(alto)), BACKGROUND_COLOR)

            # Crear un objeto ImageDraw para dibujar en la imagen
            draw = ImageDraw.Draw(imagen)

            # Definir la fuente y el tamaño del texto
            if self.ruta_fuente:
                fuente = ImageFont.truetype(self.ruta_fuente, 20)

                # Dividir el texto en líneas para que quepa en la imagen
                lineas = self.raw_braille.split('\n')

                # Definir la posición inicial para escribir el texto
                x_inicial = 30
                y_inicial = 50

                # Escribir el texto en la imagen
                for linea in lineas:
                    draw.text((x_inicial, y_inicial), linea, fill = text_color, font = fuente)
                    y_inicial += 20

                # Guardar imagen
                imagen.save(nombre)

                if imagen:
                    self.succesful_save()

    def set_font(self):
        # Registrar un TrueType font con la libreria ReportLab de pdfmetrics
        pdfmetrics.registerFont(TTFont('Braille', self.ruta_fuente))        

    def get_save_name(self, code):
        if code == '0':
            return filedialog.asksaveasfilename(
            defaultextension = ".*", title = "Save File", filetypes = (("PDF Files", "*.pdf"), ("All Files", "*.*"))
            )
        else:
            return filedialog.asksaveasfilename(
            defaultextension = ".*", title = "Save File", filetypes = (("PNG Files", "*.png"), ("All Files", "*.*"), )
        )
    
    def succesful_save(self):
        messagebox.showinfo("Success", "Archivo guardado con exito")
    
    def voice_to_braille(self):
        audio_filename = "temp_audio.wav"
        self.recognizer.record_audio(audio_filename, duration=5)  # Grabación de 5 segundos
        transcribed_text = self.recognizer.transcribe_audio(audio_filename)
        if transcribed_text:
            braille_text = T2BCode().texto_a_braile(transcribed_text)
            messagebox.showinfo("Transcription", f"Transcribed Text: {transcribed_text}\nBraille: {braille_text}")
        else:
            messagebox.showwarning("Transcription", "No se pudo transcribir el audio.")
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
        self.pos = []
        self.ruta_fuente = UtilPath().get_font_path()
        self.set_font()
        
        model_path = r"C:\Users\johan\OneDrive\Escritorio\2024-A\CALIDAD DE SOFTWARE\PROYECTO pt2\vosk-model-small-es-0.42"
        self.recognizer = VoskRecognizer(model_path)

    def get_raw_brallie(self):
        return T2BCode().get_final_braille()
    
    def get_pos(self):
        return T2BCode().get_pos()

    # Generar archivo PDF espejo
    def generar_pdf_espejo(self):

        archivo = self.get_save_name('0')
        # self.pos = self.get_pos()
        self.raw_braille = self.get_raw_brallie()


        
        # Crear un objeto canvas para el documento PDF
        if archivo:
            nombre = archivo

            # Definir el tamaño de la página
            ancho, alto = letter

            # Inicializar el lienzo (canvas)
            c = canvas.Canvas(nombre, pagesize=letter)

            # Configurar la fuente personalizada
            c.setFont("Braille", 20)  

            
            # Configurar la impresión en modo espejo horizontalmente
            c.transform(-1, 0, 0, 1, letter[0], 0)
            text_object = c.beginText(40, letter[1] - 40)

            # Dividir el texto en líneas para que quepa en la página
            for linea in self.raw_braille.split('\n'):
                # Escribir el texto en el lienzo
                text_object.textLine(linea)
            c.drawText(text_object)
            c.showPage()

            # Guardar el PDF
            c.save()

            if c:
                self.succesful_save()

    def convert_2_image(self):        
        BACKGROUND_COLOR = "white"
        text_color = "black"

        # Filediallog para preguntar ruta para guardar la imagen
        archivo = self.get_save_name('1')
        self.raw_braille = self.get_raw_brallie()

        if archivo:
            nombre = archivo
            ancho, alto = letter            

            # Crear nueva imagen con el tama;o especificado y el color de fondo
            imagen = Image.new("RGB", (int(ancho), int(alto)), BACKGROUND_COLOR)

            # Crear un objeto ImageDraw para dibujar en la imagen
            draw = ImageDraw.Draw(imagen)

            # Definir la fuente y el tamaño del texto
            if self.ruta_fuente:
                fuente = ImageFont.truetype(self.ruta_fuente, 20)

                # Dividir el texto en líneas para que quepa en la imagen
                lineas = self.raw_braille.split('\n')

                # Definir la posición inicial para escribir el texto
                x_inicial = 30
                y_inicial = 50

                # Escribir el texto en la imagen
                for linea in lineas:
                    draw.text((x_inicial, y_inicial), linea, fill = text_color, font = fuente)
                    y_inicial += 20

                # Guardar imagen
                imagen.save(nombre)

                if imagen:
                    self.succesful_save()

    def set_font(self):
        # Registrar un TrueType font con la libreria ReportLab de pdfmetrics
        pdfmetrics.registerFont(TTFont('Braille', self.ruta_fuente))        

    def get_save_name(self, code):
        if code == '0':
            return filedialog.asksaveasfilename(
            defaultextension = ".*", title = "Save File", filetypes = (("PDF Files", "*.pdf"), ("All Files", "*.*"))
            )
        else:
            return filedialog.asksaveasfilename(
            defaultextension = ".*", title = "Save File", filetypes = (("PNG Files", "*.png"), ("All Files", "*.*"), )
        )
    
    def succesful_save(self):
        messagebox.showinfo("Success", "Archivo guardado con exito")
    
    def voice_to_braille(self):
        audio_filename = "temp_audio.wav"
        self.recognizer.record_audio(audio_filename, duration=30)  
        transcribed_text = self.recognizer.transcribe_audio(audio_filename)
        if transcribed_text:
            braille_text = T2BCode().texto_a_braile(transcribed_text)
            messagebox.showinfo("Transcription", f"Transcribed Text: {transcribed_text}\nBraille: {braille_text}")
        else:
            messagebox.showwarning("Transcription", "No se pudo transcribir el audio.")
   