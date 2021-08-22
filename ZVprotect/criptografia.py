
class Criptografia(object):

    def criptografia(self, m, e, n):
        c = (m**e) % n
        return c

    def descriptografia(self, c, d, n):
        m = c**d % n
        return m

    def encripta_mensagem(self,s,e,n):
        enc = ''.join(chr(self.criptografia(ord(x), e, n)) for x in s)
        #print('Texto Cifrado: ', enc, '\n')
        return enc
        
        
    def decripta_mensagem(self,s,d,n):
        self.s = s
        dec = ''.join(chr(self.descriptografia(ord(x), d, n)) for x in s)
        return dec