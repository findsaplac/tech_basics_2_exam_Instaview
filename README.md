# Tech_Basics_2: Daniel Braun - Examproject: Instaview
This repository contains my Tech Basics II Exam Project code. I have built a MVP GUI for an 'Alternative-Front-End' to Instagram:


When you run the app.py you are greeted with a homepage, which has two buttons - one for a new user and one for the returning user.
        If this is the users first time on the app, then they will click on the new user button and register some information. This is data is stored in a .csv file. For this MVP I am sharing my test users data, but data privacy will be extremely important when I launch my app.
        If this the user has already registered, they can go to the returning user page and login with their information.
    Once a user registers or successfully logs in, they will be taken to the Online Pet Page where the pet changes based on the mood the user selects.

---

## Instructions to run my GUI
This is just for reference, and as mentioned above, you don't need to write detailed README files.

1. Clone my repository in a location of your choice

`git clone `

2. You should find my repository in your directory. You can change the directory in your terminal to where the cloned code is located:

cd python_tech_basics/tech_basics_two/13Lecture

    If you have activated a virtual environment, or it is your first time working with these libraries, you will need to install pandas and pillow:

Mac:

pip3 install pandas pillow

Windows:

pip install pandas pillow

    Run the code

Mac:

python3 app.py

Windows:

python app.py
