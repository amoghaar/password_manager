# Import necessary modules
from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import json
import pyperclip

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

# Function to generate a random password


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    final_list = []
    # Choose random letters
    letter_list = [final_list.append(choice(letters)) for char in range(randint(8, 10))]
    # Choose random symbols
    symbol_list = [final_list.append(choice(symbols)) for char in range(randint(2, 4))]
    # Choose random numbers
    number_list = [final_list.append(choice(numbers)) for char in range(randint(2, 4))]
    shuffle(final_list)

    generated_password = "".join(final_list)

    user_password.insert(0, generated_password)
    pyperclip.copy(generated_password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
# Function to save the entered password information


def save():
    if len(user_website.get()) == 0 or len(user_password.get()) == 0:
        messagebox.showerror(title="Not Allowed", message="Please make sure that the form is filled properly.")
    else:
        website_name = user_website.get()
        email_username_from_input = user_email_username.get()
        password_from_input = user_password.get()

        # Ask for user confirmation to save the information
        is_ok = messagebox.askokcancel(title=website_name, message=f"These are the details entered:\n"
                                                                     f"Website: {website_name}\n"
                                                                     f"Email-Username: {email_username_from_input}\n"
                                                                     f"Password: {password_from_input}\nIs it ok to save?")
        info_dict = {
            website_name: {
                "email_username": email_username_from_input,
                "password": password_from_input,
            }
        }
        if is_ok:
            try:
                # Try to open the data file and read existing data
                with open("data.json", "r") as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:
                data = {}

            # Update the data with the new information
            data.update(info_dict)

            # Write the updated data back to the file
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)

            # Clear the input fields after saving
            user_website.delete(0, END)
            user_password.delete(0, END)

# ---------------------------- FIND PASSWORD ------------------------------- #
# Function to search for a password by website name


def search():
    website_name = user_website.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
            # Display the email and password for the specified website
            messagebox.showinfo(title=website_name, message=f"Email: {data[website_name]['email_username']}\n"
                                                            f"Password: {data[website_name]['password']}")
    except FileNotFoundError:
        # Handle the case when the data file doesn't exist
        messagebox.showinfo(title="File Not Found", message="Sorry, the 'data.json' file does not exist.\n"
                                                            "To solve this, try filling the form and"
                                                            " hit the 'Add' button")
    except KeyError:
        # Handle the case when the website is not found in the data
        messagebox.showinfo(title=website_name, message=f"Sorry, you have not saved information about {website_name}")

# ---------------------------- UI SETUP ------------------------------- #

# Create the main application window


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)
canvas = Canvas(width=200, height=200)
image = PhotoImage(file="logo.png")  # Image file assumed to be "logo.png"
canvas.create_image(100, 100, image=image)
canvas.grid(column=1, row=0)

# Labels
website = Label(text="Website: ")
website.grid(column=0, row=1)
website.focus()

email_username = Label(text="Email/Username: ")
email_username.grid(column=0, row=2)

password = Label(text="Password: ")
password.grid(column=0, row=3)

# Entries
user_website = Entry(width=31)
user_website.focus()
user_website.grid(column=1, row=1)

user_email_username = Entry(width=50)
user_email_username.insert(END, "@gmail.com")
user_email_username.grid(column=1, row=2, columnspan=2)

user_password = Entry(width=31)
user_password.grid(column=1, row=3)

# Buttons
search_button = Button(text="Search", width=15, command=search)
search_button.grid(column=2, row=1)

generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(column=2, row=3)

add_button = Button(text="Add", width=44, command=save)
add_button.grid(column=1, row=4, columnspan=2)

# Start the main loop to run the application
window.mainloop()
