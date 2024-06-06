# T2B code and logical structure

braille = ''
class T2BCode():

    def __init__(self, text):
        self.new_text = text
        self.texto_a_braile(self.new_text)

    # Definir un diccionario de mapeo de caracteres a braille
    global mapeo_braille
    mapeo_braille = {
        'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑',
        'f': '⠋', 'g': '⠛', 'h': '⠓', 'i': '⠊', 'j': '⠚',
        'k': '⠅', 'l': '⠇', 'm': '⠍', 'n': '⠝', 'o': '⠕',
        'p': '⠏', 'q': '⠟', 'r': '⠗', 's': '⠎', 't': '⠞',
        'u': '⠥', 'v': '⠧', 'w': '⠺', 'x': '⠭', 'y': '⠽',
        'z': '⠵', 'á': '⠷', 'é': '⠮', 'í': '⠌', 'ó': '⠬',
        'ú': '⠾', 'ü': '⠳', 'ñ': '⠻',
        '0': '⠚', '1': '⠁', '2': '⠃', '3': '⠉', '4': '⠙',
        '5': '⠑', '6': '⠋', '7': '⠛', '8': '⠓', '9': '⠊',
        '¿': '⠢', '?': '⠢', '¡': '⠖', '!': '⠖',
        ',': '⠂', '.': '⠄', ';': '⠆', ':': '⠒', '-': '⠤',
        '"': '⠦', "'": '⠠⠦', '(': '⠣', ')': '⠜', '#':'⠼',
        '/':'⠌','@':'⠈⠁','$':'⠈⠎','&':'⠯'
        #' ': ' ',  # Agregar el espacio al diccionario para que sea tratado correctamente
    }



    def obtener_texto(self, texto):
        # Dividir la cadena en palabras
        palabras = texto.split()

        # Imprimir la lista de palabras
        print("Lista de palabras:")
        print(palabras)

        resultados = [] # 0 para numeros, 1 para caracteres
        for palabra in palabras:
            if palabra.isdigit():
                resultados.append((palabra, 0))
            else:
                resultados.append((palabra, 1))

        print(resultados)
        return resultados
    
    def texto_a_braile(self, texto):
        palabras_array = self.obtener_texto(texto)

        global braille
        braille = '⠀'    

        for palabra, tipo in palabras_array:
            if tipo == 0:
                braille += ' ⠼'

            for caracter in palabra:
                if caracter.lower() in mapeo_braille:  # Si el caracter está en el diccionario, añadir su representación en braille
                    if caracter.isupper():  # Si es mayúscula, añadir el símbolo de mayúscula en braille
                        braille += '⠨'
                    braille += mapeo_braille[caracter.lower()]  # Convertimos el caracter a braille y lo añadimos al resultado
                else:
                    braille += ' '  # Si el caracter no está en el diccionario, lo reemplazamos con un espacio en blanco
            braille += '⠀' # Añadir espacio entre palabras en braille
            print(braille)
        

    def get_final_braille():
        return braille
    
    def set_final_braille():
        global braille
        braille = ''