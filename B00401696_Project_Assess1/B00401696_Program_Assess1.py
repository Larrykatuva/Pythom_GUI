import tkinter as tk
from PIL import ImageTk  # Install using pip install pillow
from tkinter import messagebox
import json
import re
import pickle

LARGE_FONT = ("Verdana", 12)

"""
    MainApp class which launches the Main window frame
    Loops the frames in its main container
"""


class MainApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # Adding title to the main window
        self.title("Account Login")
        # Setting window dimensions
        self.geometry("1100x600+50+30")
        # setting background image to the main window
        self.bg = ImageTk.PhotoImage(file="images/s2.jpg")
        self.bg_image = tk.Label(self, image=self.bg)
        self.bg_image.place(x=0, y=0, relwidth=1, relheight=1)

        # initializing a new container
        container = tk.Frame(self)
        # Setting container dimensions
        container.place(x=200, y=150, height=340, width=750)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Initializing a frome list
        self.frames = {}

        # Looping over frame list and each time setting a new frame to the main container
        for F in (HomePage, LoginPage, RegisterPage, Dashboard):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(HomePage)

    # Displaying the main frame
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


"""
    --HomePage class which launches the goto action page
    --Lands the user to login or register page on button click
"""


class HomePage(tk.Frame):

    # Class constructor
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # Initializing the login main frame
        main_frame = tk.Frame(self, bg="white")
        # Setting mainframe dimensions
        main_frame.place(x=0, y=0, height=340, width=750)

        # Mainframe title
        title = tk.Label(main_frame, text="Select User Action",
                         font=("Impact", 35, "bold"), fg="#d77337", bg="white").place(x=70, y=30)
        # Mainframe description one
        desc = tk.Label(main_frame, text="> Existing customers can login using their username and password.",
                        font=("Goudy old style", 17, "bold"),
                        fg="grey", bg="white").place(x=70, y=100)
        # Mainframe description two
        desc1 = tk.Label(main_frame, text="> New customers can register their details .",
                         font=("Goudy old style", 17, "bold"),
                         fg="grey", bg="white").place(x=70, y=130)
        # Mainframe login button
        login_btn = tk.Button(main_frame, text="Login", command=lambda: controller.show_frame(LoginPage),
                              fg="white", bg="#d77337", bd=0,
                              font=("times new roman", 15)).place(x=110, y=200, width=130, height=30)
        # Mainframe registration button
        register_btn = tk.Button(main_frame, text="Register", command=lambda: controller.show_frame(RegisterPage),
                                 fg="white", bg="#d77337", bd=0,
                                 font=("times new roman", 15)).place(x=400, y=200, width=130, height=30)


"""
    --LoginPage class which launches the login page
    --Handles the user login functions
"""


class LoginPage(tk.Frame):
    # Class constructor
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="white")
        # Initializing the mainframe frame
        Frame_login = tk.Frame(self, bg="white")
        Frame_login.place(x=0, y=0, height=340, width=750)

        # ==image Frame====
        Frame_image = tk.Frame(Frame_login)
        Frame_image.place(x=0, y=0, height=340, width=300)
        Frame_image.bg = ImageTk.PhotoImage(file="images/login.png")
        Frame_image.bg_image = tk.Label(Frame_image, image=Frame_image.bg)
        Frame_image.bg_image.place(x=0, y=0, relwidth=1, relheight=1)

        # mainframe title
        title = tk.Label(Frame_login, text="Login Here",
                         font=("Impact", 35, "bold"), fg="#d77337", bg="white").place(x=340, y=30)
        # mainframe description
        desc = tk.Label(Frame_login, text="Login to access your information",
                        font=("Goudy old style", 15, "bold"),
                        fg="#d25d17", bg="white").place(x=340, y=100)
        # mainframe username label
        Username = tk.Label(Frame_login, text="Username",
                            font=("Goudy old style", 15, "bold"),
                            fg="gray", bg="white").place(x=340, y=140)
        # mainframe user input
        txt_user = tk.Entry(Frame_login, font=("times new roman", 15), bg="lightgray")
        txt_user.place(x=340, y=170, width=350, height=35)
        # mainframe password label
        Password = tk.Label(Frame_login, text="Password",
                            font=("Goudy old style", 15, "bold"),
                            fg="gray", bg="white").place(x=340, y=210)
        # mainframe password input
        txt_pass = tk.Entry(Frame_login, font=("times new roman", 15), bg="lightgray")
        txt_pass.place(x=340, y=240, width=350, height=35)
        # mainframe login button
        login_btn = tk.Button(Frame_login, text="Login", command=lambda: loginUser(self),
                              fg="white", bg="#d77337", bd=0,
                              font=("times new roman", 15)).place(x=340, y=280, width=130, height=30)
        # mainframe back button
        back_btn = tk.Button(Frame_login, text="Back", command=lambda: controller.show_frame(HomePage),
                             fg="white", bg="#d77337", bd=0,
                             font=("times new roman", 15)).place(x=560, y=280, width=130, height=30)

        # User login function
        def loginUser(self):
            # Getting the inputs data
            username = txt_user.get()
            password = txt_pass.get()
            # Initializing the loginuservalidation class
            validation = loginUserValidation()
            # Checking if all inputs are supplied
            if not validation.check_inputs(username, password):
                # Checking if supplied user exist
                if validation.if_user_exist(username):
                    # Checking if the supplied password is correct
                    if validation.check_password(username, password):
                        # accept user
                        # Showing success message
                        messagebox.showinfo("showinfo", "Login successful")
                        # Displaying a new frame
                        controller.show_frame(Dashboard)
                        # Closing the json file
                        validation.close_file()
                    else:
                        messagebox.showerror("Error", "Enter correct password!")
                else:
                    messagebox.showerror("Error", "User does not exist!")
            else:
                messagebox.showerror("Error", validation.check_inputs(username, password))


"""
    --DashBoardPage class which launches the main system dashboard
"""


class Dashboard(tk.Frame):
    # Class constructor
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # Initializing the main dashborad frame
        dash_frame = tk.Frame(self, bg="white")
        dash_frame.place(x=0, y=0, height=340, width=750)
        # Dashboard description one
        desc = tk.Label(dash_frame, text="There is, obviously, more to the system than this,",
                        font=("Goudy old style", 17, "bold"),
                        fg="grey", bg="white").place(x=70, y=100)
        # Dashboard description two
        desc1 = tk.Label(dash_frame,
                         text=" but we are only required to create this part of it.",
                         font=("Goudy old style", 17, "bold"),
                         fg="grey", bg="white").place(x=70, y=130)


"""
    --RegisterPage class which launches loginPage after successful registration
    --Handles the user registration
"""


class RegisterPage(tk.Frame):
    # Class constructor
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # Initializing the Frame register
        Frame_register = tk.Frame(self, bg="white")
        Frame_register.place(x=0, y=0, height=340, width=750)

        # ==image Frame====
        Frame_image = tk.Frame(Frame_register)
        Frame_image.place(x=0, y=0, height=340, width=300)
        Frame_image.bg = ImageTk.PhotoImage(file="images/login.png")
        Frame_image.bg_image = tk.Label(Frame_image, image=Frame_image.bg)
        Frame_image.bg_image.place(x=0, y=0, relwidth=1, relheight=1)

        # FrameRegister title
        title = tk.Label(Frame_register, text="Register Here",
                         font=("Impact", 35, "bold"), fg="#d77337", bg="white").place(x=340, y=30)
        # Frameregister description
        desc = tk.Label(Frame_register, text="Register to login",
                        font=("Goudy old style", 15, "bold"),
                        fg="#d25d17", bg="white").place(x=340, y=100)
        # Frameregister firstname label
        first_name = tk.Label(Frame_register, text="First Name",
                              font=("Goudy old style", 15, "bold"),
                              fg="gray", bg="white").place(x=340, y=140)
        # Frame register firstname input
        first_user = tk.Entry(Frame_register, font=("times new roman", 15), bg="lightgray")
        first_user.place(x=340, y=170, width=170, height=35)
        # Frameregister lastname label
        Last_name = tk.Label(Frame_register, text="Last Name",
                             font=("Goudy old style", 15, "bold"),
                             fg="gray", bg="white").place(x=520, y=140)
        # Frameregister lastname input
        last_user = tk.Entry(Frame_register, font=("times new roman", 15), bg="lightgray")
        last_user.place(x=520, y=170, width=170, height=35)
        # Frameregister password label
        Password = tk.Label(Frame_register, text="Password",
                            font=("Goudy old style", 15, "bold"),
                            fg="gray", bg="white").place(x=340, y=210)
        # Frameregister password input
        txt_pass = tk.Entry(Frame_register, font=("times new roman", 15), bg="lightgray")
        txt_pass.place(x=340, y=240, width=350, height=35)
        # Frame register register button
        register_btn = tk.Button(Frame_register, text="Register", command=lambda: registerUser(self),
                                 fg="white", bg="#d77337", bd=0,
                                 font=("times new roman", 15)).place(x=340, y=280, width=130, height=30)
        # Frameregister back button
        back_btn = tk.Button(Frame_register, text="Back", command=lambda: controller.show_frame(HomePage),
                             fg="white", bg="#d77337", bd=0,
                             font=("times new roman", 15)).place(x=560, y=280, width=130, height=30)

        # Register user function
        def registerUser(self):
            # Getting the inputs data
            firstname = first_user.get()
            lastname = last_user.get()
            password = txt_pass.get()
            # Initializing the register user validation class
            validate = registerUserValidation()
            # Checking if all inputs are provided
            if not validate.check_inputs(firstname, lastname, password):
                # Checking if provided user already exist
                if not validate.if_user_exist(firstname, lastname):
                    # Checking if the password is strong enough
                    if validate.check_password(password):
                        # Saving the user details
                        validate.save_user(firstname, lastname, password)
                        # Displaying the success message
                        messagebox.showinfo("showinfo", "Account created successfully")
                        # Displaying the loginframe
                        controller.show_frame(LoginPage)
                        # Closing the jsonfile
                        validate.close_file()
                    else:
                        messagebox.showerror("Error", "Enter a strong password!")
                else:
                    messagebox.showerror("Error", "User already exist!")
            else:
                messagebox.showerror("Error", validate.check_inputs(firstname, lastname, password))


"""
    --RegisterUserValiadtion class
    --Handles user validation functions during registration
"""


class registerUserValidation():
    # Class constructor
    def __init__(self):
        self.data = []
        with open('data.pickle', 'rb') as handle:
            data = pickle.load(handle)
        # Reading data
        for d in data:
            self.data.append(d)


    """
        checking if user already exist
        arguments: first_name, last_name
        return: boolean
    """

    def if_user_exist(self, first_name, last_name):
        # Setting the surname data
        username = first_name[:3] + last_name[:3]
        for user in self.data:
            # Checking if the surname exist
            if user['username'] == username.lower():
                return True
        return False

    """
        saving the user details
        arguments: first_name, last_name, password
        return: none
    """

    def save_user(self, first_name, last_name, password):
        # Modifying the surname
        username = first_name[:3] + last_name[:3]
        # User data
        user = {'username': username.lower(), 'password': password}
        # Appending the user to the data list
        self.data.append(user)
        with open('data.pickle', 'wb') as handle:
            pickle.dump(self.data, handle, protocol=pickle.HIGHEST_PROTOCOL)

    """
        Checking if all the user details are supplied
        arguments: first_name, last_name, password
        return: string
    """

    def check_inputs(self, first_name, surname, password):
        # Checking if all inputs are supplied
        if first_name == "" or surname == "" or password == "":
            message = "All fields are required"
        # Checking if password length is greater than 8 characters
        elif 8 > len(password):
            message = "Password too short!"
        # Checking if the password length is less than 16 characters
        elif len(password) > 16:
            message = "Password too long!"
        else:
            message = ""
        # returning the message
        return message

    """
        Checking if password is strong enough
        arguments: password
        return: boolean
    """

    def check_password(self, password):
        if re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', password):
            # match
            return True
        else:
            # no match
            return False

    """
        Closing the json file
        arguments: none
        return: none
    """

    def close_file(self):
        pass
        #self.myjsonfile.close()


"""
    --LoginUserValidatiuon class
    --Handles user validation functions during login
"""


class loginUserValidation():
    # Class constructor
    def __init__(self):
        self.data = []
        with open('data.pickle', 'rb') as handle:
            data = pickle.load(handle)
        # Reading json data
        for d in data:
            self.data.append(d)


    """
        Checking if all the user details are supplied
        arguments: surname, password
        return: string
    """

    def check_inputs(self, surname, password):
        # checking if all the data is supplied
        if surname == "" or password == "":
            message = "All fields are required"
        # Checking if the password is more than 8 characters long
        elif 8 > len(password):
            message = "Password too short!"
        # checking if the password is less than 16 characters long
        elif len(password) > 16:
            message = "Password too long!"
        else:
            message = ""
        # returning the message
        return message

    """
        checking if user exist
        arguments: surname
        return: boolean
    """

    def if_user_exist(self, username):
        for user in self.data:
            if user['username'] == username.lower():
                return True
        return False

    """
        checking if password is correct
        arguments: username,password
        return: boolean
    """

    def check_password(self, username, password):
        for user in self.data:
            if user['username'] == username and user['password'] == password:
                return True
        return False

    """
        Closing the json file
    """

    def close_file(self):
        pass


# Main app
app = MainApp()
app.mainloop()
