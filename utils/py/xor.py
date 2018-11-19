class XorCipher:
    """ Class to create plaintext to Ciphertext and viceversa"""
    def __init__(self, plaintext_ciphertext, key):
        self.input_text=plaintext_ciphertext
        self.key=key
        self.output_text=self.__xor()

    def __xor(self):
        return ''.join([str(int(self.input_text[i]) ^ int(self.key[i])) for i in range(len(self.key))])

    def get8bitchunks(self, s):
        outlist=[]
        s=''
        count=0
        for i in self.output_text:
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



if __name__=="__main__":
    Xor = XorCipher('101010010100011011100001', '111110110000111110110101')
    print(Xor.bit2string(Xor.output_text))

    # swapping key and plaintext as the inputs
    Xor2 = XorCipher('111110110000111110110101', '101010010100011011100001')
    print(Xor2.bit2string(Xor.output_text))
