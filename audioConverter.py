from scipy.io import wavfile
import numpy as np

#read from the file
#add the ability to see file type
#input filename

# Message Encoding
def encode_message(audio_file, output_file_name, message, is_binary, file_type, input_file):
    # Load the audio file
    rate, data = wavfile.read(audio_file)

    # Convert the message to binary if text or read the binary from a file
    if (is_binary):
        with open(input_file, 'rb') as file:
            binary_data = file.read()

            # Convert the bytes->integer->bits
            binary_representation = bin(int.from_bytes(binary_data, byteorder='big'))
            binary_message = binary_representation[2:] # Get rid of '0b' in the front
    else:
        binary_message = ''.join(format(ord(i), '08b') for i in message)
    

    # Convert the length of the message into binary
    lengthInBinaryForm = format(len(binary_message),'032b')

    # Convert the file type to binary
    encoded_text = file_type.encode('utf-8')
    fileTypeInBinaryForm = ''.join(format(byte, '08b') for byte in encoded_text)

    # Check if data length greater than song can hold
    if len(data) < (len(binary_message) + len(fileTypeInBinaryForm) + len(lengthInBinaryForm)):
        raise ValueError("The message is longer than the song can hold")

    # Skip forward until data isn't 0
    startIndex = 0
    while (data[startIndex][0] == 0):
        startIndex += 1
    

    # Prepend the length of the message to the message
    messageIdx = 0
    for i in range (startIndex, startIndex+(len(lengthInBinaryForm))): #should be 32 
        needToChange = lengthInBinaryForm[messageIdx]

        # If we need to change, increase amplitude by 1
        if (data[startIndex][0] == 0 and int(needToChange)):
            data[i][0] = 1

        elif (int(needToChange)):
            data[i][0] += 1
        
        startIndex += 1
        messageIdx += 1

    # Prepend the format of the file to the message
    messageIdx = 0
    for i in range (startIndex, startIndex+(len(fileTypeInBinaryForm))): #should be 24
        needToChange = fileTypeInBinaryForm[messageIdx]

        # If we need to change, increase amplitude by 1
        if (data[startIndex][0] == 0 and int(needToChange)):
            data[i][0] = 1

        elif (int(needToChange)):
            data[i][0] += 1
        
        startIndex += 1
        messageIdx += 1

    # Encode the message
    messageIdx = 0
    for i in range (startIndex, startIndex+(len(binary_message))):
        needToChange = binary_message[messageIdx]
    
        # If we need to change, flip the least significant bit
        if (data[i][0] == 0 and int(needToChange)):
            data[i][0] = 1

        elif (int(needToChange)):
            data[i][0] += 20
            
        messageIdx += 1


    # Save the modified audio
    wavfile.write(output_file_name, rate, data)


def decode_message(original_audio_file, encoded_audio_file):
    # Load the audio files
    sr1, data1 = wavfile.read(encoded_audio_file)
    sr2, data2 = wavfile.read(original_audio_file)


    # Store the bits of the message we recover
    bits = []

    # Store the length prepended to the message
    length = ''

    #store the format prepended to the message
    format = ''

    # Decoded Message
    message = ""

    # Skip forward until data isn't 0
    startIndex = 0
    while (data1[startIndex][0] == 0):
        startIndex += 1
    
    
    # Decode the length
    for i in range (startIndex, startIndex+32):
        if data1[i][0] != data2[i][0]:
            length += '1'
        else:
            length += '0'
    lengthOfMessage = int(length, 2)

    # We prepended an int and don't want it in the message
    startIndex += 32

    # Decode the format
    for i in range (startIndex, startIndex+24):
        if data1[i][0] != data2[i][0]:
            format += '1'
        else:
            format += '0'
    fileFormat = ''.join(chr(int(format[i:i+8], 2)) for i in range(0, len(format), 8))

    # We prepended the file format and don't want it in the message
    startIndex += 24

    # Decode the actual message
    for i in range (startIndex, startIndex+lengthOfMessage): 
        if data1[i][0] != data2[i][0]:
            bits.append('1')
        else:
            bits.append('0')

    # Convert the bits to characters
    if (fileFormat == "msg"):
        message = ''
        for i in range(0, len(bits), 8):
            byte = bits[i:i+8]
            message += chr(int(''.join(byte), 2))


    # Convert the integer back to bytes
    elif (fileFormat != "msg"):
        result_string = ''.join(bits)
        integer_value = int(result_string , 2)
        num_bytes = (len(result_string) + 7) // 8  # Calculate the number of bytes needed
        bytes_data = integer_value.to_bytes(num_bytes, 'big')
        with open("decodedMessage." + fileFormat, 'wb') as file:
            file.write(bytes_data)

    return message