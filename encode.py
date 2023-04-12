from RSA import *
import wave

audioCoverName = input("Enter the name of Cover Audio File: ")
coverAudio = wave.open(audioCoverName, mode='rb')
AudioInBytes = bytearray(coverAudio.readframes(coverAudio.getnframes()))

publicKey, privateKey = gen_key(p,q)

print("The Public Key is: ", publicKey)
print("The Private key is: ", privateKey)

message = input("Enter the message to hide: ")

secretMsg= str(encrypt(message, publicKey))

secretMsg = secretMsg + int((len(AudioInBytes)-(len(secretMsg)*8*8))/8) *'|'
bit_arr = list(map(int, ''.join(bin(ord(i)).lstrip('0b').rjust(8,'0') for i in secretMsg)))

for i, j in enumerate(bit_arr):
    AudioInBytes[i] = (AudioInBytes[i] & 254) | j

AudioAfterEncode = bytes(AudioInBytes)

print("Enter the name of the output file: ")
outputName = input()
with wave.open(outputName, mode='wb') as Done:
    Done.setparams(coverAudio.getparams())
    Done.writeframes(AudioAfterEncode)
coverAudio.close()