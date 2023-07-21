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

table = [["Encode and Upload File:", "encodeAndUpload [filename.wav] \'[message]\' [ip address and port]"],["Encode a file","encode [filename.wav] \'[message]\'"],["Download and Decode File:","downloadAndDecode [filename.wav] [ip address and port]"],["Decode a File", "decode [filename.wav]"]]

def encodeAndUpload(original_file_name, message, is_binary, ip_and_port):
    
    encoded_file_name = original_file_name.replace('.wav', 'Encoded.wav')

    # Encode the file
    ac.encode_message(original_file_name, encoded_file_name, message, is_binary)
    
    # Upload the file
    upload_url = f'http://{ip_and_port}/upload'
    files_encoded = {'file': open(encoded_file_name, 'rb')}
    response_encoded = requests.post(upload_url, files=files_encoded)
    print(response_encoded.text)  # Output: File uploaded successfully!
    
    
def downloadAndDecode(original_file_name, ip_and_port):
    encoded_file_name = original_file_name.replace('.wav', 'Encoded.wav')

    # Download a file
    download_url_encoded = f'http://{ip_and_port}/files/{encoded_file_name}'
    response_encoded = requests.get(download_url_encoded)
    with open(encoded_file_name, 'wb') as file:
        file.write(response_encoded.content)
    print('Files downloaded successfully!')
    
    #Decode that file
    print(ac.decode_message(original_file_name, encoded_file_name))


def main():
    print(title)
    while (True):
        print()
        # print(tabulate(table, headers = ["Explanation", "Code"], tablefmt="outline"))
        userInput = input(tabulate(table, headers = ["Explanation", "Code"], tablefmt="outline") + "\n\n>")
        userInput = shlex.split(userInput)

        # Upload and Ecrypt
        if (userInput[0].lower() == 'encodeandupload'):
            try:
                encodeAndUpload(userInput[0], userInput[1], False, userInput[2])

            except ValueError as error:
                print("Error: " + str(error))
            except IndexError as error:
                print("Missing Arguments!")
            
        # Download and Decode
        elif(userInput[0].lower() == 'downloadanddecode'):
            try:
                downloadAndDecode(userInput[0], userInput[1])

            except ValueError as error:
                print("Error: " + str(error))
            except IndexError as error:
                print("Missing Arguments!")
        
        # Decode a file
        elif(userInput[0].lower() == 'decode'):
            try:
                original_file_name = userInput[1].replace('Encoded.wav', '.wav')
                print(ac.decode_message(original_file_name, userInput[1]))

            except ValueError as error:
                print("Error: " + str(error))
            except IndexError as error:
                print("Missing Arguments!")
        
        # Encode a file
        elif(userInput[0].lower() == 'encode'):
            try:
                encoded_file_name = userInput[1].replace('.wav', 'Encoded.wav')
                ac.encode_message(userInput[1], encoded_file_name, userInput[2], False)

            except ValueError as error:
                print("Error: " + str(error))
            except IndexError as error:
                print("Missing Arguments!")

        # Invalid Format
        else:
            print('Invalid Format!')

# Check if the current module is the main module
if __name__ == "__main__":
    main()