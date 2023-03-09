import numpy as np
from scipy.io import wavfile
from stego import lsb
debug = True


# helper functions #######################################
def message_to_binary(message):
    binary_message = []
    for char in message:
        binary_message.append(format(ord(char), '08b'))
    return ''.join(binary_message)

def binary_to_message(binary_message):
    message = []
    for i in range(0, len(binary_message), 8):
        message.append(chr(int(binary_message[i:i+8], 2)))
    return ''.join(message)



# hide a text message in a wav file ########################
def hide_message(audio_file, message, output_file):
    if debug: print("hide_message entry") #DEBUG ONLY

    # Load the audio file
    rate, data = wavfile.read(audio_file)

    # Convert the message to binary format
    binary_message = message_to_binary(message)
    if debug: print(f"Binary message: {binary_message}") #DEBUG ONLY

    # Check if the message can fit in the audio file
    if len(binary_message) > len(data) * 8 - 32:
        print('Message is too long to be hidden in the audio file')
        return

    # Add the length of the message to the beginning of the binary message
    binary_length = format(len(message), '032b')
    if debug: print(f"Binary length: {binary_length}")
    binary_message = binary_length + binary_message
    if debug: print(f"Binary message: {binary_message}") #DEBUG ONLY

    # Convert the audio data to a 1D array
    audio_data = data.flatten()
    if debug: print(f"Audio data: {audio_data}") #DEBUG ONLY

    # Iterate through each bit of the binary message
    if debug: print(f"Iterate through each bit of the binary message: ") #DEBUG ONLY
    for i in range(len(binary_message)):
        # Convert the current bit to an integer value
        bit = int(binary_message[i])
        if debug: print(f"Current bit: {bit}")
        # Apply a bitwise AND operation on the current audio sample with the binary value 0xfe,
        # which is a bitmask that sets the least significant bit (LSB) of the audio sample to 0
        masked_sample = audio_data[i] & 0xfe
        if debug: print(f"Masked sample: {masked_sample}")
        # Apply a bitwise OR operation on the resulting value with the current bit of the binary message,
        # which effectively sets the LSB of the audio sample to the value of the bit in the binary message
        modified_sample = masked_sample | bit
        if debug: print(f"Modified sample: {modified_sample}")
        # Replace the original audio sample with the modified sample
        audio_data[i] = modified_sample
    # Reshape the audio data to its original shape
    audio_data = np.reshape(audio_data, data.shape)

    # Save the modified audio file
    wavfile.write(output_file, rate, audio_data)
    if debug: print("hide_message exit") #DEBUG ONLY


# reveal a text message in a wav stego file ########################
def extract_message(audio_file):
    if debug: print("Extracting message...") #DEBUG ONLY

    # Load the audio file
    rate, data = wavfile.read(audio_file)

    data = data.flatten()  # Convert to one-dimensional array

    # Extract message length from the first 32 bits of audio data
    # Extract message length from the first 32 bits of audio data
    message_length_bytes = data[:4]
    message_length = int.from_bytes(message_length_bytes, byteorder='big')
    if debug: print(f"Message length: {message_length}") #DEBUG ONLY


    # Extract the LSB of each audio sample after the first 32 bits
    binary_message = ''
    for i in range(4, 4 + message_length):
        sample = data[i]
        bit = sample & 1
        binary_message += str(bit)

    # Check the length of the extracted message
    expected_length = message_length * 8
    actual_length = len(binary_message)
    if actual_length != expected_length:
        print(f"Error: expected message length of {message_length} bytes, but found {actual_length//8} bytes in stego file")
        return None

    # Convert binary message to ASCII string
    message = ''
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        message += chr(int(byte, 2))

    return message


def main():
    choice = input("Enter 'e' to encode a message or 'd' to decode a message: ")
    if choice == 'e':
        audio_file = "./test.wav" #input("Enter the path to the audio file: ")
        message = "flag{aud10}" #input("Enter the message to be hidden: ")
        output_file = "./stego.wav"  #input("Enter the path to save the output audio file: ")
        hide_message(audio_file, message, output_file)
        print("Message hidden successfully")
    elif choice == 'd':
        audio_file = "./stego.wav" #input("Enter the path to the audio file: ")
        message = extract_message(audio_file)
        print("The hidden message is:", message)
    else:
        print("Invalid choice")

if __name__ == '__main__':
    main()
