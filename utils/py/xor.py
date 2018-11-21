class XorCipher:
    """ Class to create plaintext to Ciphertext and viceversa"""
    def __init__(self, plaintext_ciphertext, key):
        #TODO: move try except to new method
        try:
            int_of_plain_txt=int(plaintext_ciphertext, 2)
        except Exception as e:
            print(e)
            # incoming text is not binary
            plaintext_ciphertext=self.string2bits(plaintext_ciphertext)

        try:
            int_of_plain_txt=int(key, 2)
        except Exception as e:
            print(e)
            # incoming text is not binary
            key=self.string2bits(key)

        self.input_text=plaintext_ciphertext
        self.key=key
        self.output_text=self.__xor()

    def __xor(self):
        return ''.join([str(int(self.input_text[i]) ^ int(self.key[i])) for i in range(len(self.key))])

    def get8bitchunks(self, in_str):
        outlist=[]
        s=''
        count=0
        for i in in_str:
            s=s+i
            count+=1
            if count==8:
                outlist.append(s)
                s=''
                count=0
        return ' '.join(outlist)

    def bit2string(self, bitstring):
        # get the 8 bit chunks from continous stream of bits
        outlist=self.get8bitchunks(bitstring)
        outlist=outlist.split()
        outchars=''
        for item in outlist:
            outchars=outchars + chr(int(item, 2))
        return outchars

    def string2bits(self, in_str):
        """ convert chars to binary and get 8 bit chunks"""
        bitstring=''.join([str(bin(ord(s))[2:].zfill(8)) for s in in_str])
        return bitstring


if __name__=="__main__":
    Xor = XorCipher('101010010100011011100001', '111110110000111110110101')
    print(Xor.bit2string(Xor.output_text))

    # swapping key and plaintext as the inputs
    Xor2 = XorCipher('111110110000111110110101', '101010010100011011100001')
    print(Xor2.bit2string(Xor.output_text))
    print(Xor2.bit2string('111110110000111110110101'))
    print(Xor2.bit2string('101010010100011011100001'))

    Xor3 = XorCipher('RIT', '©Fá')
    print('cipher text in ascii ', Xor3.bit2string(Xor3.output_text))

