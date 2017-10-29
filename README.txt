----- TEAM NAME: DARING DUCKS--------
----- CS6340 : NLP PROJECT   --------

HOW TO COMPILE AND RUN THE CODE:

Make sure you have python in the system you try to run in.
Linux comes with python by default.
For Windows, python must be installed manually.

In the terminal or command prompt:
1. Move into the folder where the project folder (nlp_daringduck) is located. 
2. Move into the project folder.
3. Type in the terminal the following : 
/usr/local/stow/python/amd64_linux26/python-3.5.0/bin/python3 qa.py input_file
4. Hit Enter.


Doing so would display the output (QuestionID and Answer) on the command line as well as write the output into a "response_file.txt".

CONTENTS OF nlp_daringduck FOLDER:

1. qa.py - Python code for the QA system.
2. Required .txt files- location.txt, locationPrep.txt, occupation1.txt, PP.txt, time.txt, verbForms.txt, yob2000.txt
3. ReadMe File
4. We also have an input_file, answer_key file and a response_file - all that we used on the "developset" to test our output.


LIMITATIONS:

The code takes approximately 1 hour to run... PLEASE BE PATIENT !! :)

SCORING FOR ANSWER ACCURACY:

Run the following on the terminal:

perl score-answers.pl response_file.txt answer_key.txt

response_file.txt is the file into which our code prints the output other than on the terminal.


NOTE: This project was created in collaboration with HARSHITHA PARNANDI VENKATA. It is being uploaded into Github for record after project completion.
Originally, this project was maintained on Bitbucket.

