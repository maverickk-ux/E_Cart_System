import mainpage
import customtkinter as ctk
import tkinter
from tkinter import messagebox
import customtkinter
from PIL import ImageTk, Image
import json
# import openpyxl


class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.geometry("600x440")
        self.root.title("Login")

        # Set appearance and theme
        customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

        # Background image
        self.img1 = ImageTk.PhotoImage(Image.open("pattern.png"))
        self.l1 = customtkinter.CTkLabel(master=root, image=self.img1)
        self.l1.pack()

        # Create custom frame
        self.frame = customtkinter.CTkFrame(master=self.l1, width=370, height=360, corner_radius=15)
        self.frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        # Add widgets
        self.add_widgets()

    def add_widgets(self):
        # Welcome Label
        l2 = customtkinter.CTkLabel(
            master=self.frame, text="Welcome to Ecommerce Cart!!", font=("Century Gothic", 18)
        )
        l2.place(x=50, y=45)

        # Username Entry
        self.entry1 = customtkinter.CTkEntry(master=self.frame, width=220, placeholder_text="Username")
        self.entry1.place(x=80, y=110)

        # Password Entry
        self.entry2 = customtkinter.CTkEntry(master=self.frame, width=220, placeholder_text="Password", show="*")
        self.entry2.place(x=80, y=165)

        # Forget Password Label
        l3 = customtkinter.CTkLabel(master=self.frame, text="Forget password?", font=("Century Gothic", 12))
        l3.place(x=185, y=195)

        # Login Button
        button1 = customtkinter.CTkButton(
            master=self.frame, width=220, text="Login", command=self.login_function, corner_radius=6
        )
        button1.place(x=80, y=240)

        # Signup Button
        button2 = customtkinter.CTkButton(
            master=self.frame,height=10, width=100, text="Signup", command=self.signup_function, corner_radius=6, bg_color="#2B2B2B"
        )
        button2.place(x=200, y=280)

    def login_function(self):
        # # Destroy the current window and create the Welcome Page
        username = self.entry1.get()
        password = self.entry2.get()
        try:
            with open('users.json', 'r') as f:
                users = json.load(f)
            if username not in users:
                messagebox.showinfo("Account invalid","Please signup!!")
            elif username in users and users[username] == password:
                messagebox.showinfo("Success", "Login successful!")
                self.root.destroy()
                self.open_main_page()
            else:
                messagebox.showerror("Error", "Invalid credentials!")
        except FileNotFoundError:
            messagebox.showerror("Error", "No users found. Please signup!")

    def signup_function(self):
        username = self.entry1.get()
        password = self.entry2.get()
        if username and password:
            try:
                with open('users.json', 'r') as f:
                    users = json.load(f)
            except FileNotFoundError:
                users = {}
            if username in users:
                messagebox.showerror("Error", "User already exists!")
            else:
                users[username] = password
                with open('users.json', 'w') as f:
                    json.dump(users, f)
                messagebox.showinfo("Success", "Signup successful!")
        else:
            messagebox.showerror("Error", "Username and Password cannot be empty!")
        
    def open_main_page(self):
        root = ctk.CTk()
        mainpage.MainPage(root)
        root.mainloop()



if __name__ == "__main__":
    root = customtkinter.CTk()
    app = LoginPage(root)
    root.mainloop()
