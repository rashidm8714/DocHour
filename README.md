# DocHour


## Setup
1. install python (https://www.python.org/ftp/python/3.11.1/python-3.11.1-amd64.exe)
    
    don't forget to add as enviroment variable while installing ( how to do : https://drive.google.com/file/d/1y_HXNBPkXcLPN2dY4FHfo6gKh-gFRmnQ/view?usp=share_link)

2. Download and install vs code (https://code.visualstudio.com/download)

3. install git (https://www.geeksforgeeks.org/introduction-and-installation-of-git/)

4. create a folder and open vs code in that folder

5. open terminal in vs code

6. To check whether git is correctly installed

      `git -v`

7. cloning the project (downloading project to local machine)

      `https://github.com/rashidm8714/DocHour.git` 

8. go to project directory

      `cd DocHour`
      
9. create a virtual environment

    `python -m venv env`
    
10. activating environment

      `env\Scripts\activate`

11. To install required libraries 

     `pip install -r requirements.txt`
     
12.updating database

     python manage.py makemigrations
     python manage.py migrate
     
## Running the project

`python manage.py runserver`

All done! server running!


screenshot of the process : https://drive.google.com/file/d/1e3SQ67AeM0Fh2vic6eJb8TRXuyeprxqv/view?usp=share_link

