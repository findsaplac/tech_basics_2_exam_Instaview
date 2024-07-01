"""
InstaView. A MVP-GUI of an Alternative Front-End for Instagram.
   Findus - Daniel Braun, 06/2024.

 ---------------------------------------------------
"""

import customtkinter as ctk
import pandas as pd
from PIL import Image
from src.helpers import (create_timeline, show_account, check_logindata, initialize_data,
                         send_mainframe_widgets_vars_to_helpers)

# global size variables
sys_width = 400
sys_height = 800
header_height = 80
footer_height = 80
content_height = sys_height - (header_height + footer_height)

# GUI-window:
# create the GUI window
root = ctk.CTk()
# define title of GUI
root.title("InstaView")
# define size of GUI-window
root.minsize(sys_width, sys_height)

# global design_variables
text_font = ctk.CTkFont(family='Cantarell', size=16)

# global widget-variables:
mainframe = ctk.CTkFrame(root, width=sys_width, height=sys_height)
content_frame = ctk.CTkFrame(mainframe, width=sys_width, height=content_height, fg_color='white')


def new_potential_master_frame():
    print("#log: new_potential_master_frame())")
    potential_master_frame = ctk.CTkFrame(mainframe, width=sys_width, height=content_height, fg_color='white')
    return potential_master_frame


def create_login_page():
    """Function creates login-page: with among else a title, welcome-message, login-fields & labels and a
    login-button."""

    global login_page_frame, username_entry, password_entry

    # Create Frame:
    login_page_frame = ctk.CTkFrame(root, width=sys_width, height=sys_height)
    login_page_frame.pack()
    # Create Title-Label
    title = ctk.CTkLabel(login_page_frame, text='InstaView', font=("Cantarell", 32, 'bold'), text_color='#613f81')
    title.place(x=115, y=75)
    # Create Welcome Label
    welcome_label = ctk.CTkLabel(login_page_frame, text=f'Welcome to your privacy-friendly \naccess to instagram',
                                 font=("Cantarell", 19, 'bold', 'italic'), text_color='#98470b')
    welcome_label.place(x=12, y=150)

    # Create Login-Fields
    # Create Label: "Login or sign up if you don't have an account yet!"
    login_label = ctk.CTkLabel(login_page_frame, text=f"Login or sign up if you don't \nhave an account yet!",
                               font=text_font)
    login_label.place(x=80, y=280)
    # Username Label & Textbox
    username_label = ctk.CTkLabel(login_page_frame, text='Username:', font=text_font)
    username_label.place(x=60, y=360)
    username_entry = ctk.StringVar()
    username_box = ctk.CTkEntry(login_page_frame, textvariable=username_entry, font=text_font, height=20, width=250)
    username_box.place(x=70, y=385)
    # password
    password_label = ctk.CTkLabel(login_page_frame, text='Password: ', font=text_font)
    password_label.place(x=60, y=420)
    password_entry = ctk.StringVar()
    password_box = ctk.CTkEntry(login_page_frame, textvariable=password_entry, font=text_font, height=20, width=250)
    password_box.place(x=70, y=450)

    # Create Login-Button, which calls function: test_logindata()
    loginbutton = ctk.CTkButton(login_page_frame, text="Login/SignUp", font=("Canterell", 16), height=1, width=7,
                                hover_color='#98470b', fg_color='#613f81', command=login)
    loginbutton.place(x=185, y=500)

    """# Allow for Clicking 'Enter' in the Password-Entry-Box to take the same effect as Login-Button
    def load_check_logindata(event):
        check_logindata(username_entry.get(), password_entry.get())

    loginbutton.bind('<Return>', load_check_logindata())"""

    # Debug:
    print("#log: Login-Page created")


def login():
    """Function, controlling the login-steps."""
    global local_user_data

    # If check_logindata() returns true, call the function to initialize the user data (this gives back a pandas
    # dataframe with the local user's info).
    if check_logindata(username_entry.get(), password_entry.get()):
        local_user_data = initialize_data(username_entry.get(), password_entry.get())

        # Then, destroy the login-page & load the main-frame of homepage:
        login_page_frame.destroy()
        print("#log: @login(): Login-Page destroyed, load homepage-mainframe")
        create_mainframe(True)


def create_mainframe(load_timeline=False):
    """Function for loading the main frame of the logged-in views: top-bar & bottom bar"""
    # debug
    print("#log: create_mainframe()")

    global mainframe, content_frame
    # Create mainframe of logged-in state
    mainframe = ctk.CTkFrame(root, width=sys_width, height=sys_height)
    mainframe.pack()

    # Create header
    # Create frame
    header = ctk.CTkFrame(mainframe, width=sys_width, height=header_height)
    header.place(x=0, y=0)
    # Create label with username
    user_label = ctk.CTkLabel(header, text=f'@{local_user_data.iloc[0, 0]}', font=("Cantarell", 32, 'bold'))
    user_label.place(x=80, y=15)
    # Create image with local users profile picture (default-avatar)
    user_image = ctk.CTkImage(light_image=Image.open(local_user_data.iloc[0, 2]), size=(50, 50))
    user_image_label = ctk.CTkLabel(header, image=user_image, text="")  # display image with a CTkLabel
    user_image_label.place(x=260, y=15)
    # Create log-out Button
    logout_button = ctk.CTkButton(header, text='logout', width=30, command=logout, hover_color='#98470b',
                                  fg_color='#613f81')
    logout_button.place(x=320, y=25)
    print("#log: @create_mainframe(): header created")

    # Create footer
    # Create frame
    footer = ctk.CTkFrame(mainframe, width=sys_width, height=footer_height)  # grey: #c6c6c6
    footer.place(x=0, y=sys_height - header_height)
    # Create Button "Timeline"
    footer_button_timelineview = ctk.CTkButton(footer, text='Timeline', command=create_homepage_timeline,
                                               text_color='black', fg_color='transparent', hover_color='grey')
    footer_button_timelineview.grid(row=0, column=0, sticky="NSEW")
    # Create Button "My-Account"
    footer_button_profileview = ctk.CTkButton(footer, text='My Account', command=create_homepage_my_account,
                                              text_color='black', fg_color='transparent', hover_color='grey')
    footer_button_profileview.grid(row=0, column=1, sticky="NSEW")
    # Stretch the fields of the footer to fit the whole footer
    footer.columnconfigure(0, minsize=200)
    footer.columnconfigure(1, minsize=200)
    footer.rowconfigure(0, minsize=80)
    footer.rowconfigure(1, minsize=80)
    print("#log: @create_mainframe(): footer created")

    # Create content_frame to create displayed content in
    content_frame = ctk.CTkFrame(mainframe, width=sys_width, height=content_height, fg_color='white')
    content_frame.place(x=0, y=header_height)

    # Make the following widgets also available in the helpers script
    send_mainframe_widgets_vars_to_helpers(sys_width, content_height, header_height, mainframe, content_frame, header)

    # With the flag 'load_timeline' = true, which is set only at login, this function further calls the
    # create_homepage_timeline() function.
    # See below. this prevents a continous loop between the two functions.
    if load_timeline:
        create_homepage_timeline(True)


def create_homepage_timeline(keep_mainframe=False):
    """Function creates the Homepage with a chronological timeline of all posts of accounts, which the user follows."""
    print("#log: create_homepage_timeline()")

    # Role of the keep_mainframe - flag:
    # By default, this function erases the mainframe and all its contents, and goes to recreating it again by
    # calling create_mainframe() (note, that the create_mainframe() method does not by default re-evoke this
    # method here, so that) after this, it proceeds by creating the timeline (& doesn't get caught in a constant loop).
    # Only, after login, the erasure of the mainframe contents is skipped.
    if not keep_mainframe:
        # clear the formerly displayed content
        mainframe.destroy()
        create_mainframe()
        print(f"#log: @create_homepage_timeline(): mainframe destroyed")

    # Create the Homepage-Timeline
    homepage_timeline = create_timeline(content_frame, "all")
    homepage_timeline.place(x=0, y=0)
    print("#log: @create_homepage_timeline(): timeline displayed")


def create_homepage_my_account():
    """Function creates Homepage of the user's own account."""
    print("#log: create_homepage_my_account()")

    # clear the formerly displayed content
    mainframe.destroy()
    create_mainframe()
    print(f"#log: @create_homepage_my_account(): mainframe destroyed")

    # Create the Homepage of the user's account.
    show_account(content_frame, local_user_data.iloc[0, 0], True)


def logout():
    global mainframe
    mainframe.destroy()
    create_login_page()


# kick it los
create_login_page()

# execute the code above being continuously displayed on screen
root.mainloop()
