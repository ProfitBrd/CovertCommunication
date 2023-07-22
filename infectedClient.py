import audioConverter as ac
import requests
from io import BytesIO
from tabulate import tabulate
import shlex as shlex

headers = {
                "Host": "http://192.168.15.25:5000",
                "Connection": "keep-alive",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
                "Upgrade-Insecure-Requests": "1",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
}

title = '''
 ______   __       ________   ___   __         _______   ______   ______      
/_____/\\ /_/\\     /_______/\\ /__/\\ /__/\\     /_______/\\ /_____/\\ /_____/\\     
\\:::_ \\ \\\\:\\ \\    \\::: _  \\ \\\\::\\_\\\\  \\ \\    \\::: _  \\ \\\\::::_\\/_\\::::_\\/_    
 \\:(_) \\ \\\\:\\ \\    \\::(_)  \\ \\\\:. `-\\  \\ \\    \\::(_)  \\/_\\:\\/___/\\\\:\\/___/\\   
  \\: ___\\/ \\:\\ \\____\\:: __  \\ \\\\:. _    \\ \\    \\::  _  \\ \\\\::___\\/_\\::___\\/_  
   \\ \\ \\    \\:\\/___/\\\\:.\\ \\  \\ \\\\. \\`-\\  \\ \\    \\::(_)  \\ \\\\:\\____/\\\\:\\____/\\ 
    \\_\\/     \\_____\\/ \\__\\/\\__\\/ \\__\\/ \\__\\/     \\_______\\/ \\_____\\/ \\_____\\/ 
                                                                              
'''

table = [["Encode and Upload A Text Message:", "encodeAndUpload [filename.wav] \'[message]\' [ip address and port]"],["Encode A Text Message","encode [filename.wav] \'[message]\'"],["Download and Decode A Text Message:","downloadAndDecode [encodedFilename.wav] [ip address and port]"],["Decode A Text Message", "decode [encodedFilename.wav]"],["-------------------------", "--------------------------------------------------------"],["Encode and Upload A File:", "encodeAndUploadFile [filename.wav] \'[fileToBeEncoded]\' [ip address and port]"],["Encode A File","encodeFile [filename.wav] \'[fileToBeEncoded]\'"],["Download and Decode A File:","downloadAndDecodeFile [encodeFilename.wav] [ip address and port]"],["Decode A File", "decodeFile [encodedFilename.wav]"]]


def encode(original_file_name, message, is_binary, file_type, input_file):
    encoded_file_name = original_file_name.replace('.wav', 'Encoded.wav')
    
    # Encode the file
    ac.encode_message(original_file_name, encoded_file_name, message, is_binary, file_type, input_file)
    print("Successfully Encoded!")

def upload(original_file_name, ip_and_port):
    encoded_file_name = original_file_name.replace('.wav', 'Encoded.wav')

    # Upload the file
    upload_url = f'http://{ip_and_port}/upload'
    files_encoded = {'file': open(encoded_file_name, 'rb')}
    response_encoded = requests.post(upload_url, files=files_encoded)
    print(response_encoded.text)  # Output: File uploaded successfully!
    
def decode(encoded_file_name):
    original_file_name = encoded_file_name.replace('Encoded.wav', '.wav')
    #Decode the file
    return ac.decode_message(original_file_name, encoded_file_name)


def download(original_file_name, ip_and_port):
    encoded_file_name = original_file_name.replace('.wav', 'Encoded.wav')

    # Download a file
    download_url_encoded = f'http://{ip_and_port}/files/{encoded_file_name}'
    response_encoded = requests.get(download_url_encoded)
    with open(encoded_file_name, 'wb') as file:
        file.write(response_encoded.content)
    print('Files downloaded successfully!')
    
    


def main():
    print(title)
    while (True):
        try:
        
            print()
            userInput = input(tabulate(table, headers = ["Explanation", "Command"], tablefmt="outline") + "\n\n>")
            userInput = shlex.split(userInput)

            # Encode Text Message --> encode [filename.wav] '[message]'
            if(userInput[0].lower() == 'encode'):
                encode(userInput[1], userInput[2], False, "msg", "")
            
            # Decode Text Message --> decode [filename.wav]
            elif(userInput[0].lower() == 'decode'):
                print(decode(userInput[1]))

            # Upload and Ecrypt Text Message --> encodeAndUpload [filename.wav] '[message]' [ip address and port] 
            elif (userInput[0].lower() == 'encodeandupload'):
                encode(userInput[1], userInput[2], False, "msg")
                upload(userInput[1], userInput[3])
                
            # Download and Decode Text Message --> downloadAndDecode [filename.wav] [ip address and port]
            elif(userInput[0].lower() == 'downloadanddecode'):
                    download(userInput[1], userInput[2])
                    print(decode(userInput[1]))

            #-----------------------------------------------------BINARY BELOW
            
            elif (userInput[0].lower() == 'encodefile'):
                extension = userInput[2].split('.')[1]
                encode(userInput[1], "", True, extension, userInput[2]) # No message when transferring files

            elif (userInput[0].lower() == 'decodefile'):
                print(decode(userInput[1]))

            elif (userInput[0].lower() == 'encodeanduploadfile'):
                encode(userInput[1], "", True, extension, userInput[2]) # No message when transferring files
                upload(userInput[1], userInput[3])

            elif (userInput[0].lower() == 'decodefile'):
                print(decode(userInput[1]))
                upload(userInput[1], userInput[2])
                
            
            # Invalid Format
            else:
                print('Invalid Format!')
        

        except ValueError as error:
                print("Error: " + str(error))
        except IndexError as error:
            print("Missing Arguments!")



if __name__ == "__main__":
    main()


#splitting the thing
#writing to the files wrong