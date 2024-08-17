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
        ',': '⠂', '.': '⠄', ';': '⠆', ': ':'⠒', '-': '⠤',
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
            print(f"Braille generado y almacenado: {self.final_braille}")
            return braille

    def get_final_braille(self):
            if not self.final_braille:
                print("Braille no ha sido generado, llamando a texto_a_braile()")
                self.texto_a_braile("Texto de prueba")  # Cambia "Texto de prueba" por el texto que necesitas convertir
            return self.final_braille

    def set_final_braille(self, braille_text):
            self.final_braille = braille_text

    def get_pos(self):
            return self.pos
