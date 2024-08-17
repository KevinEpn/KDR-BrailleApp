# T2B code and logical structure

# braille = ''
class T2BCode:

    final_braille = ''
    pos = []

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
        ',': '⠂', '.': '⠄', ';': '⠆', ':':'⠒', '-': '⠤',
        '"': '⠦', "'": '⠠⠦', '(': '⠣', ')': '⠜', '#':'⠼', 
        '/':'⠸⠌', '@':'⠈⠁', '$':'⠈⠎', '&':'⠈⠯', '*': '⠔', 
        '+':'⠋', '=':'⠶', '%':'⠫', '<': '⠨⠮', '>':'⠨⠮', 
        '^':'⠨', '_':'⠤', '-':'⠤', '⠀':'⠀'
    }

    def obtener_texto(self, texto):
        palabras = []
        for i, char in enumerate(texto):
            if char == '*':
                palabras.append(i)
        self.pos = palabras

    def texto_a_braile(self, raw_texto):
        texto = raw_texto.replace('\t', '⠀' * 4)
        braille = ''    

        i = 0
        while i < len(texto):
            char = texto[i]
            if char.isupper():
                braille += '⠨' + self.mapeo_braille.get(char.lower(), char)
            elif char.isdigit():
                braille += '⠼'
                while i < len(texto) and texto[i].isdigit():
                    braille += self.mapeo_braille.get(texto[i], texto[i])
                    i += 1
                continue
            else:
                braille += self.mapeo_braille.get(char, char)
            i += 1
    
        self.final_braille = braille
        return braille

    def get_final_braille(self):
        print("Final braille")
        print(self.final_braille)
        return self.final_braille
    
    def set_final_braille(self):
        self.final_braille = ''

    def get_pos(self):
        return self.pos
