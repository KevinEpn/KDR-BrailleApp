# Main form class called main_form_design

import customtkinter as ctk
import util.util_ventana as util_vent
from util.util_config import FONT_ROBOTO_15, FONT_AWSOME_20, FONT_AWSOME_10

from forms.about_form_Design import AboutFormDesign
from forms.building_form_design import BuildingFormDesign
from forms.T2B_form_design import T2BFormDesign

# Set colores de la GUI
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("dark-blue")
class MainFormDesign(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.config_window()
        self.paneles()
        self.barra_sup_ctrl()
        self.menu_lat_ctrl()
        self.open_T2B()

    def config_window(self):
        #Configuracion inicial de la ventana
        w, h = 1024, 600
        self.title('Traductor de Braille')
        self.geometry(f'{w}x{h}')
        util_vent.centrar_ventana(self, w, h)


    def paneles(self):
        self.barra_sup = ctk.CTkFrame(self, height=60)
        self.barra_sup.pack(side = 'top', fill = 'both', expand = False)

        self.menu_lat = ctk.CTkFrame(self, width=150)
        self.menu_lat.pack(side = 'left', fill = 'both', expand = False)

        self.fondo = ctk.CTkFrame(self)
        self.fondo.pack(side = 'right', fill = 'both', expand = True)

    
    def barra_sup_ctrl(self):
        # Configuracion de la barra superior
        # Etiqueta de titulo
        self.labelTituloLeft = ctk.CTkLabel(
            self.barra_sup, text = "MENÚ"
        )
        self.labelTituloLeft.configure(
            font = FONT_AWSOME_20, pady = 10, padx = 25, width = 175
            )
        self.labelTituloLeft.pack(side = 'left')

        # Boton del menu principal
        self.menu_button = ctk.CTkButton(
            self.barra_sup, width = 30, text = "\uf0c9", font = FONT_ROBOTO_15,
            command = self.toggle_panel
        )
        self.menu_button.pack(side = 'left', pady = 10)

        # Etiqueta de informacion
        self.labelTituloRight = ctk.CTkLabel(
            self.barra_sup, text = "Version 1.0 - KDR"
        )
        self.labelTituloRight.configure(
            font = FONT_AWSOME_10, padx = 10, width = 25
            )
        self.labelTituloRight.pack(side = 'right')


    def menu_lat_ctrl(self):
        # Configuracion de la barra lateral
        ancho_menu = 30
        alto_menu = 2

        # Botones del menu lateral
        self.T2BButton = ctk.CTkButton(self.menu_lat)
        self.B2TButton = ctk.CTkButton(self.menu_lat)
        self.aboutButton = ctk.CTkButton(self.menu_lat)

        buttons_info = [
            ("T2B", self.T2BButton, "\uf2a1", self.open_T2B),
            ("B2T", self.B2TButton, "\uf031", self.open_build),
            ("About", self.aboutButton, "\uf05a", self.open_about)
        ]

        for text, button, icon, cm in buttons_info:
            self.menu_button_conf(button, text, icon, FONT_ROBOTO_15, ancho_menu, alto_menu, cm)
    

    def menu_button_conf(self, button, text, icon, font, ancho, alto, cm):
        button.configure(
            text = f"  {icon}\t{text}\t", anchor = "center", font = font, width = ancho, height = alto,
            command = cm
        )
        button.pack(side = 'top', padx = 15, pady = 5)

    def toggle_panel(self):
        # Cambiar el estado del panel lateral
        if self.menu_lat.winfo_ismapped():
            self.menu_lat.pack_forget()
            self.labelTituloLeft.pack_forget()
            self.menu_button.pack(padx = 10,  pady = 10)
        else:
            # self.menu_lat.pack(side = tk.LEFT, fill = tk.Y)
            self.menu_button.pack_forget()
            self.menu_lat.pack(side = 'left', fill = 'both', expand = False)
            self.labelTituloLeft.pack(side = 'left')
            self.menu_button.pack(side = 'left', pady = 10)


    # Funcionalides Botones
    def open_about(self):
        AboutFormDesign()

    def open_build(self):
        self.clear_panel(self.fondo)
        BuildingFormDesign(self.fondo)

    def open_T2B(self):
        self.clear_panel(self.fondo)
        T2BFormDesign(self.fondo)

    def clear_panel(self, panel):
        for widget in panel.winfo_children():
            widget.destroy()