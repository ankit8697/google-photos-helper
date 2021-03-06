# Google Photos Uploading Tool

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)

## About <a name = "about"></a>

This tool allows you to select a folder on your computer which the program will work on. The program will upload all images inside the folder to your Google Photos account, and turn any subfolders into albums and add images inside those subfolders to those albums.

## Getting Started <a name = "getting_started"></a>

To get the program up and running on your local machine, follow the steps below:

- Clone the repository to a folder on your local machine.
- Create a new Python virtual environment and install the packages listed in requirements.txt
- Go to the Google Photos API and create the required credentials to get your API key. Select the "Other" option when asked what kind of application the credentials are for. Save it in the root directory as credentials.json.
- Run ```python3 main.py PATH/TO/IMAGES/DIRECTORY```

## Usage <a name = "usage"></a>

To use the program, you must have python3 installed. Call the main.py file with the command line argument being the path to the folder containing the images or folders of images. The program will prompt you to sign-in with your Gmail account. The program is currently not verified by Google so your browser will tell you it isn't verified, but you can continue to the authentication page. Once you accept all permissions and choose the account you want the photos to go into, the program will begin uploading images to the relevant Google Photos account. 

## Contributing

This project is in development to add potentially a website or a GUI Desktop application, so any contributions to add those features would be helpful.
