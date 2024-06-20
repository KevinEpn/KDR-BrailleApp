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
    
    def texto_a_braile(self, raw_texto):
        # palabras_array = self.obtener_texto(texto)
        # self.obtener_texto(raw_texto)
        texto = raw_texto
                

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

            i += 1
    
        global final_braille
        final_braille = braille
        return braille
        

    def get_final_braille(self):
        print("Final braille")
        # final_braille = final_braille.replace('⠀' * 8, '\t')
        print(final_braille)
        return final_braille
    
    def set_final_braille(self):
        
        self.braille = ''

    def get_pos(self):
        return pos