# T2B code and logical structure

# braille = ''
class T2BCode():

    global final_braille
    final_braille = ''

    global pos

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
        '/':'⠸⠌','@':'⠈⠁','$':'⠈⠎','&':'⠈⠯', '*': '⠔', '⠀':'⠀'
        #' ': ' ',  # Agregar el espacio al diccionario para que sea tratado correctamente
    }

    # def __init__(self):
    #     self.braille = ''
        # self.new_text = text
        # self.texto_a_braile(self.new_text)


    def obtener_texto(self, texto):
        i = 0
        j = 0
    #     # Dividir la cadena en palabras
        palabras = []
    
        while i < len(texto):
            
            if texto[i] == '*':
                palabras.append(i)
                j = -1
            j += 1
            i += 1

        print(palabras)
        
        global pos
        pos = palabras
        

    #     # Imprimir la lista de palabras
    #     print("Lista de palabras:")
    #     print(palabras)

    #     resultados = [] # 0 para numeros, 1 para caracteres
    #     for palabra in palabras:
    #         if palabra.isdigit():
    #             # resultados.append((palabra, 0))
    #             resultados.append((0))
    #         else:
    #             resultados.append((1))

    #     print(resultados)
    #     return resultados
    
    def texto_a_braile(self, raw_texto):
        # palabras_array = self.obtener_texto(texto)
        # self.obtener_texto(raw_texto)
        texto = raw_texto
        

        # global braille
        # braille = '⠀'    

        # for palabra, tipo in palabras_array:
        #     if tipo == 0:
        #         braille += ' ⠼'

        #     for caracter in palabra:
        #         if caracter.lower() in mapeo_braille:  # Si el caracter está en el diccionario, añadir su representación en braille
        #             if caracter.isupper():  # Si es mayúscula, añadir el símbolo de mayúscula en braille
        #                 braille += '⠨'
        #             braille += mapeo_braille[caracter.lower()]  # Convertimos el caracter a braille y lo añadimos al resultado
        #         else:
        #             braille += ' '  # Si el caracter no está en el diccionario, lo reemplazamos con un espacio en blanco
        #     braille += '⠀' # Añadir espacio entre palabras en braille
        #     print(braille)
        

        # global braille
        texto = texto.replace('\t', '⠀' * 4)
        # texto = texto.replace('⠀' * 4, '\t')
        braille = ''    

        i = 0
        while i < len(texto):
            char = texto[i]
            if char.isupper():
                braille += '⠨' + mapeo_braille.get(char.lower(), char)
            elif char.isdigit():
                braille += '⠼'
                while i < len(texto) and texto[i].isdigit():
                    braille += mapeo_braille.get(texto[i], texto[i])
                    i += 1
                continue
            else:
                braille += mapeo_braille.get(char, char)
            # elif char in ['\n']:
            #     braille += mapeo_braille.get(char, char)
            # else:
            #     braille += mapeo_braille.get(char, ' ')

            i += 1
        # self.braille = braille
        # print(self.braille)
        global final_braille
        final_braille = braille
        return braille
        

    def get_final_braille(self):
        print("Final braille")
        # final_braille = final_braille.replace('⠀' * 8, '\t')
        print(final_braille)
        return final_braille
    
    def set_final_braille(self):
        # global braille
        # braille = ''
        self.braille = ''

    def get_pos(self):
        return pos