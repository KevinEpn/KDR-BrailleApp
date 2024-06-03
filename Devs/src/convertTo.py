# Convert to PDF code and logical structure

from tkinter import filedialog, messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image, ImageDraw, ImageFont

from src.T2B_code import T2BCode
from util.util_path import UtilPath

class ConvertTo():

    def __init__(self):
        print("convert")
        self.raw_braille = T2BCode.get_final_braille()
        self.ruta_fuente = UtilPath().get_font_path()
        self.set_font()

    # Generar archivo PDF espejo
    def generar_pdf_espejo(self):

        archivo = self.get_save_name('0')
        
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
            c.scale(-1, 1)  # Invertir horizontalmente

            # Dividir el texto en líneas para que quepa en la página
            lineas = [self.raw_braille[i:i+35] for i in range(0, len(self.raw_braille), 35)]

            # Definir la posición inicial para escribir el texto
            x_inicial = -ancho + 50
            y_inicial = alto - 50

            # Escribir el texto en el lienzo
            for linea in lineas:
                c.drawString(x_inicial, y_inicial, linea)
                y_inicial -= 20 * 2   # Ajustar la posición vertical para la siguiente línea

            # Guardar el PDF
            c.save()

            if c:
                self.succesful_save()

    def convert_2_image(self):        
        BACKGROUND_COLOR = "white"
        text_color = "black"

        # Filediallog para preguntar ruta para guardar la imagen
        archivo = self.get_save_name('1')

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
                lineas = [self.raw_braille[i:i+35] for i in range(0, len(self.raw_braille), 35)]

                # Definir la posición inicial para escribir el texto
                x_inicial = 30
                y_inicial = 50

                # Escribir el texto en la imagen
                for linea in lineas:
                    draw.text((x_inicial, y_inicial), linea, fill = text_color, font = fuente)
                    y_inicial += 20 * 2

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