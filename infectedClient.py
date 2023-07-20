import audioConverter as ac
import requests
from io import BytesIO

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
def uploadAndEncrypt(original_file_name, encoded_file_name, message, is_binary):
    # Encode the file
    ac.encode_message(original_file_name, encoded_file_name, message, is_binary)
    
    # Upload the file
    upload_url = 'http://10.241.1.148:5000/upload'
    # files_original = {'file': open(original_file_name, 'rb')}
    files_encoded = {'file': open(encoded_file_name, 'rb')} #<<----
    # response_original = requests.post(upload_url, files=files_original)
    response_encoded = requests.post(upload_url, files=files_encoded)
    # print(response_original.text)  # File uploaded successfully!
    print(response_encoded.text)  # File uploaded successfully!
    
    
def downloadAndDecrypt(original_file_name, encoded_file_name):
    # Download a file
    # download_url_original = f'http://10.241.1.148:5000/files/{original_file_name}'
    download_url_encoded = f'http://10.241.1.148:5000/files/{encoded_file_name}'
    # response_original = requests.get(download_url_original)
    response_encoded = requests.get(download_url_encoded)
    # with open(original_file_name, 'wb') as file:
    #     file.write(response_original.content)
    with open(encoded_file_name, 'wb') as file:
        file.write(response_encoded.content)
    print('Files downloaded successfully!')
    
    print(ac.decode_message(original_file_name, encoded_file_name))


def main():
    print(title)
    try:
        uploadAndEncrypt('aviciiLevelsWAVoriginal.wav', 'findTheMessage.wav', 'This is a test', False)
        downloadAndDecrypt('aviciiLevelsWAVoriginal.wav', 'findTheMessage.wav')

    except ValueError as error:
        print("Error: " + str(error))

# Check if the current module is the main module
if __name__ == "__main__":
    main()