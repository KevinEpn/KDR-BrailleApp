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
        self.ruta_modelo = UtilPath().get_model_path()
        self.set_font()
        
        #ruta de personal, se cuelga cuando se manda el modelo general
        # model_path = r"C:\Users\johan\OneDrive\Escritorio\2024-A\CALIDAD DE SOFTWARE\PROYECTO pt2\vosk-model-small-es-0.42"
        # model_path = r"D:\EPN\#7 SEMESTRE\CALIDAD DE SOFTWARE\Proyecto Final\KDR-BrailleApp\Devs\models\vosk-model-small-es-0.42"
        # self.recognizer = VoskRecognizer(model_path)
        self.recognizer = VoskRecognizer(self.ruta_modelo)

    def get_raw_brallie(self):
        return T2BCode().get_final_braille()
    
    def get_pos(self):
        return T2BCode().get_pos()

    # Generar archivo PDF espejo
    def generar_pdf_espejo(self):

        archivo = self.get_save_name('0')
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

            lines = self.raw_braille.split('\n')
            # Dividir el texto en líneas para que quepa en la página
            print(lines)
            for linea in lines:
                # Calculo numero de paginas necesarias.
                wrapped_lines = self.wrap_text(linea, ancho - 70, c)
                for wrapped_line in wrapped_lines:
                    if text_object.getY() < 40:
                        c.drawText(text_object)
                        c.showPage()
                        c.setFont("Braille", 20)
                        c.transform(-1, 0, 0, 1, letter[0], 0)
                        text_object = c.beginText(40, letter[1] - 40)
                    # Escribir el texto en el lienzo
                    text_object.textLine(wrapped_line)
            c.drawText(text_object)
            c.showPage()

            # Guardar el PDF
            c.save()

            if c:
                self.succesful_save()

    def wrap_text(self,text, max_width, c):
        # Dividir el texto en líneas para que quepa en la página
        wrapped_lines = []
        words = text.split(' ')
        while words:
            linea = ""
            while words and c.stringWidth(linea + words[0], "Braille", 20) <= max_width:
                linea += words.pop(0) + " "
            wrapped_lines.append(linea)
        return wrapped_lines

    def convert_2_image(self):        
        BACKGROUND_COLOR = "white"
        text_color = "black"

        # Filediallog para preguntar ruta para guardar la imagen
        archivo = self.get_save_name('1')
        self.raw_braille = self.get_raw_brallie()

        if archivo:
            nombre = archivo.split('.png')
            print(nombre)
            
            ancho, alto = letter
            margen = 45            
            max_lines_per_image = 30

            # Crear nueva imagen con el tama;o especificado y el color de fondo
            imagen = Image.new("RGB", (int(ancho), int(alto)), BACKGROUND_COLOR)

            # Crear un objeto ImageDraw para dibujar en la imagen
            draw = ImageDraw.Draw(imagen)

            # Definir la fuente y el tamaño del texto
            if self.ruta_fuente:
                # fuente = ImageFont.truetype(self.ruta_fuente, 20)
                try:
                    fuente = ImageFont.truetype(self.ruta_fuente, 20)
                except IOError:
                    fuente = ImageFont.load_default()

                # Dividir el texto en líneas para que quepa en la imagen
                lineas = self.raw_braille.split('\n')

                # Definir la posición inicial para escribir el texto
                y_inicial = margen

                img_count = 1
                line_count = 0

                print(lineas)
                # Escribir el texto en la imagen
                for linea in lineas:
                    # draw.text((x_inicial, y_inicial), linea, fill = text_color, font = fuente)
                    # y_inicial += 20
                    wrapped_lines = self.split_text_to_fit_line(linea, int(ancho) - 2 * margen, draw, fuente)
                    for wrapped_line in wrapped_lines:
                        if line_count >= max_lines_per_image:  # Si se excede el número máximo de líneas por imagen
                            # Guardar la imagen actual y crear una nueva
                            imagen.save(f"{nombre[0]}_parte_{img_count}.png")
                            img_count += 1
                            line_count = 0
                            y_inicial = margen
                            imagen = Image.new('RGB', (int(ancho), int(alto)), color=(255, 255, 255))
                            draw = ImageDraw.Draw(imagen)

                        draw.text((margen, y_inicial), wrapped_line, font=fuente, fill=(0, 0, 0))
                        y_inicial += 23
                        line_count += 1
                    

                # Guardar la última imagen si hay alguna línea dibujada
                if line_count > 0:
                    imagen.save(f"{nombre[0]}_parte_{img_count}.png")

                if imagen:
                    self.succesful_save()


    def split_text_to_fit_line(self, text, max_width, draw, font):
    # Divide el texto en varias líneas si es más ancho que max_width.
        lines = []
        words = text.split(' ')
        print('palabras')
        print(words)
        current_line = ""
        is_first_word = True

        for word in words:
            if is_first_word and word == '':
                current_line = ' '
                is_first_word = False
                continue
            elif word == '':
                current_line += '\n'
            else:
                test_line = current_line + word if current_line else word
                width = draw.textlength(test_line, font=font)
                if width <= max_width:
                    current_line = test_line + ' '
                else:
                    lines.append(current_line)
                    current_line = word + ' ' 
            is_first_word = False
        if current_line:
            lines.append(current_line)
        return lines

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
        self.transcribed_text = self.recognizer.transcribe_audio()
        if self.transcribed_text:
            self.raw_braille = T2BCode().texto_a_braile(self.transcribed_text)
            messagebox.showinfo("Transcription", f"Transcribed Text: {self.transcribed_text}\nBraille: {self.raw_braille}")
        else:
            messagebox.showwarning("Transcription", "No se pudo transcribir el audio.")


    def get_transcribed_text(self):
        return self.transcribed_text
