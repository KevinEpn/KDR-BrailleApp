# Main class called BrailleApp-KDR
from forms.main_form_design import MainFormDesign
from util.util_path import UtilPath

class BrailleApp_KDR():
    def __init__(self):
        self.main()

    def main():
        ruta_icon = UtilPath().get_icon_path()
        app = MainFormDesign()
        app.iconbitmap(ruta_icon)
        app.mainloop()
        

    if __name__ == "__main__":
        main()
