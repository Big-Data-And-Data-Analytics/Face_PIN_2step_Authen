# Two-Factor Authentication for ATM System
The Facial Recognition System that is implemented in this project will integrate a facial recognition module to the existing ATM cash withdrawal process thus adding a 2-step verification alongside the pin authentication module.
The customers will need to go through a facial recognition phase as they simultaneously go through the pin authentication process.
<br/>In this facial recognition module, we have proposed Inception-ResNet V1 as the machine learning CNN model to identify faces of the bank's customers.
The model has been initially trained on sample faces to capture the characteristics of a human face and subsequently trained on the LFW dataset with more than two hundred classes thereby providing better accuracy.

---------------
#### Setup the repository
Step 1:
<br/>Install all the necessary packages using [requirements.txt](https://github.com/Big-Data-And-Data-Analytics/Face_PIN_2step_Authen/blob/master/Documents/requirements.txt)
<br/>
<br/>Step 1.a:
<br/>Follow the steps present in [Document/]() to install all the necessary python packages using requirements.txt
<br/>
<br/>Step 2
<br/>Start the application by running the python file [gui.py](https://github.com/Big-Data-And-Data-Analytics/Face_PIN_2step_Authen/blob/master/gui.py)

---------------
#### About the repository
1. The training dataset contains over 20000 images, belonging to 200+ classes. To avoid unbiased results, each class contains 100 images.
<br/>[Face_PIN_2step_Authen/aligned_image_data/](https://github.com/Big-Data-And-Data-Analytics/Face_PIN_2step_Authen/tree/master/aligned_image_data)
  
2. The testing dataset contains over 4000 images, belonging to 200+ classes. To avoid unbiased results, each class contains 20 images.
<br/>[Face_PIN_2step_Authen/test_images/](https://github.com/Big-Data-And-Data-Analytics/Face_PIN_2step_Authen/tree/master/test_images)
  
3. The username and PIN are stored in a JSON file, this file acts a dummy database.
<br/>[Face_PIN_2step_Authen/File/userCredentials.json](https://github.com/Big-Data-And-Data-Analytics/Face_PIN_2step_Authen/blob/master/File/userCredentials.json)
  
4. The model can be evaluated using [evaluation.py](https://github.com/Big-Data-And-Data-Analytics/Face_PIN_2step_Authen/blob/master/evaluation.py)
<br/>We have achieved a model accuracy of 89.60%
<br/>![Alt text](https://github.com/Big-Data-And-Data-Analytics/Face_PIN_2step_Authen/blob/master/screenshots/Test4100_89.PNG  "Model Accuracy")

---------------
#### UI Demo
The application provides two options
1. Create New User
2. Existing User
<!-- -->
1. To create a new user, username and PIN is required.
When the user clicks on “save login details”, two threads are started.
One thread saves the login credentials into the database and second thread capture the user image. Login credentials and image, both are stored simultaneously.
<br/>![Alt text](https://github.com/Big-Data-And-Data-Analytics/Face_PIN_2step_Authen/blob/master/screenshots/UI/Create%20New%20User.PNG "Create New User")
  
2. While accessing as an existing user, the user must enter his username and PIN. When the user clicks on “Login” button, two threads are started. One thread verifies the username and PIN, another thread verifies the image.	Both the processes happen simultaneously.	If anyone the process fails, the user is not allowed to perform the transaction.
<br/>![Alt text](https://github.com/Big-Data-And-Data-Analytics/Face_PIN_2step_Authen/blob/master/screenshots/UI/2%20step_PIN_Face.PNG "Existing User")
<br/>When the user credentials and face are of same user, then only the user can perform the transaction.
<br/>![Alt text](https://github.com/Big-Data-And-Data-Analytics/Face_PIN_2step_Authen/blob/master/screenshots/UI/Face_PIN_same%20user.PNG "User credential & Face Match")
  
3. If the username & PIN does not match with the face, the user is not allowed to perform transaction.
<br/>![Alt text](https://github.com/Big-Data-And-Data-Analytics/Face_PIN_2step_Authen/blob/master/screenshots/UI/Login%20with%20mask3.PNG "User credential & Face NOT Match")
