# Tech_Basics_2: Daniel Braun - Exam-Project: 'Instaview'

---
This repository contains my Tech Basics II Exam Project. I have built a MVP GUI for an 'Alternative-Front-End' to Instagram:

If you run the app.py application, you find yourself in front of sth, that looks quite like instagram? (in some way, I hope. (at least, after the login-screen;). 



Alternative Front-Ends are a tool to access a plattform as e.g. Youtube, Instagram etc. - for example, if you don't want these companies to use so much of your (valuable) user data:). They are most FOSS software that present the Contents (Videos, etc.) - in a 2nd layer - 'in a new GUI', so you can reach them, without the data-stealing of Meta & co reaching you <3. They're quite cool :). Check out [here](https://github.com/mendel5/alternative-front-ends?tab=readme-ov-file) 4 mo info!

This is, what this app tries to represent in a very small demo-format (offline): an alternative front-end to Instagram. #ReclaimOurData #OurWorldOurInfrastructure

Features: 
- Login into user-account
- Follow other users & their posts
- Browse (chronological) timeline
- [ ] Liking posts, commenting, sharing / posting yourself
- [ ] Stories & Reels
- [ ] other...

have fun


---

## Instructions to run my GUI

1. Clone my repository in a location of your choice

```
git clone ...
```

2. You should find my repository in your directory. You can change the directory in your terminal to where the cloned code is located:
```
cd ....
``` 

3. If you have activated a virtual environment, or it is your first time working with these libraries, you will need to install customtkinter, pandas and pillow:

Mac/Linux:
```
pip3 install customtkinter pandas pillow
``` 

Windows:
```
pip install customtkinter pandas pillow
``` 
**Run the code**

Mac/Linux:
```
python3 app.py
```

Windows:
```
python app.py
```