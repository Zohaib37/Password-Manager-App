from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = [random.choice(letters) for i in range(nr_letters)]
    password_list += [random.choice(symbols) for i in range(nr_symbols)]
    password_list += [random.choice(numbers) for i in range(nr_numbers)]

    random.shuffle(password_list)

    password = ""
    for char in password_list:
        password += char

    pyperclip.copy(password)
    password_entry.insert(0, password)


def search():
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
            email_to_show = data[website_entry.get().lower()]["email"]
            password_to_show = data[website_entry.get().lower()]["password"]
    except FileNotFoundError:
        messagebox.showerror(title="No file found", message="No data file exists")
    except ValueError:
        messagebox.showerror(title="Empty Data File", message="No data in file")
    except KeyError:
        messagebox.showerror(title="Invalid Website", message="This website does not exist")
    else:
        messagebox.showinfo(title=f"{website_entry.get()}", message=f"email:  {email_to_show}\n"
                            f"password:  {password_to_show}")


def write_to_file(data_to_add):
    with open("data.json", "w") as data_file:
        json.dump(data_to_add, data_file, indent=4)


def add_data():
    website_input = website_entry.get().lower()
    email_input = email_entry.get()
    password_input = password_entry.get()
    json_data = {
        website_input: {
            "email": email_input,
            "password": password_input
        }
    }

    if website_input == "" or email_input == "" or password_input == "":
        messagebox.showerror(title="Error", message="No field can be empty")
    else:
        confirm = messagebox.askquestion(title="Confirm", message="Are you sure?")
        if confirm == "yes":
            try:
                with open("data.json", "r") as data_file:
                    data = json.load(data_file)
                    data.update(json_data)
            except (FileNotFoundError, ValueError):
                write_to_file(json_data)
            else:
                write_to_file(data)

            website_entry.delete(0, END)
            email_entry.delete(0, END)
            password_entry.delete(0, END)


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
lock_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_image)
canvas.grid(row=0, column=1)

website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

website_entry = Entry(width=28)
website_entry.grid(row=1, column=1, pady=10, sticky="W")
website_entry.focus_set()

email_entry = Entry(width=50)
email_entry.grid(row=2, column=1, pady=10, columnspan=2, sticky="EW")

password_entry = Entry(width=28)
password_entry.grid(row=3, column=1, sticky="W")

password_button = Button(text="Generate Password", command=generate_password)
password_button.grid(row=3, column=2, sticky="W")

add_button = Button(text="Add", width=36, command=add_data)
add_button.grid(row=4, column=1, columnspan=2, pady=10, sticky="EW")

search_button = Button(text="Search", width=15, command=search)
search_button.grid(row=1, column=2, sticky="W")
















window.mainloop()
