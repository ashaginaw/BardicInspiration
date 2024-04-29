import tkinter as tk
from tkinter import messagebox
import os
from PIL import Image, ImageTk
import tkinter.font as font
import subprocess

main_window = None  # Declare main_window as a global variable

def login():
    username = username_entry.get()
    password = password_entry.get()

    # Check if the username and password are correct
    if username == "admin" and password == "admin":
        # Hide the login window
        login_window.withdraw()
        # If login successful, show the main page and pass the root Tk() instance
        show_main_page()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def show_main_page():
    global main_window  # Access the global main_window variable
    main_window = tk.Toplevel()
    main_window.title("Bardic Inspiration Main Page")
    main_window.geometry("1000x500")
    
    # Add protocol handler to close the main window properly
    main_window.protocol("WM_DELETE_WINDOW", main_window.quit)
    def load_image(image_label):
        try:
            image_path = "Logos and Pictures/new-logo-color.png"
            image = Image.open(image_path)
            max_width = 1000
            max_height = 200
            image.thumbnail((max_width, max_height))
            photo = ImageTk.PhotoImage(image)
        
        # Store the image reference as an attribute of the label widget
            image_label.photo = photo  # Store the reference to prevent garbage collection
            image_label.config(image=photo)  # Update the label with the new image
        
            image_label.place(x=275, y=50)
        except Exception as e:
            print("Error loading image:", e)

    def load_canvas():
        canvas = tk.Canvas(main_window, width=1000, height=700, bg="SlateGray")
        canvas.create_text(500, 350, font=("Fixedsys", 11), fill="Grey1",
                           text="Introducing this groundbreaking application that revolutionizes music creation:\n"
                                "With this platform, users can craft soundtracks effortlessly.\n"
                                "By tapping into an extensive database of music genres,\n"
                                "individuals can specify their preferences, guiding the advanced Machine Learning algorithms to\n"
                                "curate the ideal composition for their project or campaign.\n"
                                " Whether it's the energetic pulse of electronic beats\n"
                                "or the soulful melodies of jazz, Bardic Inspiration ensures a seamless fusion of creativity and technology,\n"
                                "empowering users to bring their visions to life with tailor-made soundscapes.\n"
                                "Say goodbye to generic stock music and hello to personalized, captivating compositions—\n"
                                "discover the future of music creation with the app today!",
                           justify="center")
        canvas.pack()

    def search_callback():
        output = subprocess.check_output('python music_classification.py', shell=True)
        print(output)

    def add_music():
        os.system('python file_upload.py')

    def extract_features():
        os.system('python feature_extraction.py')

    def train_model():
        os.system('python lstm_network.py')

    load_canvas()
    image_label = tk.Label(main_window)
    image_label.pack()
    load_image(image_label)

    myFont = font.Font(family='Helvetica')

    btn = tk.Button(main_window, text="Choose Music Attributes", fg="Gray5", command=search_callback)
    btn['font'] = myFont
    btn.place(relx=0.2, rely=0.93, anchor="center")

    btn2 = tk.Button(main_window, text="Add Music", fg="Gray5", command=add_music)
    btn2['font'] = myFont
    btn2.place(relx=0.4, rely=0.93, anchor="center")

    btn3 = tk.Button(main_window, text="Extract Features", fg="Gray5", command=extract_features)
    btn3['font'] = myFont
    btn3.place(relx=0.6, rely=0.93, anchor="center")

    btn4 = tk.Button(main_window, text="Create Music", fg="Gray5", command=train_model)
    btn4['font'] = myFont
    btn4.place(relx=0.8, rely=0.93, anchor="center")

    main_window.mainloop()

# Create the login window
login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("300x150")

# Username label and entry
username_label = tk.Label(login_window, text="Username:")
username_label.grid(row=0, column=0, sticky="e")
username_entry = tk.Entry(login_window)
username_entry.grid(row=0, column=1)

# Password label and entry
password_label = tk.Label(login_window, text="Password:")
password_label.grid(row=1, column=0, sticky="e")
password_entry = tk.Entry(login_window, show="*")
password_entry.grid(row=1, column=1)

# Login button
login_button = tk.Button(login_window, text="Login", command=login)
login_button.grid(row=2, columnspan=2)

login_window.mainloop()