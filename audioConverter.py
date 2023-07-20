from scipy.io import wavfile
import numpy as np

# Message Encoding
def encode_message(audio_file, output_file_name, message, is_binary):
    # Load the audio file
    rate, data = wavfile.read(audio_file)

    
    # Convert the message to binary if it is not already binary
    if (is_binary):
        binary_message = message
    else:
        binary_message = ''.join(format(ord(i), '08b') for i in message)
    

    # Convert the length of the message into binary
    lengthInBinaryForm = format(len(binary_message),'032b')

    if len(data) < (len(binary_message) + len(lengthInBinaryForm)):
        raise ValueError("The message is longer than the song can hold")

    # Skip forward until data isn't 0
    startIndex = 0
    while (data[startIndex][0] == 0):
        startIndex += 1
    

    messageIdx = 0
    # Prepend the length of the message to the message
    for i in range (startIndex, startIndex+(len(lengthInBinaryForm))): #should be 32 
        needToChange = lengthInBinaryForm[messageIdx]

        # If we need to change, increase amplitude by 1
        if (data[startIndex][0] == 0 and int(needToChange)):
            data[i][0] = 1

        elif (int(needToChange)):
            data[i][0] += 1
        
        startIndex += 1
        messageIdx += 1

    #encode the message
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
    print('hello')
    sr1, data1 = wavfile.read(encoded_audio_file)
    print('second')
    sr2, data2 = wavfile.read(original_audio_file)


    # Store the bits of the message we recover
    bits = []

    # Store the length prepended to the message
    length = ''

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

    # Because we prepended an int and don't want it in the message
    startIndex += 32

    # Decode the actual message
    for i in range (startIndex, startIndex+lengthOfMessage): 
        if data1[i][0] != data2[i][0]:
            bits.append('1')
        else:
            bits.append('0')

    # Convert the bits to characters
    message = ''
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        message += chr(int(''.join(byte), 2))

    return message


title = '''
 ______   __       ________   ___   __         _______   ______   ______      
/_____/\\ /_/\\     /_______/\\ /__/\\ /__/\\     /_______/\\ /_____/\\ /_____/\\     
\\:::_ \\ \\\\:\\ \\    \\::: _  \\ \\\\::\\_\\\\  \\ \\    \\::: _  \\ \\\\::::_\\/_\\::::_\\/_    
 \\:(_) \\ \\\\:\\ \\    \\::(_)  \\ \\\\:. `-\\  \\ \\    \\::(_)  \\/_\\:\\/___/\\\\:\\/___/\\   
  \\: ___\\/ \\:\\ \\____\\:: __  \\ \\\\:. _    \\ \\    \\::  _  \\ \\\\::___\\/_\\::___\\/_  
   \\ \\ \\    \\:\\/___/\\\\:.\\ \\  \\ \\\\. \\`-\\  \\ \\    \\::(_)  \\ \\\\:\\____/\\\\:\\____/\\ 
    \\_\\/     \\_____\\/ \\__\\/\\__\\/ \\__\\/ \\__\\/     \\_______\\/ \\_____\\/ \\_____\\/ 
                                                                              


'''

# try:
#     print(title)
#     encode_message('aviciiLevelsWAV.wav', 'findTheMessage.wav', 'This is a test', False)
#     print(decode_message('aviciiLevelsWAV.wav', 'findTheMessage.wav'))

# except ValueError as error:
#     print("Error: " + str(error))
