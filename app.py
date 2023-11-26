
import streamlit as st
from RSA import encrypt, decrypt, gen_key,p,q
from extract import converter
import wave

# Function to generate RSA keys and store them in session state
def generate_keys(p, q):
    if 'public_key' not in st.session_state:
        public_key, private_key = gen_key(p, q)
        st.session_state.public_key = public_key
        st.session_state.private_key = private_key
    else:
        public_key = st.session_state.public_key
        private_key = st.session_state.private_key
    return public_key, private_key

def encoder(audioCoverName, message, p, q):
    coverAudio = wave.open(audioCoverName, mode='rb')
    AudioInBytes = bytearray(coverAudio.readframes(coverAudio.getnframes()))

    public_key, private_key = generate_keys(p, q)
    st.write("The Public Key is:", public_key)
    st.write("The Private Key is:", private_key)

    secretMsg = str(encrypt(message, public_key))

    secretMsg = secretMsg + int((len(AudioInBytes) - (len(secretMsg) * 8 * 8)) / 8) * '|'
    bit_arr = list(map(int, ''.join(bin(ord(i)).lstrip('0b').rjust(8, '0') for i in secretMsg)))

    for i, j in enumerate(bit_arr):
        AudioInBytes[i] = (AudioInBytes[i] & 254) | j

    AudioAfterEncode = bytes(AudioInBytes)

    outputName = st.text_input("Enter the name of the output file:")

    if st.button("Encode"):
        with wave.open(outputName, mode='wb') as Done:
            Done.setparams(coverAudio.getparams())
            Done.writeframes(AudioAfterEncode)
        coverAudio.close()
        st.success("Message successfully encoded!")

def decoder(AudioModified, p, q):
    AudioFile = wave.open(AudioModified, mode='rb')
    AudioInBytes = bytearray(AudioFile.readframes(AudioFile.getnframes()))

    extracted = [AudioInBytes[i] & 1 for i in range(len(AudioInBytes))]
    rough = "".join(chr(int("".join(map(str, extracted[i:i+8])), 2)) for i in range(0, len(extracted), 8))

    secretMessageEncrypted = rough.split("|")[0]
    AudioFile.close()

    # Use a form to input private keys
    form = st.form(key='decoder_form')
    PrivateKey1 = form.text_input("Enter the private key (part 1):", value="0")
    PrivateKey2 = form.text_input("Enter the private key (part 2):", value="0")
    decode_button = form.form_submit_button("Decode")

    # Separate decoding logic
    if decode_button:
        try:
            PrivateKey1 = int(PrivateKey1)
            PrivateKey2 = int(PrivateKey2)

            cipher = converter(secretMessageEncrypted)
            result = decrypt(cipher, PrivateKey1, PrivateKey2)
            st.success(f"The hidden message is: {result}")
        except ValueError:
            st.error("Please enter valid integers for private keys.")
        except Exception as e:
            st.error(f"Error during decoding: {e}")

def main():
    st.title("Audio Steganography with RSA Encryption🚀🚀🚀")

    st.sidebar.subheader("Encoding")
    audioCoverName = st.sidebar.file_uploader("Upload Audio File (WAV)", type=["wav"])
    message = st.sidebar.text_area("Enter Message to Hide")

    if audioCoverName and message:
        encoder(audioCoverName, message, p, q)

    st.sidebar.subheader("Decoding")
    AudioModified = st.sidebar.file_uploader("Upload Encoded Audio File (WAV)", type=["wav"])

    if AudioModified:
        decoder(AudioModified, p, q)

if __name__ == "__main__":
    # p = 12345
    # q = 67890
    main()
