# Utilidad para resolver problema con los path relativos
import os, sys

class UtilPath():
    def __init__(self):
        pass        

    def resource_path(self, relative_path):
        # Get absolute path to resource, works for dev and PyInstaller
        try:
            base_path = sys._MEIPASS2
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
    
    def get_font_path(self):
        ruta_fuente = self.resource_path("fonts\\ONCE_CBE_6.ttf")
        return ruta_fuente    