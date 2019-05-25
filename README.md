## 3-D-eyeless-Vision

### Implementation Details -

- The project has an android code and also another python folder object_detection which needs to be added to the htdocs of the apache server. 
- I used Xampp as the apache server. Make sure you make the changes required in the CGI file to allow python backend support. - - Now the main script is main.py which will check the Iplist.txt and create a subprocess for each instance. The file creates a subprocess of objectt.py which contains all the functions for the example, following a person, detecting a particular object, pop up message, text detection by creating countours and segmenting the image. 
- The App hits the test.py which checks whether there is an istance of that IP running, and if it is not running it creates a subprocess and temporary files for the same. The application can receives data in JSON format which converts the text to speech. 
- Also here Google tensorflow SSD Mobilenet model has been used for the task of object detection.

- Google tensorflow object detection link - https://github.com/tensorflow/models/tree/master/research/object_detection
- After downloading the object_detection form the above link replace the utils and add the above files. 
- Make sure you change the IP address to your server IP address in the above java app.
- Use the above java files to create a new Eyes Application. 
