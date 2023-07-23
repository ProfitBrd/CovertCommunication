# CovertCommunication

For Flask Web App:
Download 'app.py' along with the 'templates' and 'files' folders and store them in the same directory for correct functionality.


### Dependencies
install python dependencies with `pip install -r requirements.txt`

### Running the Flask Web App
Run the Flask Web App with `python3 webServer.py`

### Running the Client
Run the Client with `python3 client.py`

Inside the server use the commands in the table to interact with the web server and perform encode/decode and upload/download operations.

### How the Covert Channel Works
The covert channel in this project works by encoding a message into a wav file and then uploading that file to the web server using a POST request. The encoding is done by incrementing the amplitude of each sample if the sensitive data at that bit is a `1` else the sample remains unchanged. Another client can then download the encoded WAV file and decode by checking each sample against the original WAV file and if the amplitude is greater than the original then the bit is a `1` else it is a `0`.