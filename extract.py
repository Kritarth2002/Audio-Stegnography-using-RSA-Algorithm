import wave
from RSA import decrypt

def converter(msg):
        l = len(msg)
        c=[]
        tp=''
        for i in range(l):
                if(msg[i]=='['):
                        continue
                elif(msg[i]==']'):
                        d=int(tp)
                        c.append(d)
                        tp=''
                        break
                elif(msg[i].isdigit() == True):
                        tp = tp+msg[i]
                elif(msg[i]==','):
                        d=int(tp)
                        c.append(d)
                        tp=''        
        return c

# AudioModified = input("Enter the name of the audio you want to decode: ")

# AudioFile = wave.open(AudioModified, mode='rb')
# AudioInBytes = bytearray(AudioFile.readframes(AudioFile.getnframes()))

# extracted = [AudioInBytes[i] & 1 for i in range(len(AudioInBytes))]
# rough = "".join(chr(int("".join(map(str,extracted[i:i+8])),2)) for i in range(0,len(extracted),8))

# secretMessageEncrypted = rough.split("|")[0]
# AudioFile.close()

# PrivateKey1 = int(input("Enter the private key(part 1): "))
# PrivateKey2 = int(input("Enter the private key(part 2): "))

# cipher = converter(secretMessageEncrypted)
# print("The hidden message is: " + decrypt(cipher,PrivateKey1,PrivateKey2))
