import customtkinter as ctk
import pandas as pd
from PIL import Image
from tkinter import messagebox


def kill(frame_to_destroy, back_button):
    frame_to_destroy.destroy()
    back_button.destroy()


def generate_back_button(frame_to_destroy):
    """When a certain 'removable frame' is created on top of the former content (e.g. the display of a user account) -
    (having the master "content_frame_wg"), correspondingly, a back-button gets created, which shall be able to remove
    this 'removable_frame', and - also itself.
    Pressing this button calls the function kill(frame_to_destroy, back_button)"""

    # Create backbutton
    back_button_image = ctk.CTkImage(light_image=Image.open("data/imgs/symbols/back_button3.png"), size=(40, 40))
    back_button = ctk.CTkButton(header_wg, width=15, height=10, fg_color='transparent', text="",
                                background_corner_colors=None, hover_color='light grey',
                                image=back_button_image, command=lambda: kill(frame_to_destroy, back_button))
    back_button.place(x=10, y=25)

    # Note: apparently, it works if the frame_to_destroy is a frame, and e.g. not, if it is a scrollableframe.


def send_mainframe_widgets_vars_to_helpers(sys_width, content_height, header_height, mainframe=None,
                                           content_frame=None, header=None):
    global sys_width_var, content_height_var, header_height_var, mainframe_wg, content_frame_wg, header_wg
    sys_width_var = sys_width
    content_height_var = content_height
    header_height_var = header_height
    mainframe_wg = mainframe
    content_frame_wg = content_frame
    header_wg = header


# def show_followed_accounts(master, username=""): # not implemented yet anymore.
    """Function which get's called from the homepage_my_account by the button "xy following".
    Displays a new frame, listing the user_accounts the user follows."""


def timeline_within_account(username):
    """Helper Function, which forwards the call to create a timeline 'within an account', from only the posts of a user,
       to the create_timeline() funtion. This is,
       - a) in order to have a step between, drawing a back-button
       - and b), as create_timeline gives back a widget, which needs to be handled."""
    # create a frame to contain the timeline
    timeline_within_account_frame = ctk.CTkFrame(content_frame_wg, fg_color='transparent', width=sys_width_var,
                                                 height=content_height_var)
    timeline_within_account_frame.place(x=0, y=0)

    # this gets assigned the timeline_scrollable_frame by create_timeline()
    timeline_within_account = create_timeline(timeline_within_account_frame, username)
    timeline_within_account.place(x=0, y=0)

    generate_back_button(timeline_within_account_frame)


def check_logindata(username, password):
    """Function checks two things:
        1. if the provided login-data is formally acceptable: the fields aren't empty and don't contain a ' ',
        2. and, for the case that the user already has an account, if the password provided is correct.
        If one option is false, an Error-Message is given out to the user.
        Else, it is proceeded with the login/signup by calling the login() function."""
    # Debug
    print(f"#log: check_logindata({username}, {password})")

    # 1: Check for formal correctness
    # if username or password are empty, give out an error-message about that
    if username == "" or password == "":
        messagebox.showerror('Error', 'Please give an username & a password.')
        print("#log: @check_logindata(): username &/ password empty")
    # if username or password contain " " (space-characters), give out an error-message about that
    elif " " in username or " " in password:
        messagebox.showerror('Error', 'Your username and password may not contain spaces: " ".')
        print("#log: @check_logindata(): username &/ password contain disallowed characters (space " ")")

    # 2. For the case, that the user already has an account, check, if the password provided is correct
    else:
        # Debug
        print("#log: @check_logindata(): LoginData-Check-formally: passed.")

        try:
            # Check, if the user has already an account, through trying to open their user-data file.
            local_user_data = pd.read_csv(f"data/local_users/user_{username}.csv")
            # If yes, Check, if the given password equals the stored one. If not, give error message.
            if password != local_user_data.iloc[0, 1]:
                messagebox.showerror('Error', 'You submitted a wrong password, please try again.')
                # Debug
                print("#log: @check_logindata(): LoginData-Check-password: wrong password.")
            else:
                # if yes, proceed with login.
                # Debug
                print("#log: @check_logindata(): LoginData-Check-password: correct password, logging in.")
                return True

        # if the user doesn't yet have an account, this will be created by the login function
        except FileNotFoundError:
            # debug
            print("#log: @check_logindata(): New user. Go to creating account by storing login details.")
            return True


def initialize_data(username, password):
    """Function checks, whether
        - a user with the given login-data is existing already, and in that case giving back their user-data info in
          a local_user_data dataframe
        - or, if no account yet exists, creates one for the user by storing their login-data in a new
          "user_{username}.csv"-file at "data/local_users/". It then also reads this file to 'local_user_data'.
    """

    # Debug
    print(f"#log: initialize_data({username}, {password})")

    # Check, if the user has already an account with the provided username & password, by checking if there
    # is already a file with the user's information.
    try:
        local_user_data = pd.read_csv(f"data/local_users/user_{username}.csv", index_col="index")
        # debug
        print("#log: @initialize_data(): user already has account - data read successfully")

    # if not, 'create an account' through storing the user's info in a new file: user_username.csv
    except FileNotFoundError:
        # log
        print("#log: @initialize_data(): creating new account.")

        # read the template 'source_local_user_data' into a dataframe: 'local_user_data'
        local_user_data = pd.read_csv("data/source_local_user_data.csv", index_col="index")
        # store the user's given username & password in a 2nd temporary dataframe
        input_user_data_df = pd.DataFrame({'username': [username], 'password': [password]})
        # update the 'local_user_data'-dataframe with the 'input_user_data_df' Dataframe
        local_user_data.update(input_user_data_df)
        # debug
        print("#log: @initialize_data(): storing new user's data as:\n", local_user_data)

        # save the generated new user's local_user_data-Dataframe into a .csv file with the username as part of filename
        local_user_data.to_csv(f"data/local_users/user_{username}.csv")
        print(f"#log: @initialize_data(): new user (login-)data stored successfully at: data/local_users/user_{username}.csv")

    return local_user_data


def display_account_details(master, user_data, local):
    """Function for creating the details part of account page: displaying profile picture, username, Title, Bio, etc."""

    print(f"#log: display_account_details({master.winfo_name()}, {type(user_data)}, local: {local})")

    # Create Parent Frame containing all the single widgets
    account_details_frame = ctk.CTkFrame(master, width=master.cget('width'), height=master.cget('height'),
                                         fg_color='white')
    account_details_frame.place(x=0, y=0)

    # Create Account Username Label
    username_label = ctk.CTkLabel(account_details_frame, text=user_data['username'], font=("Cantarell", 24,
                                                                                           'bold'), justify="left")
    username_label.grid(row=0, column=1, sticky="w")
    # Create user account picture
    user_account_img = ctk.CTkImage(light_image=Image.open(user_data['profile_image_path']), size=(80, 80))
    user_account_img_label = ctk.CTkLabel(account_details_frame, width=80, height=80, image=user_account_img, text="",
                                          fg_color='transparent')
    user_account_img_label.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky='w')

    stat_labels_frame = ctk.CTkFrame(account_details_frame, fg_color='transparent')
    stat_labels_frame.grid(row=1, column=1, rowspan=2, padx=10)
    # Create label Number Posts
    num_posts_label = ctk.CTkLabel(stat_labels_frame, text=f'{user_data['number_posts']}\nposts', width=20,
                                   font=("Cantarell", 14), justify='center')
    num_posts_label.grid(row=0, column=0, padx=5)
    # Create label Number Followers
    num_followers_label = ctk.CTkLabel(stat_labels_frame, text=f'{user_data['number_followers']}\nfollowers', width=20,
                                       font=("Cantarell", 14), justify='center')
    num_followers_label.grid(row=0, column=1, padx=5)
    # Create Info Number Following
    # if local==True, create button instead of label
    if local:
        num_following_button = ctk.CTkButton(stat_labels_frame, text=f'{user_data['number_following']}\nfollowing',
                                             width=20, font=("Cantarell", 14), text_color='black',
                                             fg_color='transparent', hover_color='light grey')
        num_following_button.grid(row=0, column=2, padx=5)
    else:
        num_following_label = ctk.CTkLabel(stat_labels_frame, text=f'{user_data['number_following']}\nfollowing',
                                           width=20, font=("Cantarell", 14), justify='center')
        num_following_label.grid(row=0, column=2, padx=5)
    # Create Account Title
    title_label = ctk.CTkLabel(account_details_frame, text=user_data['title'], wraplength=380,
                               font=("Cantarell", 15, "bold"))
    title_label.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="w")
    # Create Account Bio
    bio_label = ctk.CTkLabel(account_details_frame, text=user_data['bio'], font=("Cantarell", 13), wraplength=380,
                             justify='left')
    bio_label.grid(row=4, column=0, columnspan=2, padx=10, sticky="w")
    # Create Account Url
    url_label = ctk.CTkLabel(account_details_frame, text=user_data['url'], font=("Cantarell", 13), wraplength=380,
                             justify='left')
    url_label.grid(row=5, column=0, columnspan=2, padx=10, sticky="w")

    account_details_frame.columnconfigure(0, minsize=80)
    account_details_frame.columnconfigure(1, weight=1, minsize=320)
    account_details_frame.rowconfigure(0, minsize=80)
    account_details_frame.rowconfigure(1, minsize=20)

    print("#log: @show_account(): account detail-items created, returning account_details_frame")

    return account_details_frame


def create_post_grid(master, user_data):
    """Function displaying the post-images of a user account in a grid with 3 columns."""

    # print(f"#log: create_account_grid({master.winfo_name()}, {type(user_data)}, local: {local})")

    # Create Grid of User's posts

    # create container-frame
    grid_posts_frame = ctk.CTkFrame(master, fg_color='transparent')

    # Read Posts-Database into dataframe & filter it by username
    print("#log: @show_account(): reading users post-data")
    posts_user = pd.read_csv("data/source_posts.csv", index_col='index')
    posts_user = posts_user[posts_user['user_account'] == user_data['username']]
    # debug
    # print(posts_user)

    # Retrieve image_path variables for each post from this dataframe to create images of the posts
    for i in range(len(posts_user)):
        print("#log: @show_account(): creating grid of post-images")

        # retrieve file-path, create image & create button
        post_image = ctk.CTkImage(light_image=Image.open(posts_user.iloc[i, 4]), size=(110, 110))
        post_image_button = ctk.CTkButton(grid_posts_frame, width=110, height=110, fg_color='transparent',
                                          image=post_image, text="", hover_color='light grey',
                                          command=lambda: timeline_within_account(user_data['username']))
        # As the posts in the dataframe are sorted chronologicly (newest first), the index with which we iterate
        # in this direction through the dataframe [0, 1, 2..], serves as a representation of their order and
        # helps to fit them into a grid accordingly (top->bottom & left->right from new to old):
        # Specifying image column:
        if (i + 3) % 3 == 0:
            imgcolumn = 0
        elif (i + 2) % 3 == 0:
            imgcolumn = 1
        elif (i + 1) % 3 == 0:
            imgcolumn = 2
        # Specifying image row
        imgrow = int(i / 3)
        # .grid() Button acoordingly
        post_image_button.grid(row=imgrow, column=imgcolumn, sticky="n")

    print("#log: @show_account(): finished creating grid of post-images - returning frame, containing grid.")
    return grid_posts_frame


def show_account(master, username, local=False):
    """Method shows a certain user's profile."""

    print(f"#log: show_account({master.winfo_name()}, {username}, local: {local})")

    # master.place(x=0, y=80)

    # Import the user's account data - either from local-user file, or from (online-)accounts-database.
    if local:
        # Import user data of local user in dataframe
        user_data = pd.read_csv(f"data/local_users/user_{username}.csv", index_col="index")
        # Convert Dataframe into Series, to further process
        user_data = user_data.iloc[0, :]
        print("#log: @show_account(): local user-data read as:\n")
        print(user_data)
    else:
        # read accounts database and select account of given 'username' in dataframe
        accounts_db = pd.read_csv("data/source_accounts.csv", index_col="index")
        user_data = accounts_db[accounts_db["username"] == username]
        # Convert Dataframe into Series, to further process
        user_data = user_data.iloc[0, :]
        print("#log: @show_account(): online user-data read as:\n")
        print(user_data)

    # Create Parent Account Frame to contain both, followingly seperately created items: profile_details & the post-grid
    account_frame = ctk.CTkFrame(master, width=master.cget('width'), height=master.cget('height'), fg_color='white')
    account_frame.place(x=0, y=0)

    # Call Function to create account details to give back a containing-frame of all single items.
    account_details = display_account_details(account_frame, user_data, local)
    account_details.grid(row=0, column=0)
    account_frame.rowconfigure(0, minsize=280)

    # only for online-accounts (as local users don't & can't have images at this moment of development)
    if not local:
        # Call Function to create grid of posts of useraccount
        grid_posts = create_post_grid(account_frame, user_data)
        grid_posts.grid(row=1, column=0, sticky="n")
        account_frame.rowconfigure(1, minsize=360)

    if not local:
        generate_back_button(account_frame)


def create_post(master, post_data):
    """Method creates and gives back a single post (to be included in a timeline) within the master-widget, it gets #
    and gives this post back in the form of a frame (containing the single post's items)."""

    print(f"#log: create_post({type(master)}, {type(post_data)})")
    # create containing frame
    post_frame = ctk.CTkFrame(master, width=master.cget('width'), fg_color=master.cget('fg_color'))

    # Create User-Account's Profile-Image
    # read accounts-database, where information of filepath of user's account-image is, slice this user's entry out
    # of the database, and give out the image_filepath value
    accounts_db = pd.read_csv("data/source_accounts.csv", index_col="index")
    user_data = accounts_db[accounts_db["username"] == post_data['user_account']]
    user_account_image_filepath = user_data.iloc[0, 2]
    # Create image and button with the image retrieved.
    user_account_img = ctk.CTkImage(light_image=Image.open(user_account_image_filepath), size=(60, 60))
    user_account_img_button = ctk.CTkButton(post_frame, width=60, height=0, fg_color='transparent',
                                            background_corner_colors=None, image=user_account_img, text="",
                                            command=lambda: show_account(content_frame_wg, post_data['user_account']))
    user_account_img_button.grid(row=0, column=0, sticky="w")

    # Create account-name as button
    user_account_name_button = ctk.CTkButton(post_frame, fg_color='transparent', hover=False,
                                             text=post_data['user_account'], font=("Cantarell", 17, 'bold'),
                                             text_color=('black', 'white'),
                                             command=lambda: show_account(content_frame_wg, post_data['user_account']))
    user_account_name_button.grid(row=0, column=1, sticky="w")

    # Create post_image in this frame
    post_img = ctk.CTkImage(light_image=Image.open(post_data['image_path']), size=(360, 360))
    post_img_label = ctk.CTkLabel(post_frame, width=360, height=360, bg_color='transparent', image=post_img, text='')
    post_img_label.grid(row=1, column=0, columnspan=2, padx=5, pady=6, sticky="w")

    # Create caption
    caption = ctk.CTkLabel(post_frame, text=post_data['caption'], wraplength=360, justify='left')
    caption.grid(row=2, column=0, columnspan=2, ipadx=8, sticky="w")

    post_frame.columnconfigure(0, minsize=55)
    post_frame.columnconfigure(1, minsize=340)

    # print("#log: @create_post(): all post-widgets created, returning post frame")

    # give back frame
    return post_frame


def create_timeline(master, post_select):
    """Method creates a timeline within a given master widget and from a selection of posts.
    This is either specified by the 'username' of the account who's posts to list, or for the general homepage-timeline,
    by 'all' as keyword."""

    print(f"#log: create_timeline({type(master)}, {post_select})")

    # create scrollable frame
    timeline_scrollable_frame = ctk.CTkScrollableFrame(master, width=master.cget('width') - 20,
                                                       height=master.cget('height') - 10, fg_color='white')
    print("#log: @create_timeline(): timeline_scrollable_frame created")

    # Organise the Posts-Data to be displayed in  the Timeline
    # Read post_database as dataframe
    posts_for_timeline = pd.read_csv("data/source_posts.csv", index_col="index",
                                     parse_dates=["date"], date_format="%d/%m/%Y")
    # From this DataFrame, select all rows (posts), which have 'followed'=True
    posts_for_timeline = posts_for_timeline[posts_for_timeline['followed'] == True]
    # if the selection is by a certain username, shrink the dataframe accordingly
    if post_select != 'all':
        posts_for_timeline = posts_for_timeline[posts_for_timeline['user_account'] == post_select]
    print("#log: @create_timeline(): Posts data to give in timeline organised as:")
    print(posts_for_timeline)

    # Create Posts in order below another in the timeline_scrollable_frame:
    # Iterate 'through the dataframe' of posts: for each row of Dataframe (each post) calling the create_post() method.
    # This method gives back a CTkFrame widget which is placed within the timeline_scrollable_frame afterwards.
    for i in range(len(posts_for_timeline)):
        # The create_post method gets the timeline_scrollable_frame-widget as parent widget, and the data of one post
        # respectively as a pandas Series, sliced out of the posts_for_timeline Dataframe.
        post = create_post(timeline_scrollable_frame, posts_for_timeline.iloc[i])
        # placing this in the scrollable_frame
        post.grid(row=i, column=0, padx=10, pady=20, ipadx=10)
        print("#log: @create_timeline(): post created, next iteration")

    print("#log: @create_timeline(): all posts created")
    print("#log: @create_timeline(): timeline created, returning timeline")
    return timeline_scrollable_frame
