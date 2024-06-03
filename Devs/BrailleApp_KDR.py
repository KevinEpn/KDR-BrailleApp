# Main class called BrailleApp-KDR
from Forms.main_form_design import MainFormDesign

class BrailleApp_KDR():
    def __init__(self):
        self.main()

    def main():
        app = MainFormDesign()
        app.mainloop()

    if __name__ == "__main__":
        main()
