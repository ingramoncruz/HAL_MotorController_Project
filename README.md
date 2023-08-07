# HAL_MotorController_Project
This is a rep for the final project to be delivered at the Advanced Python Bootcamp from CodigoFacilito. And consist of a HAL of two different types of controllers.

# REQUIREMENTS
Just run this program in Windows 10 or +. With a 64bit system. 
The pythong used with this app is 3.10 version.

# Python Pip Installs
Consider to install the next modules from Python:
- pip install PyQt5
- pip install pythonnet
- pip install PyQt5Designer

# PI Motor Controller Driver
You need to install the PI Software Suite provided from PI Company. You can download it from:
- The next [google drive folder](https://drive.google.com/drive/folders/1RtPNm62ZJxk-qgdb-JEMKJjKYlB4zoFs?usp=sharing)
- Or go to the [PI Web Site](https://www.physikinstrumente.com/en/knowledge-center/downloads/product-documentation/A)

After installing the SW Suite you can open the SPiiPlus MMI Application Studio 2.30 app.
- Then in the Workspace box, right clic in the folder shown and clic in Add Controller.
- Name it as you wish and then double clic in the red icon (red circle with white cross).
- Then go to the Simulator tab. And clic in Connect.
- After some seconds you will see that the icon turns out in Green Color.
- Double clic again in the icon, but this time go to Ethernet tab.
- Copy the Controller IP Address (Example '172.25.176.1') and then clic in Connect.
- Go to the Config folder in the main root path, and open the PI_Motor_Config.ini to paste the IP Address.

Now you are ready to run the program.
